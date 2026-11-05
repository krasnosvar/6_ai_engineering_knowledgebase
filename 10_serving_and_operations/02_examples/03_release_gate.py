"""Детерминированные правила выпуска по заранее рассчитанным метрикам."""
import math


def release_gate(report):
    # Отчёт должен содержать ровно эти метрики: пропуск — это не «всё хорошо».
    required = {'quality', 'p95_ms', 'acl_failures'}
    if set(report) != required:
        raise ValueError('Incomplete release report')

    # Качество и задержка — конечные числа;
    # NaN или inf означают сломанное измерение.
    for key in ('quality', 'p95_ms'):
        value = report[key]
        if type(value) not in (int, float) or not math.isfinite(value):
            raise ValueError('Finite numeric metrics required')
    # Число нарушений доступа — неотрицательное целое (bool сюда не подходит).
    if type(report['acl_failures']) is not int or report['acl_failures'] < 0:
        raise ValueError('Nonnegative integer failure count required')
    if not 0 <= report['quality'] <= 1 or report['p95_ms'] < 0:
        raise ValueError('Invalid metrics')

    # Каждое правило проверяется отдельно, причины отказа копятся в список.
    reasons = []
    if report['quality'] < .85:
        reasons.append('quality')
    if report['p95_ms'] > 1500:
        reasons.append('latency')
    if report['acl_failures'] != 0:
        reasons.append('authorization')
    return {'approved': not reasons, 'reasons': reasons}


reports = [
    {'quality': .9, 'p95_ms': 1000, 'acl_failures': 0},
    {'quality': .95, 'p95_ms': 800, 'acl_failures': 1},
    {'quality': .8, 'p95_ms': 2000, 'acl_failures': 0},
]
for report in reports:
    print(report, '=>', release_gate(report))

# Идеальное качество не компенсирует одну утечку доступа.
leak = {'quality': 1., 'p95_ms': 10, 'acl_failures': 1}
assert not release_gate(leak)['approved']

# Отсутствующее измерение задержки (NaN) должно остановить выпуск, а не пройти.
try:
    release_gate({'quality': 1., 'p95_ms': float('nan'), 'acl_failures': 0})
except ValueError:
    pass
else:
    raise AssertionError('Missing latency cannot pass the release gate')

print('Thresholds are illustrative, not universal production SLOs.')
