"""Алгебра LoRA на случайных матрицах: без обучения, только проверка формул."""
import numpy as np

rng = np.random.default_rng(42)
out_dim, in_dim, rank = 64, 128, 4

w = rng.normal(size=(out_dim, in_dim))   # базовая матрица слоя, её не обучаем
a = rng.normal(size=(rank, in_dim))      # A: случайный старт
b = np.zeros((out_dim, rank))            # B: нули, поэтому B@A = 0
x = rng.normal(size=(in_dim,))           # один входной вектор

# С нулевой B адаптер ничего не меняет: выход совпадает с базовым.
assert np.allclose(w @ x, (w + b @ a) @ x)

# После «обучения» B ненулевая. Масштаб поправки — alpha / rank.
b = rng.normal(size=(out_dim, rank))
alpha = 8
scale = alpha / rank
# Слить поправку в матрицу или посчитать её отдельно — одно и то же:
# (W + s·B·A)·x == W·x + s·B·(A·x). Второй способ не создаёт большую матрицу.
assert np.allclose((w + scale * b @ a) @ x, w @ x + scale * b @ (a @ x))

print('Full matrix parameters:', w.size, 'adapter parameters:', a.size + b.size)
print('Algebra only; real training of A and B on CPU is 03_tiny_adapter.py.')
