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

    # Цены за 1 млн токенов: ровно три ключа, без цен «по умолчанию».
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


PRICE_KEYS = {'input', 'cached_input', 'output'}


def call_cost(input_tokens, output_tokens, cached_tokens, prices):
    for value in (input_tokens, output_tokens, cached_tokens):
        # Тот же приём, что в remaining_tokens: bool не число токенов.
        if type(value) is not int or value < 0:
            raise ValueError('Nonnegative integers required')
    # Закэшированные токены — часть входа, а не добавка к нему.
    if cached_tokens > input_tokens:
        raise ValueError('cached_tokens > input_tokens')

    # Цены за миллион токенов: ровно три ключа, без цен «по умолчанию».
    if not isinstance(prices, dict) or set(prices) != PRICE_KEYS:
        raise ValueError('Prices need input, cached_input, output')
    for price in prices.values():
        if type(price) not in (int, float) or price < 0:
            raise ValueError('Price must be a nonnegative number')

    fresh = input_tokens - cached_tokens
    return (fresh * prices['input']
            + cached_tokens * prices['cached_input']
            + output_tokens * prices['output']) / 1_000_000


def wrap_untrusted(text, tag):
    if not isinstance(text, str):
        raise ValueError('Text must be a string')
    # Имя тега — только строчные латинские буквы: иначе в нём могли бы
    # оказаться '<', '>' или '/', и разделитель сломался бы сам.
    if not isinstance(tag, str) or not tag or not (
            tag.isascii() and tag.isalpha() and tag.islower()):
        raise ValueError('Tag must be lowercase latin letters')

    closing = f'</{tag}>'
    # Данные не должны закрыть разделитель раньше времени: как в уроке 03,
    # превращаем '</ticket>' в '</ ticket>'. Текст сохраняется, но
    # закрывающего тега внутри больше нет.
    safe = text.replace(closing, f'</ {tag}>')
    return f'<{tag}>\n{safe}\n{closing}'


def weights_memory_gb(params, bits):
    for value in (params, bits):
        # 7e9 — это float, а число параметров целое: пиши 7_000_000_000.
        if type(value) is not int or value <= 0:
            raise ValueError('Positive integers required')
    # Биты → байты (делим на 8), байты → GB (делим на 10**9, как в уроке).
    return params * bits / 8 / 10**9
