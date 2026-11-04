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


assert m.iou((0, 0, 2, 2), (0, 0, 2, 2)) == 1
assert m.iou((0, 0, 1, 1), (2, 2, 3, 3)) == 0
assert abs(m.iou((0, 0, 2, 2), (1, 1, 3, 3)) - 1 / 7) < 1e-12
expect_value_error(lambda: m.iou((0, 0, 0, 1), (0, 0, 1, 1)))

t = {'a': {'x': 1}, 'b': {'x': 2}}
assert m.document_accuracy(t, {'a': {'x': 1}}, ['x']) == .5
assert m.document_accuracy({'a': {'x': None}}, {'a': {}}, ['x']) == 0
expect_value_error(lambda: m.document_accuracy({}, {}, ['x']))

mode = 'answers' if options.answers else 'student'
print('PASS:', source.parent.parent.name, mode)
