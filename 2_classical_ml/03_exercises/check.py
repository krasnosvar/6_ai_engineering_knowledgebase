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
# m.binary_metrics(...)
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


r = m.binary_metrics([1, 1, 0, 0], [1, 0, 1, 0])
assert r == {'precision': .5, 'recall': .5, 'f1': .5}
# Ни одного предсказанного положительного: метрики 0, а не деление на ноль.
assert m.binary_metrics([0, 1], [0, 0]) == {
    'precision': 0., 'recall': 0., 'f1': 0.}
assert m.binary_metrics([1, 0], [1, 0])['f1'] == 1

# Общие группы в train и test — признак утечки.
assert m.group_overlap(['a', 'b'], ['b', 'c']) == {'b'}
assert m.group_overlap(['a'], ['b']) == set()

expect_value_error(lambda: m.binary_metrics([], []))      # пустой вход
expect_value_error(lambda: m.binary_metrics([1], [1, 0]))  # разная длина
expect_value_error(lambda: m.binary_metrics([2], [1]))     # метка не 0/1

mode = 'answers' if options.answers else 'student'
print('PASS:', source.parent.parent.name, mode)
