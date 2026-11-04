from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Корень репы: здесь data/ и artifacts/.
ROOT = Path(__file__).resolve().parents[2]


def require_model():
    """Путь к локальным весам; модели вручную кладутся в artifacts/models/."""
    model = ROOT / 'artifacts/models/smollm2-135m'
    if not (model / 'config.json').is_file():
        raise SystemExit('Модель отсутствует. См. data/models.md: '
                         'ссылки и ручное размещение файлов.')
    return model


torch.set_num_threads(2)
torch.manual_seed(42)
path = require_model()

# local_files_only: ничего не скачивать; trust_remote_code=False: не выполнять
# код из папки модели.
tokenizer = AutoTokenizer.from_pretrained(
    path, local_files_only=True, trust_remote_code=False)
model = AutoModelForCausalLM.from_pretrained(
    path, local_files_only=True, trust_remote_code=False).eval()

# Диалог из одного сообщения пользователя; chat template добавит маркеры ролей,
# а add_generation_prompt — начало ответа ассистента.
messages = [{'role': 'user',
             'content': 'Explain in one sentence what a database index does.'}]
# return_dict=False: вернуть тензор ID токенов, а не словарь (BatchEncoding);
# в будущих версиях Transformers умолчание может смениться.
x = tokenizer.apply_chat_template(
    messages, tokenize=True, add_generation_prompt=True,
    return_tensors='pt', return_dict=False)

with torch.inference_mode():
    out = model.generate(
        x,
        attention_mask=torch.ones_like(x),
        max_new_tokens=48,
        do_sample=False,  # greedy: всегда самый вероятный токен
        pad_token_id=tokenizer.eos_token_id,
    )

# out содержит вход и продолжение; печатаем только новые токены.
print(tokenizer.decode(out[0, x.shape[1]:], skip_special_tokens=True))
print('input tokens:', x.shape[1], 'output tokens:', out.shape[1] - x.shape[1])
