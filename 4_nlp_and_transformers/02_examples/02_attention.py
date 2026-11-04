import numpy as np

# Три позиции по 2 числа. Строка — вектор одной позиции.
x = np.array([[1., 0.], [0., 1.], [1., 1.]])


def attention(x):
    # Проекции Q, K, V взяты единичными (Q=K=V=x), чтобы изолировать
    # маскирование и взвешенное усреднение.
    scores = x @ x.T / np.sqrt(x.shape[1])  # форма (T, T)

    # Causal mask: элементы выше диагонали (j > i) — это будущее, ставим -inf.
    scores[np.triu_indices(len(x), 1)] = -np.inf

    # Устойчивый softmax по каждой строке: вычитаем максимум строки.
    scores -= scores.max(axis=-1, keepdims=True)
    weights = np.exp(scores)
    weights /= weights.sum(axis=-1, keepdims=True)

    return weights, weights @ x


weights, out = attention(x)
print('weights:', weights, '\noutput:', out)

# Проверка 1: каждая строка весов — доли, их сумма равна 1.
assert np.allclose(weights.sum(axis=-1), 1)
# Проверка 2: веса на будущие позиции нулевые.
assert np.allclose(np.triu(weights, 1), 0)
# Проверка 3: меняем последний токен — выходы первых двух позиций не меняются.
changed = x.copy()
changed[2] = [100., -100.]
assert np.allclose(out[:2], attention(changed)[1][:2])
print('Future-token invariance: PASS')
