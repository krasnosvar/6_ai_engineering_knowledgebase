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

# --- span_tree_summary: trace RAG-запроса из урока ---
# (id, parent, start, end); время в миллисекундах.
trace = [
    ('request', None, 0, 2905),
    ('retrieve', 'request', 0, 110),
    ('embed_query', 'retrieve', 0, 20),
    ('vector_search', 'retrieve', 20, 110),
    ('llm.generate', 'request', 110, 2890),
    ('check_citations', 'request', 2890, 2905),
]
assert m.span_tree_summary(trace) == {
    'request': (2905, 0),
    'retrieve': (110, 0),
    'embed_query': (20, 20),
    'vector_search': (90, 90),
    'llm.generate': (2780, 2780),
    'check_citations': (15, 15),
}
# Вопрос 1 урока: 3000 мс у родителя, 1200 мс у детей — 1800 вне spans.
gap = [('request', None, 0, 3000), ('a', 'request', 100, 700),
       ('b', 'request', 900, 1500)]
assert m.span_tree_summary(gap)['request'] == (3000, 1800)
assert m.span_tree_summary([]) == {}
bad_traces = (
    [('a', None, 0, 10), ('a', None, 0, 10)],        # повтор id
    [('a', None, 0, 10), ('b', 'x', 0, 5)],          # неизвестный родитель
    [('a', 'a', 0, 10)],                             # сам себе родитель
    [('a', None, 10, 5)],                            # конец раньше начала
    [('a', None, 0, 10), ('b', 'a', 5, 15)],         # вышел за родителя
    [('a', None, 0, 10), ('b', 'a', 0, 8), ('c', 'a', 2, 10)],  # пересечение
    [('a', None, 0.5, 10)],                          # не целое время
    [('a', None, 0)],                                # не 4 поля
)
for t in bad_traces:
    expect_value_error(lambda t=t: m.span_tree_summary(t))

# --- redact: ключи API и адреса почты ---
assert m.redact('ключ sk-abc123 не работает') == 'ключ sk-*** не работает'
assert m.redact('sk-proj-A_1 и sk-x9') == 'sk-*** и sk-***'
assert m.redact('пишите на ops.team+llm@example.com, ответим') == (
    'пишите на <email>, ответим')
# Похожее, но не секрет: остаётся как есть.
assert m.redact('task-42 готов; просто sk- без ключа') == (
    'task-42 готов; просто sk- без ключа')
assert m.redact('') == ''
expect_value_error(lambda: m.redact(None))
expect_value_error(lambda: m.redact(b'sk-abc'))

mode = 'answers' if options.answers else 'student'
print('PASS:', source.parent.parent.name, mode)
