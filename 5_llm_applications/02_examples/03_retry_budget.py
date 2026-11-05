"""Детерминированный сценарий ответов сервера. Нет сети и реальных ожиданий."""

# Временные ошибки: имеет смысл повторить запрос позже.
RETRYABLE = (429, 500, 502, 503, 504)


def simulate(statuses, max_attempts=3):
    """statuses — какие HTTP-коды сервер вернул бы на попытки 1, 2, 3, ..."""
    if max_attempts < 1:
        raise ValueError('Positive budget required')
    trace = []
    # enumerate даёт пары (номер с нуля, элемент): (0, 429), (1, 503), ...
    for i, status in enumerate(statuses):
        if i >= max_attempts:
            return {'status': 'budget_exhausted', 'trace': trace}
        trace.append({'attempt': i + 1, 'http_status': status})
        if status == 200:
            return {'status': 'ok', 'trace': trace}
        if status not in RETRYABLE:
            # Например, 401: повтор не поможет, ошибка постоянная.
            return {'status': 'permanent_error', 'trace': trace}
        if i + 1 < max_attempts:
            # Экспоненциальная пауза 1, 2, 4, ... секунд, но не больше 8.
            trace[-1]['planned_backoff_seconds'] = min(2 ** i, 8)
    return {'status': 'failed', 'trace': trace}


assert simulate([429, 503, 200])['status'] == 'ok'
assert len(simulate([401, 200])['trace']) == 1
assert len(simulate([503] * 10)['trace']) == 3
print(simulate([429, 503, 200]))
print('Real client also needs timeout, Retry-After handling, jitter '
      'and cancellation.')
