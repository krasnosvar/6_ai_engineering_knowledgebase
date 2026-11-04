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

mode = 'answers' if options.answers else 'student'
print('PASS:', source.parent.parent.name, mode)
