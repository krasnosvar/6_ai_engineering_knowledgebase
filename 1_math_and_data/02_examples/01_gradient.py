"""CPU, stdlib: проверить формулу градиента и обучить модель y = 2x + 1.

Формулы — из урока 1_math_and_data/01_theory/02_gradients.md.
"""
import math


def loss(w, b, x, y):
    """MSE: средний квадрат ошибки по всем примерам."""
    squared_errors = [(w * a + b - t) ** 2 for a, t in zip(x, y)]
    return sum(squared_errors) / len(x)


def gradient(w, b, x, y):
    """Пара производных MSE: (dL/dw, dL/db)."""
    errors = [w * a + b - t for a, t in zip(x, y)]
    dw = 2 * sum(e * a for e, a in zip(errors, x)) / len(x)
    db = 2 * sum(errors) / len(x)
    return dw, db


def main():
    # Пять точек, лежащих точно на прямой y = 2x + 1.
    x = [-2.0, -1.0, 0.0, 1.0, 2.0]
    y = [2 * a + 1 for a in x]

    w = 0.0
    b = 0.0

    # Проверка формулы: сравниваем с численной производной.
    eps = 1e-5
    analytic = gradient(w, b, x, y)[0]
    numeric = (loss(w + eps, b, x, y) - loss(w - eps, b, x, y)) / (2 * eps)
    assert math.isclose(analytic, numeric, abs_tol=1e-7)

    # Градиентный спуск: 100 шагов против градиента со скоростью 0.1.
    learning_rate = 0.1
    before = loss(w, b, x, y)
    for _ in range(100):
        dw, db = gradient(w, b, x, y)
        w -= learning_rate * dw
        b -= learning_rate * db

    print(f"градиент по w: формула={analytic:.5f}, численно={numeric:.5f}")
    print(f"ошибка {before:.6f} -> {loss(w, b, x, y):.9f}; w={w:.5f}, b={b:.5f}")
    assert abs(w - 2) < 1e-5 and abs(b - 1) < 1e-5


if __name__ == "__main__":
    main()
