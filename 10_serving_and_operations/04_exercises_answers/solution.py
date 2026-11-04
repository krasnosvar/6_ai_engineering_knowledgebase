import math


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
