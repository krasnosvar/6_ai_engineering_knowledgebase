"""XOR: сеть со скрытым слоем учит то, что не разделяется одной прямой."""
import torch
from torch import nn

torch.manual_seed(42)
torch.set_num_threads(2)

x = torch.tensor([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])  # (4, 2)
y = torch.tensor([0, 1, 1, 0])                    # (4,) номера классов

model = nn.Sequential(
    nn.Linear(2, 8),   # (4, 2) -> (4, 8)
    nn.Tanh(),         # нелинейность
    nn.Linear(8, 2),   # (4, 8) -> (4, 2): logits двух классов
)
optimizer = torch.optim.Adam(model.parameters(), lr=0.03)

for step in range(250):
    optimizer.zero_grad()
    loss = nn.functional.cross_entropy(model(x), y)
    loss.backward()
    optimizer.step()
    if step in (0, 249):
        print('step', step, 'loss', round(loss.item(), 5))

model.eval()
with torch.inference_mode():
    pred = model(x).argmax(-1)   # номер класса с наибольшей оценкой
print('predictions:', pred.tolist())
assert torch.equal(pred, y)
