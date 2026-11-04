def mse_gradient(w, b, x, y):
    """Вернуть пару (dL/dw, dL/db) для MSE модели y_hat = w*x + b.

    Пустые списки или списки разной длины — ValueError.
    """
    raise NotImplementedError("TODO: производные средней квадратичной ошибки")


def cosine(a, b):
    """Вернуть косинусное сходство векторов a и b.

    Пустые входы, разные длины и нулевой вектор — ValueError.
    """
    raise NotImplementedError("TODO: косинусное сходство и проверки входа")


def softmax_with_temperature(logits, t):
    """Вернуть список вероятностей softmax(logits / t).

    Пустые logits или t <= 0 — ValueError. Огромные logits вроде
    [1000, 999] не должны вызывать переполнение.
    """
    raise NotImplementedError("TODO: устойчивый softmax с температурой")


def perplexity(token_probs):
    """Вернуть exp(средняя потеря -ln p) по вероятностям правильных токенов.

    Пустой список или вероятность вне (0, 1] — ValueError.
    """
    raise NotImplementedError("TODO: perplexity по вероятностям токенов")
