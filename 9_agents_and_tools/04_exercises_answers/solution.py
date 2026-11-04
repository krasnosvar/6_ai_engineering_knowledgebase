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


def handle_jsonrpc(request, tools, allowed):
    """Отвечает на JSON-RPC запрос в стиле MCP с учётом политики хоста."""
    # Неверная форма запроса — ошибка вызывающего кода, а не ответ модели.
    if not isinstance(request, dict) or request.get('jsonrpc') != '2.0':
        raise ValueError('Invalid JSON-RPC request')
    if 'id' not in request or not isinstance(request.get('method'), str):
        raise ValueError('Invalid JSON-RPC request')
    params = request.get('params', {})
    if not isinstance(params, dict):
        raise ValueError('Invalid JSON-RPC request')
    rid = request['id']

    def ok(result):
        return {'jsonrpc': '2.0', 'id': rid, 'result': result}

    def error(code, message):
        return {'jsonrpc': '2.0', 'id': rid,
                'error': {'code': code, 'message': message}}

    if request['method'] == 'tools/list':
        # Модели показываем только пересечение: что сервер умеет И что
        # разрешил хост. sorted — порядок не зависит от порядка в словаре.
        return ok({'tools': sorted(n for n in tools if n in allowed)})
    if request['method'] != 'tools/call':
        return error(-32601, 'Method not found')

    name, arguments = params.get('name'), params.get('arguments')
    if not isinstance(name, str) or not isinstance(arguments, dict):
        return error(-32602, 'Invalid params')
    # Сначала политика хоста: запрещённый инструмент не вызываем вовсе,
    # даже если сервер его знает.
    if name not in allowed:
        return error(-32000, 'Tool not allowed')
    if name not in tools:
        return error(-32602, 'Unknown tool')
    try:
        text = tools[name](arguments)
    except ValueError as exc:
        # Инструмент запустился, но не справился: это результат с isError,
        # его прочитает модель. Другие исключения не глушим.
        return ok({'isError': True,
                   'content': [{'type': 'text', 'text': str(exc)}]})
    return ok({'isError': False, 'content': [{'type': 'text', 'text': text}]})


def check_positive(*values):
    """ValueError, если хоть одно значение не положительное целое."""
    for v in values:
        # type(v) is int отсекает и дроби, и True/False.
        if type(v) is not int or v < 1:
            raise ValueError('Positive integers required')


def agent_tokens(system, per_step, steps):
    """Входные токены одного агента за steps шагов (формула урока)."""
    check_positive(system, per_step, steps)
    # На шаге i (с нуля) читается system + per_step * i токенов.
    # Сумма 0 + 1 + ... + (steps - 1) равна steps * (steps - 1) // 2.
    return system * steps + per_step * (steps * (steps - 1) // 2)


def multi_agent_cost(system, per_step, steps, workers, summary):
    """Оркестратор (план и итог) плюс workers исполнителей по steps шагов."""
    check_positive(system, per_step, steps, workers, summary)
    workers_total = workers * agent_tokens(system, per_step, steps)
    plan = system                          # первый вызов: план
    final = system + workers * summary     # второй: итог по сводкам
    return workers_total + plan + final
