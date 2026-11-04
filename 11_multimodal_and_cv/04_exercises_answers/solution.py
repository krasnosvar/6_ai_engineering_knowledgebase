import math


def area(box):
    x1, y1, x2, y2 = box
    return (x2 - x1) * (y2 - y1)


def iou(a, b):
    for box in (a, b):
        if len(box) != 4 or not all(math.isfinite(v) for v in box):
            raise ValueError('Invalid rectangle')
        x1, y1, x2, y2 = box
        if x2 <= x1 or y2 <= y1:
            raise ValueError('Invalid rectangle')

    # Пересечение по каждой оси: от большего левого края до меньшего правого.
    # Если рамки не пересекаются, разность отрицательна — обрезаем до нуля.
    overlap_x = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    overlap_y = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    intersection = overlap_x * overlap_y

    # Объединение = A + B − пересечение (иначе пересечение посчитано дважды).
    return intersection / (area(a) + area(b) - intersection)


def document_accuracy(truth, pred, fields):
    if not truth or not fields:
        raise ValueError('Truth and fields required')

    correct = 0
    for doc_id, true_row in truth.items():
        if doc_id not in pred:
            continue  # пропущенный документ — ошибка
        predicted_row = pred[doc_id]
        all_fields_match = True
        for k in fields:
            # Поле должно присутствовать в обоих словарях и совпасть.
            # Отсутствующее поле — не то же самое, что явный None.
            if k not in true_row or k not in predicted_row or predicted_row[k] != true_row[k]:
                all_fields_match = False
                break
        if all_fields_match:
            correct += 1
    return correct / len(truth)
