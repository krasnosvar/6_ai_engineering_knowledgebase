import torch


def one_step(model, optimizer, x, y):
    """Один шаг обучения классификатора; возвращает loss как обычное число."""
    model.train()
    optimizer.zero_grad()
    loss = torch.nn.functional.cross_entropy(model(x), y)
    loss.backward()
    optimizer.step()
    return float(loss.detach())


def masked_mean(hidden, mask):
    """Среднее по оси T только по позициям, где mask == 1.

    hidden: (B, T, D), mask: (B, T) из 0 и 1 -> результат (B, D).
    """
    if hidden.ndim != 3 or mask.shape != hidden.shape[:2]:
        raise ValueError('Expected BTD hidden and binary BT mask')
    if not torch.all((mask == 0) | (mask == 1)):
        raise ValueError('Expected BTD hidden and binary BT mask')

    counts = mask.sum(dim=1, keepdim=True)        # (B, 1): реальных позиций
    if (counts == 0).any():
        raise ValueError('Empty sequence')
    weighted = hidden * mask.unsqueeze(-1)        # (B, T, D): пустые -> 0
    return weighted.sum(dim=1) / counts           # (B, D)
