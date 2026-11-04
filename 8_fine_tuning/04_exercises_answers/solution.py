def _is_token_id(value):
    # Точная проверка типа: True/False — тоже int в Python, но токеном не являются.
    return type(value) is int and value >= 0


def answer_labels(prompt_ids, answer_ids, pad_to):
    """Метки для loss: -100 на prompt и padding, ID токенов на месте ответа."""
    if not prompt_ids or not answer_ids:
        raise ValueError('Prompt and answer must be nonempty')
    if type(pad_to) is not int or pad_to < len(prompt_ids) + len(answer_ids):
        raise ValueError('pad_to must be an integer covering prompt and answer')
    if not all(_is_token_id(v) for v in prompt_ids + answer_ids):
        raise ValueError('Invalid token IDs')
    padding = pad_to - len(prompt_ids) - len(answer_ids)
    # [-100] * n — список из n значений -100.
    return [-100] * len(prompt_ids) + list(answer_ids) + [-100] * padding


def lora_parameters(in_features, out_features, rank):
    """A: rank×in_features, B: out_features×rank."""
    for value in (in_features, out_features, rank):
        if type(value) is not int or value < 1:
            raise ValueError('Positive dimensions required')
    return rank * in_features + out_features * rank
