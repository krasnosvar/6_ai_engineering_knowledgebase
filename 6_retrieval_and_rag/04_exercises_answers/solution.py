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
