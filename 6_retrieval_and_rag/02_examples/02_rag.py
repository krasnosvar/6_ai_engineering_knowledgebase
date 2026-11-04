from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import json

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


# Команда пользователя берётся из доверенной авторизации, а не из ответа модели.
tenant = 'team-a'
query = 'What is the error budget of the exercise service atlas?'

# 1. Поиск: только разрешённые документы, два лучших по TF-IDF.
docs = [d for d in data('documents') if d['tenant'] in ('public', tenant)]
v = TfidfVectorizer()
matrix = v.fit_transform([d['text'] for d in docs])
scores = (matrix @ v.transform([query]).T).toarray().ravel()
best = scores.argsort()[::-1][:2]  # [::-1] разворачивает порядок: по убыванию
selected = [docs[i] for i in best if scores[i] > 0]
assert all(d['tenant'] != 'team-b' for d in selected)

# 2. Контекст с ID источников, чтобы модель могла на них сослаться.
context = '\n'.join(f"[{d['id']}] {d['text']}" for d in selected)

# 3. Генерация ответа по найденным источникам.
torch.set_num_threads(2)
path = require_model()
tok = AutoTokenizer.from_pretrained(
    path, local_files_only=True, trust_remote_code=False)
model = AutoModelForCausalLM.from_pretrained(
    path, local_files_only=True, trust_remote_code=False).eval()
prompt = (
    'Use only the sources below. If absent, say unknown. Cite source IDs.\n'
    f'Sources:\n{context}\nQuestion: {query}'
)
# return_dict=False: вернуть тензор ID токенов, а не словарь (BatchEncoding);
# в будущих версиях Transformers умолчание может смениться.
x = tok.apply_chat_template(
    [{'role': 'user', 'content': prompt}], add_generation_prompt=True,
    return_tensors='pt', return_dict=False)
with torch.inference_mode():
    out = model.generate(
        x,
        attention_mask=torch.ones_like(x),
        max_new_tokens=64,
        do_sample=False,
        pad_token_id=tok.eos_token_id,
    )
print('SOURCES:', context)
print('ANSWER:', tok.decode(out[0, x.shape[1]:], skip_special_tokens=True))
print('Manually check 43 minutes and source d9; '
      'generation correctness is not asserted.')
