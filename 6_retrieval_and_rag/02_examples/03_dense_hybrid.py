from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModel
from sklearn.feature_extraction.text import TfidfVectorizer
import json

ROOT = Path(__file__).resolve().parents[2]  # корень репы: здесь data/ и artifacts/


def data(name):
    """Учебный набор из data/<name>.json."""
    return json.loads((ROOT / 'data' / (name + '.json')).read_text())


path = ROOT / 'artifacts/models/minilm'
if not (path / 'config.json').exists():
    raise SystemExit('MiniLM absent. See data/models.md; no automatic download.')
torch.set_num_threads(2)
tok = AutoTokenizer.from_pretrained(path, local_files_only=True, trust_remote_code=False)
model = AutoModel.from_pretrained(path, local_files_only=True, trust_remote_code=False).eval()


def encode(texts):
    """Embedding текста: masked mean векторов токенов, затем нормализация до длины 1."""
    inputs = tok(texts, padding=True, truncation=True, max_length=256, return_tensors='pt')
    with torch.inference_mode():
        hidden = model(**inputs).last_hidden_state          # (тексты, токены, d)
        mask = inputs['attention_mask'].unsqueeze(-1)        # 1 — реальный токен, 0 — padding
        pooled = (hidden * mask).sum(1) / mask.sum(1)        # среднее только по реальным
        return torch.nn.functional.normalize(pooled, p=2, dim=1)


tenant = 'public'
query = 'How can I limit repeated requests after server throttling?'
docs = [d for d in data('documents') if d['tenant'] in ('public', tenant)]

# Смысловой поиск: векторы длины 1, поэтому скалярное произведение = косинус.
emb = encode([d['text'] for d in docs])
dense = (emb @ encode([query]).T).squeeze(1)

# Поиск по словам: TF-IDF.
v = TfidfVectorizer()
mat = v.fit_transform([d['text'] for d in docs])
lexical = (mat @ v.transform([query]).T).toarray().ravel()

rankings = [
    [docs[i]['id'] for i in dense.argsort(descending=True).tolist()],
    [docs[i]['id'] for i in lexical.argsort()[::-1].tolist() if lexical[i] > 0],
]

# RRF: каждый рейтинг добавляет документу 1/(60+rank); rank начинается с 1.
fused = {}
for ranking in rankings:
    for rank, key in enumerate(ranking, 1):
        fused[key] = fused.get(key, 0) + 1 / (60 + rank)

print('dense:', rankings[0][:3])
print('lexical:', rankings[1][:3])
print('RRF:', sorted(fused, key=lambda key: (-fused[key], key))[:3])
print('Expected source: d8. Evaluate on more than one query before selecting a method.')
