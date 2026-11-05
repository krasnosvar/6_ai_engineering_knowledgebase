"""Алгебра LoRA на случайных матрицах: без обучения, только проверка формул."""
import numpy as np

# Пример урока на двух числах: W единичная, r = 1.
w_small = np.eye(2)
a_small = np.array([[0.1, 0.2]])   # A: форма (1, 2)
b_small = np.array([[1.0], [2.0]])  # B: форма (2, 1)
x_small = np.array([2.0, 3.0])
hand = w_small @ x_small + b_small @ (a_small @ x_small)
assert np.allclose(hand, [2.8, 4.6])
print('Lesson example output:', hand)

# Размеры как в уроке: W (64, 128), r = 4.
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
# Поправка B·A получена через r = 4 промежуточных координат: ранг не больше 4.
assert np.linalg.matrix_rank(b @ a) <= rank

print('Full matrix parameters:', w.size, 'adapter parameters:', a.size + b.size)
print('Algebra only; real training of A and B on CPU is 03_tiny_adapter.py.')
