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
# m.rrf(...)
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
    {'id': 'private', 'tenant': 'b', 'score': 10},
    {'id': 'own', 'tenant': 'a', 'score': 2},
    {'id': 'pub', 'tenant': 'public', 'score': 1},
]
# Чужой документ отбрасывается до top-k, даже с лучшим score.
assert m.authorized_topk(rows, 'a', 1) == ['own']
assert m.authorized_topk(rows, 'c', 3) == ['pub']

# RRF: 'b' второй в первом списке и первый во втором.
r = m.rrf([['a', 'b'], ['b', 'c']])
assert abs(r['b'] - (1 / 62 + 1 / 61)) < 1e-12
assert r['b'] > r['a'] and m.rrf([]) == {}

expect_value_error(lambda: m.rrf([['a', 'a']]))  # повтор в одном списке
expect_value_error(lambda: m.authorized_topk(rows, 'a', 0))

mode = 'answers' if options.answers else 'student'
print('PASS:', source.parent.parent.name, mode)
