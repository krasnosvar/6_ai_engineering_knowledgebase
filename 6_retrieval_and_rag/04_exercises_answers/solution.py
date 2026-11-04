import numpy as np


def authorized_topk(rows, tenant, k):
    # type(k) is not int, а не isinstance: bool — подкласс int (True == 1).
    if type(k) is not int or k < 1:
        raise ValueError('Positive k required')

    # Сначала права доступа, потом top-k: иначе чужие документы с высоким score
    # вытеснят из первых k допустимые документы своей команды.
    visible = []
    for row in rows:
        if row['tenant'] in ('public', tenant):
            visible.append(row)

    # sorted(..., key=функция) сортирует по значению, которое функция вернула
    # для каждой строки. lambda r: (...) — короткая безымянная функция.
    # Ключ (-score, id): минус даёт убывание score, id разрешает равенство.
    ordered = sorted(visible, key=lambda r: (-r['score'], r['id']))

    result = []
    for row in ordered[:k]:
        result.append(row['id'])
    return result


def rrf(rankings, k=60):
    if k <= 0:
        raise ValueError('Positive k required')
    result = {}
    for ranking in rankings:
        # set убирает повторы: если длина уменьшилась, какой-то ID встретился дважды.
        if len(set(ranking)) != len(ranking):
            raise ValueError('Duplicate ID in ranking')
        # enumerate(ranking, 1) нумерует с 1: (1, 'a'), (2, 'b'), ...
        for rank, doc in enumerate(ranking, 1):
            # result.get(doc, 0): текущая сумма документа или 0, если его ещё нет.
            result[doc] = result.get(doc, 0) + 1 / (k + rank)
    return result


def ann_recall_at_k(approx_ids, exact_ids, k):
    """Доля настоящих top-k (точный перебор), которую вернул ANN."""
    if type(k) is not int or k < 1:
        raise ValueError('Positive k required')
    if len(exact_ids) < k:
        raise ValueError('exact_ids must contain at least k IDs')
    for ids in (approx_ids, exact_ids):
        if len(set(ids)) != len(ids):
            raise ValueError('Duplicate ID in ranking')
    # Сравниваем только первые k каждого списка. ANN может вернуть меньше
    # k (например, после фильтра) — недостающие просто не совпадут.
    found = set(approx_ids[:k]) & set(exact_ids[:k])  # & — пересечение
    return len(found) / k


def ivf_candidates(query, centers, cell, n_probe):
    """ID документов из n_probe ячеек, чьи центры ближе всего к запросу."""
    # np.asarray превращает списки в массивы NumPy; массивы не меняет.
    query = np.asarray(query, dtype=float)
    centers = np.asarray(centers, dtype=float)
    cell = np.asarray(cell)
    if centers.ndim != 2 or query.shape != (centers.shape[1],):
        raise ValueError('query length must match center length')
    n_cells = centers.shape[0]
    if type(n_probe) is not int or not 1 <= n_probe <= n_cells:
        raise ValueError('n_probe must be from 1 to number of cells')
    if cell.ndim != 1 or cell.min() < 0 or cell.max() >= n_cells:
        raise ValueError('cell must hold a center index for each document')

    # Векторы нормированы, поэтому сходство — скалярное произведение:
    # centers @ query — по одному числу на каждый центр.
    scores = centers @ query
    # argsort(-scores) упорядочивает центры от ближнего к дальнему;
    # kind='stable' при равенстве оставляет меньший номер раньше —
    # результат не зависит от случая.
    near = np.argsort(-scores, kind='stable')[:n_probe]
    # np.isin(cell, near) — True для документов из выбранных ячеек,
    # np.flatnonzero — номера позиций, где стоит True.
    return np.flatnonzero(np.isin(cell, near)).tolist()
