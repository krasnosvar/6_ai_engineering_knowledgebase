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
# m.validate_action(...)
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


good_action = {'tool': 'read_metrics', 'arguments': {'service': 'demo'}}
assert m.validate_action(good_action) == {'service': 'demo'}

bad_actions = (
    # чужой инструмент
    {'tool': 'shell', 'arguments': {}},
    # чужой сервис
    {'tool': 'read_metrics', 'arguments': {'service': 'private'}},
    # лишнее поле
    {'tool': 'read_metrics', 'arguments': {'service': 'demo', 'cmd': 'x'}},
    # не словарь
    [],
)
for a in bad_actions:
    # `lambda a=a:` фиксирует ТЕКУЩЕЕ a в момент создания функции. Без `a=a`
    # лямбда брала бы a в момент вызова; здесь вызов сразу, но в отложенных
    # вызовах все лямбды увидели бы последнее значение цикла.
    expect_value_error(lambda a=a: m.validate_action(a))

assert m.may_continue(0, 2, False)
assert not m.may_continue(2, 2, False)   # бюджет исчерпан
assert not m.may_continue(0, 2, True)    # задачу отменили
expect_value_error(lambda: m.may_continue(-1, 2, False))

mode = 'answers' if options.answers else 'student'
print('PASS:', source.parent.parent.name, mode)
