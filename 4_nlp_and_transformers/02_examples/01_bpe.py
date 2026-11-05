"""Миниатюрный BPE на символах слов; не production byte-level tokenizer."""
from collections import Counter

# Корпус: слово -> сколько раз оно встретилось (как в ручном разборе урока).
words = {'low': 5, 'lower': 2, 'newest': 6, 'widest': 3}

# Каждое слово разбиваем на символы и добавляем маркер конца слова '</w>'.
# Ключ словаря — кортеж токенов, значение — частота слова.
vocab = {}
for word, count in words.items():
    vocab[tuple(word) + ('</w>',)] = count


def merge(tokens, pair):
    """Склеить все вхождения пары соседних токенов pair в один токен."""
    result = []
    i = 0
    while i < len(tokens):
        if i + 1 < len(tokens) and (tokens[i], tokens[i + 1]) == pair:
            result.append(tokens[i] + tokens[i + 1])
            i += 2  # пару съели целиком, перешагиваем оба токена
        else:
            result.append(tokens[i])
            i += 1
    return tuple(result)


merges = []
for _ in range(8):
    # 1. Считаем частоты всех пар соседних токенов, умножая на частоту слова.
    counts = Counter()
    for tokens, count in vocab.items():
        # zip(tokens, tokens[1:]) даёт пары соседей: (t0,t1), (t1,t2), ...
        for pair in zip(tokens, tokens[1:]):
            counts[pair] += count
    if not counts:
        break

    # 2. Берём самую частую пару; при равенстве — первую по алфавиту.
    #    Ключ сортировки (-частота, пара): минус ставит частые пары первыми.
    best = sorted(counts, key=lambda p: (-counts[p], p))[0]
    merges.append(best)

    # 3. Склеиваем эту пару во всех словах корпуса.
    updated = Counter()
    for tokens, count in vocab.items():
        updated[merge(tokens, best)] += count
    vocab = dict(updated)

print('merges:', merges)

# Новое слово разбиваем, применяя выученные объединения по порядку.
for word in ('lowest', 'newest'):
    tokens = tuple(word) + ('</w>',)
    for pair in merges:
        tokens = merge(tokens, pair)
    # Склеив токены обратно, получаем исходное слово: информация не потеряна.
    assert ''.join(tokens).removesuffix('</w>') == word
    print(word, '=>', tokens)

print('Production tokenizers also need byte coverage, normalization '
      'and special tokens.')
