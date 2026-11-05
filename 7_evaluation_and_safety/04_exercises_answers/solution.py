def slice_accuracy(rows):
    """Доля верных ответов (accuracy) отдельно для каждого среза."""
    if not rows:
        raise ValueError('Nonempty evaluation set required')
    counts = {}     # срез -> сколько строк
    successes = {}  # срез -> сколько верных
    for row in rows:
        # Точная проверка типа: отсекает и строку 'yes', и число 1,
        # хотя в Python 1 == True. Иначе 1 молча посчиталось бы успехом.
        if type(row['correct']) is not bool:
            raise ValueError('correct must be bool')
        key = row['slice']
        # .get(key, 0): текущее значение или 0, если ключа ещё нет.
        counts[key] = counts.get(key, 0) + 1
        # True складывается как 1, False — как 0.
        successes[key] = successes.get(key, 0) + row['correct']
    return {key: successes[key] / n for key, n in counts.items()}


def citations_allowed(cited_ids, context_ids):
    """True, если каждый процитированный ID был в переданном контексте."""
    # set(a) <= set(b) — «каждый элемент a есть в b» (подмножество).
    return set(cited_ids) <= set(context_ids)


def position_bias_check(verdicts_ab, verdicts_ba):
    """Согласованность вердиктов судьи при двух порядках показа A и B."""
    if not verdicts_ab or len(verdicts_ab) != len(verdicts_ba):
        raise ValueError('Nonempty verdict lists of equal length required')
    for verdict in verdicts_ab + verdicts_ba:
        if verdict not in ('A', 'B'):
            raise ValueError("Verdict must be 'A' or 'B'")
    # zip идёт по парам вердиктов одного вопроса в двух порядках.
    consistent = 0
    for ab, ba in zip(verdicts_ab, verdicts_ba):
        if ab == ba:
            consistent += 1
    # В verdicts_ab первым показан A, в verdicts_ba — B.
    first_wins = verdicts_ab.count('A') + verdicts_ba.count('B')
    return {
        'consistent': consistent,
        'inconsistent': len(verdicts_ab) - consistent,
        'first_wins': first_wins,
    }


def judge_calibration(human, judge):
    """Agreement, kappa и ложные одобрения судьи; 1 — «да», 0 — «нет»."""
    if not human or len(human) != len(judge):
        raise ValueError('Nonempty label lists of equal length required')
    for label in human + judge:
        # type(...) is not int отсекает True/False: bool — подкласс int.
        if type(label) is not int or label not in (0, 1):
            raise ValueError('Labels must be 0 or 1')
    n = len(human)
    p_o = sum(h == j for h, j in zip(human, judge)) / n  # наблюдаемое
    ph, pj = sum(human) / n, sum(judge) / n              # доли «да»
    p_e = ph * pj + (1 - ph) * (1 - pj)                  # случайное
    if p_e == 1:
        # Оба всегда говорят одно и то же: kappa = 0/0 не определена.
        raise ValueError('Kappa undefined: both raters use one label')
    # Ложное одобрение: человек сказал «нет», судья — «да».
    false_ok = sum(h == 0 and j == 1 for h, j in zip(human, judge))
    return {
        'agreement': p_o,
        'kappa': (p_o - p_e) / (1 - p_e),
        'false_approvals': false_ok,
    }


def guard_tool_call(call, allowlist, needs_approval):
    """Решение кода по вызову инструмента: 'allow', 'confirm' или 'deny'."""
    # Ошибка настройки — сразу ValueError, а не молчаливое разрешение.
    if not set(needs_approval) <= set(allowlist):
        raise ValueError('needs_approval must be a subset of allowlist')
    tool = call.get('tool')
    if type(tool) is not str:
        raise ValueError('call must contain tool name as str')
    # Allow-list: всё, чего нет в списке, запрещено по умолчанию —
    # что бы ни написала модель и какой бы текст ни был в контексте.
    if tool not in allowlist:
        return 'deny'
    # Рискованное действие ждёт подтверждения человека.
    if tool in needs_approval:
        return 'confirm'
    return 'allow'
