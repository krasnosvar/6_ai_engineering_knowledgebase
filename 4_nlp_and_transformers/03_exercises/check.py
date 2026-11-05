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
# m.softmax(...)
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


# Большие числа не должны переполнять exp (нужен сдвиг на максимум).
a = m.softmax([1000., 1000.])
assert a == [.5, .5]
b = m.softmax([-1000., 0., 1000.])
assert abs(sum(b) - 1) < 1e-12 and b[-1] > .999

# True — позиция может смотреть на столбец (себя и прошлое).
assert m.causal_allowed(3) == [
    [True, False, False],
    [True, True, False],
    [True, True, True],
]

expect_value_error(lambda: m.softmax([]))
expect_value_error(lambda: m.softmax([float('inf')]))
expect_value_error(lambda: m.softmax([float('-inf')]))
expect_value_error(lambda: m.softmax([float('nan')]))
expect_value_error(lambda: m.causal_allowed(0))
expect_value_error(lambda: m.causal_allowed(True))  # bool — не число позиций
expect_value_error(lambda: m.causal_allowed(1.5))

mode = 'answers' if options.answers else 'student'
print('PASS:', source.parent.parent.name, mode)
