"""Исследуем сохранность фразы на границе словесных окон; не tokenizer LLM."""


def chunks(words, size, overlap):
    """Нарезать список слов на окна по size слов с перекрытием overlap."""
    if size < 1 or not 0 <= overlap < size:
        raise ValueError('Require 0 <= overlap < size')
    result = []
    # Шаг окна = size - overlap: при перекрытии следующее окно
    # начинается раньше.
    for start in range(0, len(words), size - overlap):
        part = words[start:start + size]
        if part:
            result.append(' '.join(part))
        if start + size >= len(words):
            break  # окно дошло до конца текста
    return result


# 12 слов; нужный факт — слова 5–10 (индексы 4..9).
words = ('alpha beta gamma delta error budget is forty three minutes '
         'omega sigma').split()
for size, overlap in [(6, 0), (6, 3), (12, 0)]:
    parts = chunks(words, size, overlap)
    # Сохранился ли нужный факт целиком хотя бы в одном фрагменте?
    intact = any('error budget is forty three minutes' in p for p in parts)
    print({
        'size_words': size,
        'overlap_words': overlap,
        'chunks': parts,
        'fact_intact': intact,
        'indexed_words': sum(len(p.split()) for p in parts),
    })
print('More overlap costs index space. Word counts are not LLM token counts.')
