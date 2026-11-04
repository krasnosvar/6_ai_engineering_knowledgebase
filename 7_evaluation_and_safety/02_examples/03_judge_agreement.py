"""Фикстуры разметки человеком и моделью-судьёй; настоящий judge не вызывается."""
from sklearn.metrics import cohen_kappa_score, confusion_matrix

# 1 — «ответ хороший», 0 — «плохой»; позиция i — один и тот же ответ.
human = [1, 1, 1, 1, 0, 0, 0, 0, 1, 0]
judge = [1, 1, 1, 1, 1, 1, 1, 0, 1, 0]

# Строки матрицы — оценка человека (0, 1), столбцы — оценка судьи.
print('confusion rows=human cols=judge:', confusion_matrix(human, judge, labels=[0, 1]))

matches = sum(h == j for h, j in zip(human, judge))
print('agreement:', matches / len(human))
print('Cohen kappa:', round(cohen_kappa_score(human, judge), 3))

# Ложное одобрение: человек сказал «плохо», судья — «хорошо».
false_approvals = sum(h == 0 and j == 1 for h, j in zip(human, judge))
print('Judge false approvals:', false_approvals)
print('Small artificial sample; neither human labels nor kappa guarantee objective truth.')
