"""Детерминированный тест исполнителя; не имитирует LLM."""


def execute(action):
    """Выполняет действие, только если оно в точности разрешено."""
    # isinstance(x, dict) — «x является словарём». set(action) — множество ключей.
    if not isinstance(action, dict) or set(action) != {'tool', 'arguments'}:
        raise ValueError('Invalid action schema')
    if action['tool'] != 'read_metrics':
        raise ValueError('Tool is not allowed')
    args = action['arguments']
    if not isinstance(args, dict) or set(args) != {'service'} or args['service'] != 'demo':
        raise ValueError('Only the demo service is authorized')
    return {'service': 'demo', 'error_rate': 0.15, 'source': 'synthetic fixture'}


def run(actions, max_steps=2):
    """Цикл агента: выполняет действия по очереди, не больше max_steps."""
    trace = []
    for i, action in enumerate(actions):  # enumerate даёт номер шага и действие
        if i >= max_steps:
            return {'status': 'budget_exhausted', 'trace': trace}
        # try/except: если execute бросит ValueError, цикл не падает, а честно
        # возвращает статус «отклонено» с причиной.
        try:
            result = execute(action)
        except ValueError as e:
            return {'status': 'rejected', 'reason': str(e), 'trace': trace}
        trace.append({'action': action, 'observation': result})
    return {'status': 'completed', 'trace': trace}


if __name__ == '__main__':
    good = {'tool': 'read_metrics', 'arguments': {'service': 'demo'}}
    assert run([good])['status'] == 'completed'
    assert run([good] * 3)['status'] == 'budget_exhausted'   # 3 шага при лимите 2
    assert run([{'tool': 'shell', 'arguments': {'cmd': 'anything'}}])['status'] == 'rejected'
    print(run([good]))
