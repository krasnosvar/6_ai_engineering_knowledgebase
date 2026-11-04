"""Проверка упражнения. Без флага проверяет task.py, с --answers — эталон."""
import argparse
import importlib.util
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--answers', action='store_true')
options = parser.parse_args()

folder = Path(__file__).resolve().parent
if options.answers:
    source = folder.parent / '04_exercises_answers/solution.py'
else:
    source = folder / 'task.py'

# Загружаем файл с решением как модуль m, чтобы вызывать его функции:
# m.cosine(...)
spec = importlib.util.spec_from_file_location('student', source)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def expect_value_error(fn):
    """Вызывает fn() и требует, чтобы она бросила ValueError."""
    try:
        fn()
    except ValueError:
        return  # ожидаемая ошибка — проверка пройдена
    raise AssertionError('Expected ValueError')


# Градиент MSE для w=0, b=0 и в точке минимума (там он нулевой).
assert m.mse_gradient(0, 0, [1, 2], [3, 5]) == (-13., -8.)
assert m.mse_gradient(2, 1, [1, 2], [3, 5]) == (0., 0.)

# Перпендикулярные векторы дают 0, противоположные — -1.
assert abs(m.cosine([1, 0], [0, 1])) < 1e-12
assert abs(m.cosine([1, 0], [-2, 0]) + 1) < 1e-12

# Пустые векторы, нулевой вектор и разная длина — ошибка входа.
for args in [([], []), ([0, 0], [1, 2]), ([1], [1, 2])]:
    # `args=args` фиксирует текущее значение цикла внутри lambda.
    expect_value_error(lambda args=args: m.cosine(*args))
expect_value_error(lambda: m.mse_gradient(0, 0, [1], []))

# Softmax с температурой: числа из таблицы урока 05.
for t, expected in [(0.5, [0.867, 0.117, 0.016]),
                    (1, [0.665, 0.245, 0.090]),
                    (2, [0.506, 0.307, 0.186])]:
    probs = m.softmax_with_temperature([2, 1, 0], t)
    assert [round(p, 3) for p in probs] == expected, (t, probs)
    assert abs(sum(probs) - 1) < 1e-12

# Сдвиг всех logits на 1000 не меняет вероятности и не должен вызывать
# переполнение: наивный math.exp(1000) бросает OverflowError.
shifted = m.softmax_with_temperature([1000, 999, 998], 1)
assert [round(p, 3) for p in shifted] == [0.665, 0.245, 0.090]
# Один токен получает всю вероятность.
assert m.softmax_with_temperature([5], 0.1) == [1.0]
for args in [([], 1), ([1, 2], 0), ([1, 2], -1)]:
    expect_value_error(lambda args=args: m.softmax_with_temperature(*args))

# Perplexity: пример урока 05 и уверенная модель (все p = 1).
assert abs(m.perplexity([0.5, 0.25, 0.8]) - 10 ** (1 / 3)) < 1e-9
assert m.perplexity([1, 1, 1]) == 1.0
# Четыре равновероятных варианта на каждом шаге — perplexity 4.
assert abs(m.perplexity([0.25, 0.25]) - 4) < 1e-9
for probs in [[], [0.5, 0], [1.2], [-0.1]]:
    expect_value_error(lambda probs=probs: m.perplexity(probs))

mode = 'answers' if options.answers else 'student'
print('PASS:', source.parent.parent.name, mode)
