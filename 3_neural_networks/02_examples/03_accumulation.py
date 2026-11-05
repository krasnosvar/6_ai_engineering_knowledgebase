"""Накопление градиента из неравных частей batch.

Как масштабировать loss частей, чтобы градиент совпал с целым batch.
"""
import torch
from torch import nn

torch.manual_seed(42)
torch.set_num_threads(2)

x = torch.randn(5, 3)                 # 5 примеров по 3 признака
y = torch.tensor([0, 1, 0, 1, 1])

full = nn.Linear(3, 2)
parts = nn.Linear(3, 2)
parts.load_state_dict(full.state_dict())   # одинаковые стартовые веса

# 1. Градиент по всему batch сразу: средний loss по 5 примерам.
nn.functional.cross_entropy(full(x), y).backward()

# 2. Тот же batch частями по 2 и 3 примера, без zero_grad между ними.
#    Сумма loss каждой части делится на ОБЩЕЕ число примеров (5).
for start, end in [(0, 2), (2, 5)]:
    part_loss = nn.functional.cross_entropy(
        parts(x[start:end]), y[start:end], reduction='sum')
    (part_loss / len(x)).backward()      # градиенты складываются в .grad

for p, q in zip(full.parameters(), parts.parameters()):
    assert torch.allclose(p.grad, q.grad, atol=1e-7)
print('Неравные части дают тот же градиент, что и целый batch: PASS')
print('Не усредняй средние частей поровну, если их размеры различаются.')
