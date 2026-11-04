def kv_bytes(layers, batch, tokens, kv_heads, head_dim, bytes_per_value):
    raise NotImplementedError('TODO: keys and values for each cached position')


def nearest_rank(values, p):
    raise NotImplementedError('TODO: documented quantile convention')


def span_tree_summary(spans):
    raise NotImplementedError('TODO: total and self time for each span')


def redact(text):
    raise NotImplementedError('TODO: mask API keys and emails')
