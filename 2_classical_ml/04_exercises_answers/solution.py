def binary_metrics(truth, pred):
    """Precision, recall и F1 для бинарных меток 0/1."""
    if not truth or len(truth) != len(pred):
        raise ValueError('Nonempty paired binary labels required')
    if any(v not in (0, 1) for v in truth + pred):
        raise ValueError('Nonempty paired binary labels required')

    pairs = list(zip(truth, pred))
    tp = sum(1 for t, p in pairs if t == 1 and p == 1)  # верно нашли
    fp = sum(1 for t, p in pairs if t == 0 and p == 1)  # ложная тревога
    fn = sum(1 for t, p in pairs if t == 1 and p == 0)  # пропуск

    # При нулевом знаменателе метрика не определена; договоримся считать 0.
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    if precision + recall:
        f1 = 2 * precision * recall / (precision + recall)
    else:
        f1 = 0.0
    return {'precision': precision, 'recall': recall, 'f1': f1}


def group_overlap(train_groups, test_groups):
    """Группы (например, ID клиентов), попавшие и в train, и в test."""
    return set(train_groups) & set(test_groups)
