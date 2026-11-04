import math


def mse_gradient(w, b, x, y):
    """Производные MSE по w и b для модели y_hat = w*x + b."""
    if not x or len(x) != len(y):
        raise ValueError("Нужны непустые списки одинаковой длины")
    errors = [w * a + b - t for a, t in zip(x, y)]
    dw = 2 * sum(e * a for e, a in zip(errors, x)) / len(x)
    db = 2 * sum(errors) / len(x)
    return dw, db


def cosine(a, b):
    """Косинус угла между векторами: скалярное произведение / произведение длин."""
    if not a or len(a) != len(b):
        raise ValueError("Нужны непустые векторы одинаковой длины")
    length_a = math.sqrt(sum(v * v for v in a))
    length_b = math.sqrt(sum(v * v for v in b))
    if length_a == 0 or length_b == 0:
        raise ValueError("У нулевого вектора нет направления")
    dot = sum(p * q for p, q in zip(a, b))
    return dot / (length_a * length_b)


def softmax_with_temperature(logits, t):
    """Вероятности токенов: softmax от logits, делённых на температуру t."""
    if not logits:
        raise ValueError("Нужен непустой список logits")
    if t <= 0:
        raise ValueError("Температура должна быть больше 0")
    scaled = [z / t for z in logits]
    # math.exp(1000) не помещается во float и бросает OverflowError.
    # Вычитаем максимум: e^(z-m) = e^z / e^m, и множитель 1/e^m
    # сокращается в числителе и знаменателе — ответ тот же, а самая
    # большая экспонента теперь e^0 = 1.
    top = max(scaled)
    exps = [math.exp(z - top) for z in scaled]
    total = sum(exps)
    return [e / total for e in exps]


def perplexity(token_probs):
    """Экспонента средней потери -ln(p) по токенам фразы."""
    if not token_probs:
        raise ValueError("Нужен непустой список вероятностей")
    for p in token_probs:
        # ln(0) не существует, а вероятность больше 1 — ошибка входа.
        if not 0 < p <= 1:
            raise ValueError("Вероятность должна быть в (0, 1]")
    mean_loss = sum(-math.log(p) for p in token_probs) / len(token_probs)
    return math.exp(mean_loss)
