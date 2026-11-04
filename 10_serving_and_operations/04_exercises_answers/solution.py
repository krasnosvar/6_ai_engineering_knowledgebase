import math
import re


def kv_bytes(layers, batch, tokens, kv_heads, head_dim, bytes_per_value):
    dims = (layers, batch, tokens, kv_heads, head_dim, bytes_per_value)
    # Каждый размер — положительное целое: ноль токенов или дробная голова
    # означают ошибку во входных данных, а не «пустой кэш».
    for v in dims:
        if type(v) is not int or v < 1:
            raise ValueError('Positive dimensions required')
    # math.prod перемножает все элементы; 2 — key и value.
    return 2 * math.prod(dims)


def nearest_rank(values, p):
    if not values or not 0 < p <= 1:
        raise ValueError('Invalid latency samples or quantile')
    for v in values:
        # math.isfinite отбрасывает NaN и бесконечность.
        if not math.isfinite(v) or v < 0:
            raise ValueError('Invalid latency samples or quantile')
    # sorted создаёт новый список — исходный не меняется.
    ordered = sorted(values)
    rank = math.ceil(p * len(values))  # номер, считая с 1
    return ordered[rank - 1]           # индекс в Python — с 0


def span_tree_summary(spans):
    """Возвращает {id: (total, self)}: полное и собственное время span."""
    if not isinstance(spans, list):
        raise ValueError('List of spans required')
    by_id = {}
    for s in spans:
        if not isinstance(s, tuple) or len(s) != 4:
            raise ValueError('Span must be (id, parent, start, end)')
        sid, parent, start, end = s
        if sid in by_id:
            raise ValueError(f'Duplicate span id: {sid}')
        # Время — целые миллисекунды; конец не раньше начала.
        if type(start) is not int or type(end) is not int:
            raise ValueError(f'Integer times required: {sid}')
        if not 0 <= start <= end:
            raise ValueError(f'Invalid interval: {sid}')
        by_id[sid] = s

    children_ms = {sid: 0 for sid in by_id}  # сумма длительностей детей
    for sid, parent, start, end in spans:
        if parent is None:
            continue  # корень trace
        if parent == sid or parent not in by_id:
            raise ValueError(f'Unknown parent of span: {sid}')
        _, _, p_start, p_end = by_id[parent]
        # Родитель охватывает детей по времени.
        if start < p_start or end > p_end:
            raise ValueError(f'Span outside its parent: {sid}')
        children_ms[parent] += end - start

    summary = {}
    for sid, _, start, end in spans:
        total = end - start
        own = total - children_ms[sid]
        # Отрицательное собственное время значит, что дети пересекаются;
        # в этом задании дети одного родителя идут друг за другом.
        if own < 0:
            raise ValueError(f'Children overlap: {sid}')
        summary[sid] = (total, own)
    return summary


# \b — граница слова: `task-42` не похоже на ключ, хотя содержит `sk-`.
API_KEY = re.compile(r'\bsk-[A-Za-z0-9_-]+')
EMAIL = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')


def redact(text):
    """Маскирует ключи вида sk-... и адреса почты до записи в trace."""
    if not isinstance(text, str):
        raise ValueError('Text must be a string')
    text = API_KEY.sub('sk-***', text)
    return EMAIL.sub('<email>', text)
