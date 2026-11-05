"""Первый текстовый классификатор: TF-IDF + логистическая регрессия.

Тот же путь, что в уроке 01_classification_basics.md: текст -> вектор TF-IDF ->
оценки классов -> вероятности -> класс с наибольшей вероятностью.
"""
from pathlib import Path

from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import json

# Корень репозитория: здесь лежат data/ и artifacts/.
ROOT = Path(__file__).resolve().parents[2]


def data(name):
    """Учебный набор из data/<name>.json."""
    return json.loads((ROOT / 'data' / (name + '.json')).read_text())


rows = data('tickets')
train = [r for r in rows if r['split'] == 'train']
test = [r for r in rows if r['split'] == 'test']

# Pipeline: сначала тексты -> TF-IDF векторы, затем логистическая регрессия.
# C=1 задаёт обратную силу регуляризации; это значение по умолчанию.
model = make_pipeline(TfidfVectorizer(),
                      LogisticRegression(C=1, random_state=42))
# fit: словарь, IDF и веса строятся только по train.
model.fit([r['text'] for r in train], [r['label'] for r in train])

# predict: test переводится в векторы уже готовым словарём.

pred = model.predict([r['text'] for r in test])
print(classification_report([r['label'] for r in test], pred, zero_division=0))
for row, label in zip(test, pred):
    print(row['text'], '=>', label, 'ожидалось:', row['label'])
print('Крошечный синтетический test: это не оценка качества в production.')
