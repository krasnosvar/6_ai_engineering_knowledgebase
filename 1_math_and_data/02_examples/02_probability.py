"""CPU, stdlib: редкие сбои и точность тревог.

Симуляция примера из урока 1_math_and_data/01_theory/09_probability.md:
сбоев 1%, детектор замечает 90% сбоев и ложно тревожит на 5% исправных запросов.
"""
import random

# Фиксированное зерно: на той же версии Python числа повторяются.
rng = random.Random(42)

# Четыре исхода: TP — тревога при сбое, FP — тревога без сбоя,
# FN — сбой без тревоги, TN — нет ни сбоя, ни тревоги.
tp = fp = fn = tn = 0
for _ in range(100_000):
    failure = rng.random() < 0.01
    alarm_probability = 0.9 if failure else 0.05
    alarm = rng.random() < alarm_probability
    if failure and alarm:
        tp += 1
    elif alarm:
        fp += 1
    elif failure:
        fn += 1
    else:
        tn += 1

precision = tp / (tp + fp)   # доля настоящих сбоев среди тревог
recall = tp / (tp + fn)      # доля пойманных сбоев
expected_precision = 0.9 * 0.01 / (0.9 * 0.01 + 0.05 * 0.99)   # формула Байеса

print({"TP": tp, "FP": fp, "FN": fn, "TN": tn})
print(f"precision={precision:.3f}; recall={recall:.3f}")
print(f"ожидаемая precision по формуле Байеса: {expected_precision:.3f}")
assert 0.12 < precision < 0.19
