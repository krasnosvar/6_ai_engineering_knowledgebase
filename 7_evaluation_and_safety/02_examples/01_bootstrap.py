"""Парный bootstrap: сравниваем правильность двух систем на одних задачах."""
import random
import statistics


def paired_interval(a, b, seed=42, repeats=3000):
    """Разность средних b-a и приближённый 95% интервал для неё.

    a и b — списки 0/1 (неверно/верно) для ОДНИХ И ТЕХ ЖЕ задач в одном
    порядке: a[i] и b[i] — ответы двух версий на задачу i. Ручной разбор
    одного шага и квантилей — в уроке
    7_evaluation_and_safety/01_theory/02_comparing_versions.md.
    """
    if not a or len(a) != len(b):
        raise ValueError('Nonempty paired observations required')
    rng = random.Random(seed)  # фиксированный seed: результат повторяем
    diffs = []
    for _ in range(repeats):
        # Выбираем len(a) индексов с повторами — одни и те же для обеих версий.
        indices = [rng.randrange(len(a)) for _ in a]
        diffs.append(statistics.mean(b[i] - a[i] for i in indices))
    diffs.sort()
    delta = statistics.mean(y - x for x, y in zip(a, b))
    # 2.5% и 97.5% квантили отсортированных разностей — границы интервала.
    low = diffs[int(0.025 * repeats)]
    high = diffs[int(0.975 * repeats)]
    return delta, low, high


if __name__ == '__main__':
    a = [1, 1, 0, 1, 0, 0, 1, 0, 1, 0]
    b = [1, 1, 1, 1, 0, 1, 1, 0, 0, 0]
    delta, low, high = paired_interval(a, b)
    print(f'delta={delta:.3f}; '
          f'approximate 95% interval=[{low:.3f}, {high:.3f}]')
    print('Zero inside interval:', low <= 0 <= high)
    # Версия, сравнённая сама с собой, обязана дать нулевую разность.
    assert paired_interval(a, a) == (0, 0, 0)
