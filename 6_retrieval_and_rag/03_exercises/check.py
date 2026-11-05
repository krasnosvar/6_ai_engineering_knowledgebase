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

# Recall ANN относительно точного перебора: из top-3 {d1, d2, d3}
# приближённый поиск нашёл d1 и d3.
exact = ['d1', 'd2', 'd3', 'd4']
assert abs(m.ann_recall_at_k(['d3', 'd1', 'd9'], exact, 3) - 2 / 3) < 1e-12
assert m.ann_recall_at_k(['d4', 'd3', 'd2', 'd1'], exact, 4) == 1.0
assert m.ann_recall_at_k(['d1'], exact, 2) == 0.5   # ANN вернул меньше k
assert m.ann_recall_at_k([], exact, 1) == 0.0
expect_value_error(lambda: m.ann_recall_at_k(['d1'], exact, 0))
expect_value_error(lambda: m.ann_recall_at_k(['d1'], exact, True))
expect_value_error(lambda: m.ann_recall_at_k(['d1'], exact, 5))  # мало exact
expect_value_error(lambda: m.ann_recall_at_k(['d1', 'd1'], exact, 2))

# IVF: три ячейки; документ i лежит в ячейке cell[i].
centers = [[1, 0], [0, 1], [-1, 0]]
cell = [0, 1, 2, 0, 1]
assert m.ivf_candidates([0.9, 0.1], centers, cell, 1) == [0, 3]
assert m.ivf_candidates([0.9, 0.1], centers, cell, 2) == [0, 1, 3, 4]
assert m.ivf_candidates([0.9, 0.1], centers, cell, 3) == [0, 1, 2, 3, 4]
# Равное сходство с центрами 0 и 1: выбирается меньший номер.
assert m.ivf_candidates([0.5, 0.5], centers, cell, 1) == [0, 3]
assert m.ivf_candidates([-1, 0], centers, [0, 1], 1) == []  # пустая ячейка
assert m.ivf_candidates([1, 0], centers, [], 1) == []  # нет документов
expect_value_error(lambda: m.ivf_candidates([1, 0], centers, cell, 0))
expect_value_error(lambda: m.ivf_candidates([1, 0], centers, cell, 4))
expect_value_error(lambda: m.ivf_candidates([1, 0, 0], centers, cell, 1))
expect_value_error(lambda: m.ivf_candidates([1, 0], centers, [0, 5], 1))
expect_value_error(lambda: m.ivf_candidates([1, 0], centers, [0.5], 1))

mode = 'answers' if options.answers else 'student'
print('PASS:', source.parent.parent.name, mode)
