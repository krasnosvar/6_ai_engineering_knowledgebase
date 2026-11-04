from pathlib import Path

import argparse
import json
import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model, PeftModel

ROOT = Path(__file__).resolve().parents[2]  # корень репы: здесь data/ и artifacts/


def data(name):
    """Учебный набор из data/<name>.json."""
    return json.loads((ROOT / 'data' / (name + '.json')).read_text())


def require_model():
    """Путь к локальным весам; модели вручную кладутся в artifacts/models/."""
    model = ROOT / 'artifacts/models/smollm2-135m'
    if not (model / 'config.json').is_file():
        raise SystemExit('Модель отсутствует. См. data/models.md: ссылки и ручное размещение файлов.')
    return model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--steps', type=int, default=12)
    args=parser.parse_args()
    if args.steps<1: parser.error('--steps must be positive')
    torch.manual_seed(42)
    torch.set_num_threads(2)
    path = require_model()
    target = ROOT / 'artifacts/adapter'  # сюда сохраним адаптер и отчёт
    if target.exists(): raise SystemExit('artifacts/adapter already exists: preserve or move it before a new run.')
    tok=AutoTokenizer.from_pretrained(path,local_files_only=True,trust_remote_code=False)
    base=AutoModelForCausalLM.from_pretrained(path,local_files_only=True,trust_remote_code=False)
    rows = data('sft')
    train = [r for r in rows if r['split'] == 'train']
    test = [r for r in rows if r['split'] == 'test']

    def evaluate(model):
        """Жадная генерация (без случайности) ответа на каждый test-запрос."""
        model.eval()
        results = []
        with torch.inference_mode():
            for row in test:
                x=tok.apply_chat_template([{'role':'user','content':row['prompt']}],add_generation_prompt=True,return_tensors='pt')
                out=model.generate(x,attention_mask=torch.ones_like(x),max_new_tokens=4,do_sample=False,pad_token_id=tok.eos_token_id)
                answer=tok.decode(out[0,x.shape[1]:],skip_special_tokens=True).strip().lower()
                results.append({'id':row['id'],'expected':row['answer'],'answer':answer,'correct':answer==row['answer']})
        return results

    before = evaluate(base)  # качество базы до обучения

    # LoRA r=4 только на проекциях q и v внутри attention; база заморожена.
    config=LoraConfig(r=4,lora_alpha=8,target_modules=['q_proj','v_proj'],lora_dropout=0,task_type='CAUSAL_LM')
    model = get_peft_model(base, config)
    model.print_trainable_parameters()
    model.train()
    # Оптимизатор получает только обучаемые параметры — матрицы адаптера.
    opt=torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],lr=3e-4)
    losses = []
    started = time.perf_counter()
    for step in range(args.steps):
        row=train[step%len(train)]
        prompt=tok.apply_chat_template([{'role':'user','content':row['prompt']}],tokenize=False,add_generation_prompt=True)
        prefix=tok(prompt,add_special_tokens=False)['input_ids']
        # Concatenating token IDs makes the loss boundary exact; no padding in batch=1.
        completion=tok(row['answer']+tok.eos_token,add_special_tokens=False)['input_ids']
        ids = torch.tensor([prefix + completion])
        labels = ids.clone()
        labels[:, :len(prefix)] = -100  # loss только на ответе, не на запросе
        assert (labels!=-100).any()
        opt.zero_grad()
        loss = model(input_ids=ids, attention_mask=torch.ones_like(ids), labels=labels).loss
        if not torch.isfinite(loss): raise RuntimeError('Non-finite loss')
        loss.backward()
        opt.step()
        losses.append(loss.item())

    model.save_pretrained(target)
    # Проверяем то, что сохранено на диск: загружаем базу заново и подключаем адаптер.
    del model, base, opt
    fresh=AutoModelForCausalLM.from_pretrained(path,local_files_only=True,trust_remote_code=False)
    restored=PeftModel.from_pretrained(fresh,target)
    after=evaluate(restored)
    report={'steps':args.steps,'seed':42,'train_loss':losses,'elapsed_seconds':time.perf_counter()-started,
            'model_manifest':json.loads((ROOT/'data/models.json').read_text()),'before':before,'after':after,
            'note':'Small synthetic experiment; no quality improvement is guaranteed.'}
    (target/'experiment.json').write_text(json.dumps(report,indent=2))
    print('base accuracy:',sum(r['correct'] for r in before)/len(before))
    print('adapter accuracy:',sum(r['correct'] for r in after)/len(after))
    print('report:',target/'experiment.json')
if __name__=='__main__': main()
