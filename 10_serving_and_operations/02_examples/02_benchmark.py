from pathlib import Path

import json
import time

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
path = require_model()
tok = AutoTokenizer.from_pretrained(
    path, local_files_only=True, trust_remote_code=False)
model = AutoModelForCausalLM.from_pretrained(
    path, local_files_only=True, trust_remote_code=False).eval()
# return_dict=False: вернуть тензор ID токенов, а не словарь (BatchEncoding);
# в будущих версиях Transformers умолчание может смениться.
x = tok.apply_chat_template(
    [{'role': 'user', 'content': 'Explain how a database works.'}],
    add_generation_prompt=True, return_tensors='pt', return_dict=False)

timings = []
counts = []
with torch.inference_mode():
    for i in range(4):
        start = time.perf_counter()
        out = model.generate(x, attention_mask=torch.ones_like(x),
                             max_new_tokens=24, do_sample=False,
                             pad_token_id=tok.eos_token_id)
        elapsed = time.perf_counter() - start
        if i == 0:
            # Первый запуск — прогрев: выделение памяти, ленивые инициализации.
            # Его не смешиваем с замерами.
            print('warmup seconds:', round(elapsed, 3))
        else:
            timings.append(elapsed)
            counts.append(out.shape[1] - x.shape[1])  # только новые токены

# Имя метрики прямо говорит, что это полное время generate, а не TTFT.
report = {
    'metric': 'end_to_end_generate_seconds_NOT_TTFT',
    'input_tokens': x.shape[1],
    'seconds': timings,
    'output_tokens': counts,
    'cpu_threads': 2,
    'concurrency': 1,
    'output_tokens_per_second': [n / t for n, t in zip(counts, timings)],
}
outpath = ROOT / 'artifacts/benchmark.json'
outpath.parent.mkdir(exist_ok=True)
outpath.write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
print('Three samples are not enough for a meaningful p95.')
