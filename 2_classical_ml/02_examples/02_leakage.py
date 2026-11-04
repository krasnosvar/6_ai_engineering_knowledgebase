"""Групповая утечка: у одного клиента несколько строк, метка зависит от клиента.

Признак у «модели» только один — ID клиента. Метка (например, «клиент уйдёт»)
случайна для каждого клиента, поэтому настоящей закономерности нет. Хорошая
оценка возможна только за счёт запоминания ID.
"""
import random

rng = random.Random(42)

GROUPS = 200          # клиентов
ROWS_PER_GROUP = 4    # обращений от каждого клиента

labels = {g: rng.randrange(2) for g in range(GROUPS)}
rows = [(g, labels[g]) for g in range(GROUPS) for _ in range(ROWS_PER_GROUP)]


def evaluate(train, test):
    """«Модель» запоминает метку каждого клиента из train.

    Для клиента, которого в train не было, отвечает самой частой меткой train.
    """
    lookup = dict(train)
    ones = sum(y for _, y in train)
    majority = int(ones > len(train) / 2)
    correct = sum(lookup.get(g, majority) == y for g, y in test)
    return correct / len(test)


# 1. Случайное разбиение СТРОК: строки одного клиента попадают и в train, и в test.
shuffled = rows[:]
rng.shuffle(shuffled)
cut = int(len(shuffled) * 0.75)
row_train, row_test = shuffled[:cut], shuffled[cut:]
seen = {g for g, _ in row_train}
share_seen = sum(g in seen for g, _ in row_test) / len(row_test)

# 2. Разбиение по КЛИЕНТАМ: клиенты из test в train не встречаются вообще.
test_groups = set(rng.sample(range(GROUPS), GROUPS // 4))
group_train = [r for r in rows if r[0] not in test_groups]
group_test = [r for r in rows if r[0] in test_groups]

a = evaluate(row_train, row_test)
b = evaluate(group_train, group_test)
print(f'Разбиение по строкам: {share_seen:.0%} test-строк от знакомых клиентов, '
      f'accuracy={a:.3f}')
print(f'Разбиение по клиентам: 0% знакомых клиентов, accuracy={b:.3f}')
print('Высокая оценка в первом случае — запоминание ID, а не закономерность.')
assert a > 0.95 and b < 0.7
