import math


def softmax(values):
    # Пустой список или нечисловые бесконечности/NaN делают результат бессмысленным.
    if not values:
        raise ValueError('Finite nonempty logits required')
    for v in values:
        # math.isfinite(v) ложно для inf, -inf и NaN.
        if not math.isfinite(v):
            raise ValueError('Finite nonempty logits required')

    # Вычитаем максимум: exp(1000) переполнит float, а exp(1000-1000)=exp(0)=1.
    # Доли не меняются: exp(a-c)/exp(b-c) = exp(a)/exp(b).
    top = max(values)
    exps = []
    for v in values:
        exps.append(math.exp(v - top))

    total = sum(exps)
    result = []
    for e in exps:
        result.append(e / total)
    return result


def causal_allowed(length):
    # type(...) is not int, а не isinstance: bool — подкласс int,
    # и isinstance(True, int) вернул бы True, пропустив causal_allowed(True).
    if type(length) is not int or length < 1:
        raise ValueError('Positive integer length required')

    rows = []
    for i in range(length):
        row = []
        for j in range(length):
            # Позиция i видит себя и прошлое (j <= i), но не будущее.
            row.append(j <= i)
        rows.append(row)
    return rows
