# Разбор диагностики

Решение ниже — один из правильных вариантов. Если твой код другой, но все
проверки проходят и ты можешь объяснить каждую строку, пункт засчитан.

## Пункты 1–2: данные и подсчёт меток

```python
rows = [
    {"text": "не работает вход", "label": "auth"},
    {"text": "ошибка оплаты", "label": "billing"},
    {"text": "сбросить пароль", "label": "auth"},
]


def count_labels(rows):
    counts = {}
    for row in rows:
        counts[row["label"]] = counts.get(row["label"], 0) + 1
    return counts


assert count_labels(rows) == {"auth": 2, "billing": 1}
```

`counts.get(label, 0)` возвращает 0 для метки, которой ещё нет в словаре.
Функция создаёт новый словарь и не меняет `rows`. Типичная ошибка —
`counts[row["label"]] += 1` без `get`: на первой метке будет `KeyError`.
Такой подсчёт встретится в разделе 2, когда будем искать перекос классов.

## Пункт 3: JSON

```python
import json
from pathlib import Path

path = Path("artifacts/rows.json")
path.write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")
assert json.loads(path.read_text(encoding="utf-8")) == rows
```

`json.dumps` превращает список словарей в текст, `json.loads` — обратно. Без
`ensure_ascii=False` русские буквы сохранятся в виде последовательностей вроде
`\u043d`: данные не испортятся, но файл неудобно читать. Равенство подтверждает,
что структура сохранилась, и ничего не говорит о качестве разметки. Подойдёт и
вариант с `with open(...)`.

## Пункт 4: ошибка входа

```python
def validate(row):
    if not row.get("text"):
        raise ValueError("пустой текст обращения")
    if "label" not in row:
        raise ValueError("нет метки")
    return row


try:
    validate({"text": "", "label": "auth"})
except ValueError as error:
    print("неверная строка:", error)   # неверная строка: пустой текст обращения
```

Ошибку поднимают сразу при неверном входе, а ловят там, где знают, что с
ней делать: здесь — напечатать и продолжить. В заданиях курса функции
поднимают `ValueError`, а `check.py` проверяет, что ошибка действительно
появилась. Типичная ошибка — вернуть `None` или напечатать сообщение
вместо `raise`: вызывающий код не узнает о проблеме.

## Пункт 5: класс

```python
class Ticket:
    def __init__(self, text, label):
        self.text = text
        self.label = label

    def short(self, n):
        return self.text[:n]


tickets = [Ticket(row["text"], row["label"]) for row in rows]
print(tickets[1].short(6))   # ошибка
```

`self.text` — атрибут конкретного объекта. Срез `[:n]` не падает, если
текст короче `n`. Похожая схема «данные в `__init__`, вычисление в
методе» встретится в моделях PyTorch.
