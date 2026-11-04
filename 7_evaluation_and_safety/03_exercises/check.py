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
# m.slice_accuracy(...)
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


rows = [
    {'slice': 'rare', 'correct': False},
    {'slice': 'normal', 'correct': True},
    {'slice': 'normal', 'correct': False},
]
assert m.slice_accuracy(rows) == {'rare': 0.0, 'normal': 0.5}
assert m.citations_allowed(['a'], ['a', 'b'])
assert not m.citations_allowed(['private'], ['public'])
assert m.citations_allowed([], [])

# lambda: — короткая функция без имени; её вызовет expect_value_error.
expect_value_error(lambda: m.slice_accuracy([]))
expect_value_error(lambda: m.slice_accuracy([{'slice': 'a', 'correct': 'yes'}]))

mode = 'answers' if options.answers else 'student'
print('PASS:', source.parent.parent.name, mode)
