from pathlib import Path

import importlib.util
import json
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


# Берём исполнитель из соседнего 01_executor.py: модель только ПРЕДЛАГАЕТ
# действие, проверяет и выполняет его наш код.
spec = importlib.util.spec_from_file_location(
    'executor', Path(__file__).with_name('01_executor.py'))
executor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(executor)

torch.set_num_threads(2)
path = require_model()
tok = AutoTokenizer.from_pretrained(
    path, local_files_only=True, trust_remote_code=False)
model = AutoModelForCausalLM.from_pretrained(
    path, local_files_only=True, trust_remote_code=False).eval()
messages = [{'role': 'user', 'content': (
    'Check demo service metrics. Return only JSON with tool and arguments. '
    'The only tool is read_metrics with argument service. '
    'Example: {"tool":"read_metrics","arguments":{"service":"demo"}}')}]
# return_dict=False: вернуть тензор ID токенов, а не словарь (BatchEncoding);
# в будущих версиях Transformers умолчание может смениться.
x = tok.apply_chat_template(messages, add_generation_prompt=True,
                            return_tensors='pt', return_dict=False)
with torch.inference_mode():
    out = model.generate(x, attention_mask=torch.ones_like(x),
                         max_new_tokens=64, do_sample=False,
                         pad_token_id=tok.eos_token_id)
# Только новые токены, без повторения входа.
raw = tok.decode(out[0, x.shape[1]:], skip_special_tokens=True)
print('MODEL:', raw)

# Модель могла вернуть не JSON: это честный результат шага,
# а не повод скрыть ошибку.
try:
    result = executor.run([json.loads(raw)])
except json.JSONDecodeError as e:
    result = {'status': 'invalid_json', 'reason': str(e)}
print('RESULT:', result)
print('One tool-selection step, not a complete autonomous diagnostic agent.')
