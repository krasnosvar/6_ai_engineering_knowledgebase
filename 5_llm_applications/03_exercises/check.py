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
# m.parse_ticket(...)
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


assert m.parse_ticket('{"ticket_id":"a","label":"access"}')['label'] == 'access'

bad_answers = (
    '{}',                                            # нет полей
    '[]',                                            # не объект
    '{"ticket_id":1,"label":"access"}',              # ID не строка
    '{"ticket_id":"a","label":"x"}',                 # чужая категория
    '{"ticket_id":"a","label":"access","extra":1}',  # лишнее поле
    'prose',                                         # не JSON
)
for s in bad_answers:
    # `s=s` фиксирует текущее значение цикла внутри lambda.
    expect_value_error(lambda s=s: m.parse_ticket(s))

# Бюджет контекста: 100 - 60 - 20 = 20 токенов.
assert m.remaining_tokens(100, 60, 20) == 20
expect_value_error(lambda: m.remaining_tokens(100, 99, 2))
expect_value_error(lambda: m.remaining_tokens(100, True, 1))

mode = 'answers' if options.answers else 'student'
print('PASS:', source.parent.parent.name, mode)
