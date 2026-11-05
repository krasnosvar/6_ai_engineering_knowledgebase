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
# m.masked_mean(...)
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


import torch
from torch import nn

torch.manual_seed(42)
torch.set_num_threads(2)

# Третья позиция — padding (маска 0), её 99 не должны попасть в среднее.
h = torch.tensor([[[1., 3.], [3., 5.], [99., 99.]]])
mask = torch.tensor([[1, 1, 0]])
assert torch.allclose(m.masked_mean(h, mask), torch.tensor([[2., 4.]]))
expect_value_error(lambda: m.masked_mean(h, torch.zeros(1, 3)))

# Две одинаковые модели с одинаковыми оптимизаторами.
a = nn.Linear(2, 2)
b = nn.Linear(2, 2)
b.load_state_dict(a.state_dict())
x = torch.tensor([[1., 0.], [0., 1.]])
y = torch.tensor([0, 1])
oa = torch.optim.SGD(a.parameters(), lr=.1)
ob = torch.optim.SGD(b.parameters(), lr=.1)

# Старые градиенты в .grad не должны влиять на шаг: one_step обнуляет их.
for p in a.parameters():
    p.grad = torch.ones_like(p) * 100
a.eval()
value = m.one_step(a, oa, x, y)
m.one_step(b, ob, x, y)
assert isinstance(value, float) and value > 0
assert a.training
# После шага веса обеих моделей должны совпасть.
assert all(torch.allclose(p, q) for p, q in zip(a.parameters(), b.parameters()))

mode = 'answers' if options.answers else 'student'
print('PASS:', source.parent.parent.name, mode)
