"""Запоминание случайных меток: успех на train не гарантирует обобщения.

Метки случайны, поэтому связи между входом и ответом нет. Сеть учится на 16
примерах, остальные 112 — validation. Следи за двумя кривыми loss.
"""
import torch
from torch import nn

torch.manual_seed(42)
torch.set_num_threads(2)

x = torch.randn(128, 16)              # 128 примеров по 16 случайных признаков
y = torch.randint(0, 2, (128,))       # случайные классы 0/1
x_train, y_train = x[:16], y[:16]
x_val, y_val = x[16:], y[16:]

model = nn.Sequential(nn.Linear(16, 64), nn.ReLU(), nn.Linear(64, 2))
optimizer = torch.optim.Adam(model.parameters(), lr=0.02)
loss_fn = nn.CrossEntropyLoss()

best_val, best_epoch = float('inf'), 0
print('эпоха  train_loss  val_loss')
for epoch in range(1, 151):
    # Весь train помещается в один batch: одна эпоха = один шаг.
    model.train()
    optimizer.zero_grad()
    loss = loss_fn(model(x_train), y_train)
    loss.backward()
    optimizer.step()

    model.eval()
    with torch.inference_mode():
        val_loss = loss_fn(model(x_val), y_val).item()
    if val_loss < best_val:
        best_val, best_epoch = val_loss, epoch
    if epoch in (1, 5, 10, 20, 50, 100, 150):
        print(f'{epoch:5d}  {loss.item():10.3f}  {val_loss:8.3f}')

with torch.inference_mode():
    train_acc = (model(x_train).argmax(-1) == y_train).float().mean().item()
    val_acc = (model(x_val).argmax(-1) == y_val).float().mean().item()
print(f'Лучший val_loss={best_val:.3f} на эпохе {best_epoch}: '
      f'здесь остановила бы ранняя остановка.')
print(f'Итог: train accuracy={train_acc:.3f}; '
      f'validation accuracy={val_acc:.3f}')
assert train_acc > 0.95 and val_acc < 0.75
