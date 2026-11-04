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

# Перестановка A/B — данные из урока о судье.
ab = ['A', 'A', 'B', 'A', 'A', 'B', 'A', 'A', 'B', 'A']  # A показан первым
ba = ['B', 'A', 'B', 'B', 'A', 'B', 'B', 'A', 'B', 'B']  # B показан первым
assert m.position_bias_check(ab, ba) == {
    'consistent': 6, 'inconsistent': 4, 'first_wins': 14}
assert m.position_bias_check(['A'], ['A']) == {
    'consistent': 1, 'inconsistent': 0, 'first_wins': 1}
expect_value_error(lambda: m.position_bias_check([], []))
expect_value_error(lambda: m.position_bias_check(['A'], ['A', 'B']))
expect_value_error(lambda: m.position_bias_check(['A'], ['tie']))

# Калибровка: 9 из 10 хороших одобрены, 4 из 10 плохих тоже.
human = [1] * 10 + [0] * 10
judge = [1] * 9 + [0] + [1] * 4 + [0] * 6
r = m.judge_calibration(human, judge)
assert r['agreement'] == 0.75 and r['false_approvals'] == 4
assert abs(r['kappa'] - 0.5) < 1e-12
r = m.judge_calibration([1, 0], [0, 1])  # всегда не согласны
assert r['agreement'] == 0 and r['kappa'] == -1 and r['false_approvals'] == 1
expect_value_error(lambda: m.judge_calibration([1, 1], [1, 1]))  # p_e = 1
expect_value_error(lambda: m.judge_calibration([1, 0], [1]))
expect_value_error(lambda: m.judge_calibration([1, 2], [1, 0]))
expect_value_error(lambda: m.judge_calibration([True, 0], [1, 0]))
expect_value_error(lambda: m.judge_calibration([], []))

# Проверка вызова инструмента кодом, а не моделью.
allow = ['search', 'create_ticket', 'send_email']
confirm = ['send_email']
call = {'tool': 'search', 'args': {'q': 'atlas'}}
assert m.guard_tool_call(call, allow, confirm) == 'allow'
assert m.guard_tool_call({'tool': 'send_email'}, allow, confirm) == 'confirm'
assert m.guard_tool_call({'tool': 'delete_all'}, allow, confirm) == 'deny'
assert m.guard_tool_call({'tool': 'Search'}, allow, confirm) == 'deny'
assert m.guard_tool_call({'tool': 'search'}, [], []) == 'deny'
expect_value_error(lambda: m.guard_tool_call({'args': {}}, allow, confirm))
expect_value_error(lambda: m.guard_tool_call({'tool': 1}, allow, confirm))
expect_value_error(lambda: m.guard_tool_call({'tool': 'search'}, [], confirm))

mode = 'answers' if options.answers else 'student'
print('PASS:', source.parent.parent.name, mode)
