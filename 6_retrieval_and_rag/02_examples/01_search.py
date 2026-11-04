from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import json

ROOT = Path(__file__).resolve().parents[2]  # корень репы: здесь data/ и artifacts/


def data(name):
    """Учебный набор из data/<name>.json."""
    return json.loads((ROOT / 'data' / (name + '.json')).read_text())


def search(query, tenant, k=3):
    # Права доступа ДО поиска: только общие документы и документы своей команды.
    docs = [d for d in data('documents') if d['tenant'] in ('public', tenant)]

    # TF-IDF: каждый документ -> вектор весов слов.
    vectorizer = TfidfVectorizer()
    x = vectorizer.fit_transform([d['text'] for d in docs])

    # Оценка документа = скалярное произведение его вектора с вектором запроса.
    scores = (x @ vectorizer.transform([query]).T).toarray().ravel()

    # argsort(-scores): номера документов по убыванию оценки; берём первые k.
    order = np.argsort(-scores, kind='stable')[:k]
    return [(docs[i], float(scores[i])) for i in order if scores[i] > 0]


if __name__ == '__main__':
    values = []
    for q in data('queries'):
        hits = search(q['query'], q['tenant'])
        found = [d['id'] for d, _ in hits]
        if q['relevant']:
            # Recall@3: какая доля нужных документов попала в первые 3.
            recall = len(set(found) & set(q['relevant'])) / len(q['relevant'])
            values.append(recall)
            print(q['id'], q['split'], found, 'recall@3=', recall)
        else:
            print(q['id'], 'unanswerable; returned=', found)
        # Ни один найденный документ не принадлежит чужой команде.
        assert all(d['tenant'] in ('public', q['tenant']) for d, _ in hits)
    print('Toy aggregate recall (split-specific reports belong in exercises):', sum(values) / len(values))
