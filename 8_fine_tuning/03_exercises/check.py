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
# m.answer_labels(...)
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


assert m.answer_labels([1, 2], [3, 4], 6) == [-100, -100, 3, 4, -100, -100]
assert m.lora_parameters(128, 64, 4) == 768

# lambda: — короткая функция без имени; её вызовет expect_value_error.
expect_value_error(lambda: m.answer_labels([1], [], 3))      # пустой ответ
expect_value_error(lambda: m.answer_labels([1], [2], 1))     # не хватает длины
expect_value_error(lambda: m.answer_labels([1], [True], 3))  # bool вместо ID
expect_value_error(lambda: m.lora_parameters(1, 2, 0))       # rank = 0

mode = 'answers' if options.answers else 'student'
print('PASS:', source.parent.parent.name, mode)
