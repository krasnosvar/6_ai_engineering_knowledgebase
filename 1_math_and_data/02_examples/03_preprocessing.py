"""CPU: параметры стандартизации определяются только по train.

Урок: 1_math_and_data/01_theory/13_standardization.md.
"""
import numpy as np
from sklearn.preprocessing import StandardScaler

# Один признак, поэтому каждая таблица — столбец формы (число примеров, 1).
train = np.array([[1.0], [2.0], [3.0]])
test = np.array([[100.0], [101.0]])

# Правильно: среднее и отклонение берутся только из train.
correct = StandardScaler().fit(train)
# Ошибка: преобразование подогнано по train и test вместе
# (vstack ставит таблицы друг под другом).
leaked = StandardScaler().fit(np.vstack([train, test]))

print("среднее только по train:", correct.mean_,
      "среднее с утечкой:", leaked.mean_)
print("test, преобразованный правильно:", correct.transform(test).ravel())
print("test, преобразованный с утечкой:", leaked.transform(test).ravel())
assert correct.mean_[0] == 2 and leaked.mean_[0] > 40

print("Большие значения test — сигнал: новые данные не похожи на обучающие.")
print("Подгонка преобразования по test прячет этот сигнал: это утечка.")
