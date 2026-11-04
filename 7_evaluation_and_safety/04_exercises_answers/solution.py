def slice_accuracy(rows):
    """Доля верных ответов (accuracy) отдельно для каждого среза."""
    if not rows:
        raise ValueError('Nonempty evaluation set required')
    counts = {}     # срез -> сколько строк
    successes = {}  # срез -> сколько верных
    for row in rows:
        # Точная проверка типа: отсекает и строку 'yes', и число 1,
        # хотя в Python 1 == True. Иначе 1 молча посчиталось бы успехом.
        if type(row['correct']) is not bool:
            raise ValueError('correct must be bool')
        key = row['slice']
        counts[key] = counts.get(key, 0) + 1          # .get: 0, если ключа ещё нет
        successes[key] = successes.get(key, 0) + row['correct']  # True = 1, False = 0
    return {key: successes[key] / n for key, n in counts.items()}


def citations_allowed(cited_ids, context_ids):
    """True, если каждый процитированный ID был в переданном контексте."""
    # set(a) <= set(b) — «каждый элемент a есть в b» (подмножество).
    return set(cited_ids) <= set(context_ids)
