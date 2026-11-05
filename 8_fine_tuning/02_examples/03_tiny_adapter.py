"""Настоящее обучение low-rank матриц на синтетической регрессии без весов.

Синтаксис PyTorch (тензоры, nn.Module, оптимизатор) разобран в уроке
3_neural_networks/01_theory/02_pytorch_basics.md.
"""
import torch
from torch import nn

torch.manual_seed(42)
torch.set_num_threads(2)

# Маленькие размеры, чтобы обучение шло секунды: W (4, 8), r = 2. Задачу
# строим так, чтобы ответ существовал: нужная поправка имеет ранг 2.
in_dim, out_dim, rank = 8, 4, 2
base = torch.randn(out_dim, in_dim)        # «предобученная» матрица W
true_delta = torch.randn(out_dim, rank) @ torch.randn(rank, in_dim)
# Ранг адаптера задаём отдельно от ранга нужной поправки, чтобы менять его
# в эксперименте, не меняя саму задачу.
adapter_rank = 2
x = torch.randn(160, in_dim)               # 160 входов: 120 train + 40 test
# Строки x — отдельные примеры, поэтому x @ M.T — это M × x для каждой строки.
y = x @ (base + true_delta).T              # правильные ответы: W + поправка


# Своя модель nn.Module: в __init__ объявляем части, в forward — вычисление.
class Adapted(nn.Module):
    def __init__(self):
        super().__init__()  # обязательная настройка базового класса nn.Module
        # register_buffer: тензор хранится в модели, но НЕ обучается —
        # так мы замораживаем базовую матрицу.
        self.register_buffer('base', base.clone())
        # nn.Parameter: тензор, который оптимизатор будет менять.
        self.a = nn.Parameter(torch.randn(adapter_rank, in_dim) * 0.1)
        # B = 0: на старте поправка нулевая, модель равна базе.
        self.b = nn.Parameter(torch.zeros(out_dim, adapter_rank))

    def forward(self, x):
        # Базовый выход плюс поправка B·(A·x), большую матрицу B·A не собираем.
        return x @ self.base.T + (x @ self.a.T) @ self.b.T


model = Adapted()
opt = torch.optim.Adam(model.parameters(), lr=0.05)  # получит только a и b

with torch.no_grad():  # no_grad: только измеряем, градиенты не нужны
    before = nn.functional.mse_loss(model(x[120:]), y[120:]).item()

for _ in range(200):           # учимся только на первых 120 строках
    opt.zero_grad()
    loss = nn.functional.mse_loss(model(x[:120]), y[:120])
    loss.backward()
    opt.step()

with torch.no_grad():          # проверяем на 40 отложенных строках
    after = nn.functional.mse_loss(model(x[120:]), y[120:]).item()

# База не изменилась, а ошибка на новых данных упала больше чем в 20 раз.
assert torch.equal(model.base, base) and after < before * 0.05
print('Held-out MSE:', before, '->', after, 'base unchanged: PASS')
print('Synthetic low-rank adaptation, not evidence of LLM fine-tuning quality.')
