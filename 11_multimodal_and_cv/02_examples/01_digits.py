"""CPU: настоящая CNN на встроенных изображениях digits 8x8."""
import torch
from torch import nn
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split

torch.manual_seed(42)
torch.set_num_threads(2)

digits = load_digits()
train, test = train_test_split(range(len(digits.target)), test_size=.25,
                               random_state=42, stratify=digits.target)

# images имеет форму (N, 8, 8); [:, None] добавляет ось каналов -> (N, 1, 8, 8).
# Деление на 16 переводит яркость 0..16 в 0..1.
x = torch.tensor(digits.images[:, None, :, :] / 16, dtype=torch.float32)
y = torch.tensor(digits.target, dtype=torch.long)

# Формы для группы из B изображений:
# (B,1,8,8) -> Conv2d -> (B,8,8,8) -> Flatten -> (B,512) -> Linear -> (B,10)
model = nn.Sequential(
    nn.Conv2d(1, 8, 3, padding=1),  # 8 ядер 3x3; padding=1 сохраняет размер 8x8
    nn.ReLU(),
    nn.Flatten(),
    # 512 входов -> 10 logits, по одному на цифру.
    nn.Linear(8 * 8 * 8, 10),
)
opt = torch.optim.Adam(model.parameters(), lr=.01)

for _ in range(8):  # 8 эпох
    # Каждую эпоху перемешиваем номера обучающих примеров
    # и режем на группы по 64.
    indices = torch.tensor(train)[torch.randperm(len(train))]
    for batch in indices.split(64):
        opt.zero_grad()
        loss = nn.functional.cross_entropy(model(x[batch]), y[batch])
        loss.backward()
        opt.step()

model.eval()
with torch.inference_mode():
    # argmax(-1) — номер самого большого logit, то есть предсказанная цифра.
    predicted = model(x[test]).argmax(-1)
    accuracy = (predicted == y[test]).float().mean().item()
print('held-out digits accuracy:', round(accuracy, 4))
assert accuracy > .85
