"""Короткое SFT с LoRA для локальной SmolLM2-135M-Instruct на CPU.

Сравнивает ответы базы и адаптера на test из data/sft.json и пишет отчёт
в artifacts/adapter/experiment.json. QLoRA (4-битную базу) не выполняет.
"""
from pathlib import Path

import argparse
import json
import time

import torch
from peft import LoraConfig, PeftModel, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer

# Корень репы: здесь data/ и artifacts/.
ROOT = Path(__file__).resolve().parents[2]


def data(name):
    """Учебный набор из data/<name>.json."""
    return json.loads((ROOT / 'data' / (name + '.json')).read_text())


def require_model():
    """Путь к локальным весам; модели вручную кладутся в artifacts/models/."""
    model = ROOT / 'artifacts/models/smollm2-135m'
    if not (model / 'config.json').is_file():
        raise SystemExit('Модель отсутствует. См. data/models.md: '
                         'ссылки и ручное размещение файлов.')
    return model


def load_base(path):
    """Загружает базовую модель только из локальных файлов."""
    # local_files_only: ничего не скачивать; trust_remote_code=False: не
    # выполнять код из папки модели.
    return AutoModelForCausalLM.from_pretrained(
        path, local_files_only=True, trust_remote_code=False)


def evaluate(model, tok, rows):
    """Жадная генерация (без случайности) ответа на каждый test-запрос."""
    model.eval()
    results = []
    with torch.inference_mode():
        for row in rows:
            messages = [{'role': 'user', 'content': row['prompt']}]
            # return_dict=False: вернуть тензор ID токенов, а не словарь
            # (BatchEncoding); в будущих версиях Transformers умолчание
            # может смениться.
            x = tok.apply_chat_template(
                messages, add_generation_prompt=True,
                return_tensors='pt', return_dict=False)
            out = model.generate(
                x, attention_mask=torch.ones_like(x), max_new_tokens=4,
                do_sample=False, pad_token_id=tok.eos_token_id)
            # out содержит вход и продолжение; берём только новые токены.
            answer = tok.decode(out[0, x.shape[1]:],
                                skip_special_tokens=True).strip().lower()
            results.append({'id': row['id'], 'expected': row['answer'],
                            'answer': answer,
                            'correct': answer == row['answer']})
    return results


def training_example(tok, row):
    """input_ids и labels одного примера: loss только на ответе и EOS."""
    prompt = tok.apply_chat_template(
        [{'role': 'user', 'content': row['prompt']}],
        tokenize=False, add_generation_prompt=True)
    prefix = tok(prompt, add_special_tokens=False)['input_ids']
    # Токенизируем prompt и ответ по отдельности и склеиваем ID: так граница
    # prompt/ответ точно известна. В batch один пример, поэтому без padding.
    completion = tok(row['answer'] + tok.eos_token,
                     add_special_tokens=False)['input_ids']
    ids = torch.tensor([prefix + completion])
    labels = ids.clone()
    labels[:, :len(prefix)] = -100  # позиции prompt не входят в loss
    assert (labels != -100).any(), 'no target tokens left'
    return ids, labels


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--steps', type=int, default=12)
    args = parser.parse_args()
    if args.steps < 1:
        parser.error('--steps must be positive')
    torch.manual_seed(42)
    torch.set_num_threads(2)
    path = require_model()
    target = ROOT / 'artifacts/adapter'  # сюда сохраним адаптер и отчёт
    if target.exists():
        raise SystemExit('artifacts/adapter already exists: '
                         'preserve or move it before a new run.')
    tok = AutoTokenizer.from_pretrained(
        path, local_files_only=True, trust_remote_code=False)
    base = load_base(path)
    rows = data('sft')
    train = [r for r in rows if r['split'] == 'train']
    test = [r for r in rows if r['split'] == 'test']

    before = evaluate(base, tok, test)  # качество базы до обучения

    # LoRA r=4, alpha=8 (масштаб alpha/r = 2) только на проекциях q и v
    # внутри attention; остальные веса базы заморожены.
    config = LoraConfig(r=4, lora_alpha=8,
                        target_modules=['q_proj', 'v_proj'],
                        lora_dropout=0, task_type='CAUSAL_LM')
    model = get_peft_model(base, config)
    # Печатает число обучаемых (A и B) и всех параметров.
    model.print_trainable_parameters()
    model.train()
    # Оптимизатор получает только обучаемые параметры — матрицы адаптера.
    opt = torch.optim.AdamW(
        [p for p in model.parameters() if p.requires_grad], lr=3e-4)
    losses = []
    started = time.perf_counter()
    for step in range(args.steps):
        # batch = 1: по очереди берём обучающие примеры по кругу.
        ids, labels = training_example(tok, train[step % len(train)])
        opt.zero_grad()
        # Сдвиг labels на одну позицию модель делает сама.
        loss = model(input_ids=ids, attention_mask=torch.ones_like(ids),
                     labels=labels).loss
        if not torch.isfinite(loss):
            raise RuntimeError('Non-finite loss')
        loss.backward()
        opt.step()
        losses.append(loss.item())

    model.save_pretrained(target)  # сохраняются только A, B и настройки
    # Проверяем то, что сохранено на диск: загружаем базу заново и
    # подключаем адаптер из файла.
    del model, base, opt
    restored = PeftModel.from_pretrained(load_base(path), target)
    after = evaluate(restored, tok, test)
    report = {
        'steps': args.steps,
        'seed': 42,
        'train_loss': losses,
        'elapsed_seconds': time.perf_counter() - started,
        'model_manifest': json.loads(
            (ROOT / 'data/models.json').read_text()),
        'before': before,
        'after': after,
        'note': 'Small synthetic experiment; '
                'no quality improvement is guaranteed.',
    }
    (target / 'experiment.json').write_text(json.dumps(report, indent=2))
    print('base accuracy:', sum(r['correct'] for r in before) / len(before))
    print('adapter accuracy:', sum(r['correct'] for r in after) / len(after))
    print('report:', target / 'experiment.json')


if __name__ == '__main__':
    main()
