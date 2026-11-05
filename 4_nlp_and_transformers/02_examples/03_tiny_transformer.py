"""CPU: маленький causal Transformer, без внешних данных и готовых весов."""
import torch
from torch import nn

torch.manual_seed(42)
torch.set_num_threads(2)

# Учебный корпус: одна строка, повторённая 40 раз. Токены — отдельные символы.
text = 'metrics show errors. logs explain errors. restart fixes demo. ' * 40
chars = sorted(set(text))
ids = {c: i for i, c in enumerate(chars)}  # символ -> номер в словаре
seq = torch.tensor([ids[c] for c in text])
block = 24  # длина контекста, которую видит модель


class TinyLM(nn.Module):
    def __init__(self):
        super().__init__()
        self.token = nn.Embedding(len(chars), 32)  # таблица embeddings токенов
        self.pos = nn.Embedding(block, 32)          # обучаемый вектор позиции
        # Один блок Transformer: d_model=32, 4 головы, feed-forward шириной 64.
        self.layer = nn.TransformerEncoderLayer(32, 4, 64, dropout=0,
                                                batch_first=True)
        self.head = nn.Linear(32, len(chars))       # logits всех символов

    def forward(self, x):
        t = x.shape[1]
        h = self.token(x) + self.pos(torch.arange(t))
        # True выше диагонали = запрещено смотреть в будущее (causal mask).
        mask = torch.triu(torch.ones(t, t, dtype=torch.bool), diagonal=1)
        return self.head(self.layer(h, src_mask=mask))


model = TinyLM()
opt = torch.optim.AdamW(model.parameters(), lr=0.01)
losses = []
for step in range(100):
    # Батч из 8 случайных кусков: вход x и цели y, сдвинутые на 1 символ.
    starts = torch.randint(len(seq) - block - 1, (8,))
    x = torch.stack([seq[s:s + block] for s in starts])
    y = torch.stack([seq[s + 1:s + block + 1] for s in starts])

    opt.zero_grad()
    logits = model(x)
    loss = nn.functional.cross_entropy(logits.reshape(-1, len(chars)),
                                       y.reshape(-1))
    loss.backward()
    opt.step()
    losses.append(loss.item())

model.eval()
with torch.inference_mode():
    # Проверка маски: меняем последний символ — предсказания для ранних
    # позиций остаются теми же.
    probe = seq[:block].unsqueeze(0)
    changed = probe.clone()
    changed[:, -1] = (changed[:, -1] + 1) % len(chars)
    assert torch.allclose(model(probe)[:, :-1], model(changed)[:, :-1],
                          atol=1e-5)

    # Greedy-генерация: каждый раз берём самый вероятный следующий символ.
    context = torch.tensor([[ids[c] for c in 'metrics ']])
    for _ in range(60):
        nxt = model(context[:, -block:])[:, -1].argmax(-1, keepdim=True)
        context = torch.cat([context, nxt], dim=1)

print(f'loss {losses[0]:.3f} -> {losses[-1]:.3f}')
print(''.join(chars[i] for i in context[0].tolist()))
assert losses[-1] < losses[0] * 0.5
print('Synthetic memorization demo; not a held-out language benchmark.')
