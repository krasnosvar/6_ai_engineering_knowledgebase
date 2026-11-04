"""Оценки памяти, не измерение фактического runtime."""


def kv_bytes(layers, batch, tokens, kv_heads, head_dim, bytes_per_value):
    # 2 — потому что для каждой позиции храним и key, и value.
    return 2 * layers * batch * tokens * kv_heads * head_dim * bytes_per_value


if __name__ == '__main__':
    # Веса в FP32: 4 байта на параметр. 2**30 байтов = 1 GiB.
    for size in (135_000_000, 1_000_000_000, 3_000_000_000):
        print(size, 'parameters: FP32 weights GiB=', round(size * 4 / 2**30, 3))

    # Одна и та же модель, контекст 2048 и 4096 токенов.
    short_context = kv_bytes(24, 1, 2048, 8, 64, 2)
    long_context = kv_bytes(24, 1, 4096, 8, 64, 2)
    print('Example KV cache GiB:', short_context / 2**30,
          'double context:', long_context / 2**30)
    assert long_context == 2 * short_context

    print('Exclude runtime, activations, quantization metadata and optimizer state.')
