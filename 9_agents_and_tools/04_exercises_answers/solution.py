def validate_action(action):
    """Возвращает аргументы, только если действие в точности разрешено."""
    # isinstance(x, dict) — «x является словарём». set(action) — множество его ключей:
    # требуем ровно tool и arguments, без лишних полей.
    if not isinstance(action, dict) or set(action) != {'tool', 'arguments'}:
        raise ValueError('Invalid schema')
    if action['tool'] != 'read_metrics':
        raise ValueError('Unauthorized tool')
    args = action['arguments']
    if not isinstance(args, dict) or set(args) != {'service'} or args['service'] != 'demo':
        raise ValueError('Unauthorized arguments')
    return args


def may_continue(steps, limit, cancelled):
    """True, только если бюджет шагов не исчерпан и задачу не отменили."""
    # Точная проверка типа: True/False — тоже int в Python, поэтому `type(...) is int`.
    if type(steps) is not int or type(limit) is not int or type(cancelled) is not bool:
        raise ValueError('Invalid budget state')
    if steps < 0 or limit < 1:
        raise ValueError('Invalid budget state')
    return steps < limit and not cancelled
