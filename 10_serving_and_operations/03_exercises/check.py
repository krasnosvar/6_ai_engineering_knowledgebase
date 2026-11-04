"""Проверка задания. Без флага проверяет task.py, с --answers — эталон."""
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

# Загружаем выбранный файл как модуль m, чтобы вызывать его функции.
spec = importlib.util.spec_from_file_location('student', source)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def expect_value_error(fn):
    try:
        fn()
    except ValueError:
        return
    raise AssertionError('Expected ValueError')


assert m.kv_bytes(1, 1, 1, 1, 1, 2) == 4
assert m.kv_bytes(2, 3, 4, 5, 6, 2) == 2880

x = [20, 1, 1, 1, 1]
assert m.nearest_rank(x, .95) == 20
assert x[0] == 20, 'входной список нельзя сортировать на месте'
assert m.nearest_rank(x, .5) == 1

expect_value_error(lambda: m.nearest_rank([], .95))
expect_value_error(lambda: m.nearest_rank([1], 0))
expect_value_error(lambda: m.kv_bytes(1, 1, 0, 1, 1, 2))

mode = 'answers' if options.answers else 'student'
print('PASS:', source.parent.parent.name, mode)
