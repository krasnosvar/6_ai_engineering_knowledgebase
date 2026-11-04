import math


def mse_gradient(w, b, x, y):
    """Производные MSE по w и b для модели y_hat = w*x + b."""
    if not x or len(x) != len(y):
        raise ValueError("Нужны непустые списки одинаковой длины")
    errors = [w * a + b - t for a, t in zip(x, y)]
    dw = 2 * sum(e * a for e, a in zip(errors, x)) / len(x)
    db = 2 * sum(errors) / len(x)
    return dw, db


def cosine(a, b):
    """Косинус угла между векторами: скалярное произведение / произведение длин."""
    if not a or len(a) != len(b):
        raise ValueError("Нужны непустые векторы одинаковой длины")
    length_a = math.sqrt(sum(v * v for v in a))
    length_b = math.sqrt(sum(v * v for v in b))
    if length_a == 0 or length_b == 0:
        raise ValueError("У нулевого вектора нет направления")
    dot = sum(p * q for p, q in zip(a, b))
    return dot / (length_a * length_b)
