import json

ALLOWED_LABELS = ('database', 'network', 'access', 'unknown')


def parse_ticket(raw):
    # Слой 1: это вообще JSON? На прозе вроде 'prose' json.loads бросит
    # json.JSONDecodeError. Это подкласс ValueError, поэтому ловить и
    # перебрасывать его не нужно — проверка и так получит ValueError.
    obj = json.loads(raw)

    # Слой 2: объект (dict) ровно с двумя полями. Список '[]' или лишнее поле
    # 'extra' не проходят. set(obj) — множество ключей словаря.
    if not isinstance(obj, dict) or set(obj) != {'ticket_id', 'label'}:
        raise ValueError('Invalid fields')

    # Слой 3: типы и значения. ID — непустая строка, а не число 1.
    if not isinstance(obj['ticket_id'], str) or not obj['ticket_id']:
        raise ValueError('Invalid ID')
    if obj['label'] not in ALLOWED_LABELS:
        raise ValueError('Invalid label')

    # Слой 4 (смысл) здесь не проверить: нужна разметка или сравнение с запросом.
    return obj


def remaining_tokens(limit, input_tokens, reserved_output):
    for value in (limit, input_tokens, reserved_output):
        # type(...) is not int, а не isinstance: bool — подкласс int,
        # и isinstance(True, int) вернул бы True. True не число токенов.
        if type(value) is not int or value < 0:
            raise ValueError('Nonnegative integers required')

    result = limit - input_tokens - reserved_output
    if result < 0:
        raise ValueError('Context budget exceeded')
    return result
