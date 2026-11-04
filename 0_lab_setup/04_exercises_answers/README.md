# Разбор диагностики

Пункты 1–2. Для подсчёта используй словарь: для каждого `row` увеличивай
счётчик `row['label']`. Новый словарь не меняет исходный список.

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

print(count_labels(rows))   # {'auth': 2, 'billing': 1}
```

Пункт 3. Сериализация — `json.dumps(rows, ensure_ascii=False)`, чтение —
`json.loads(text)`. Равенство полученных списков проверяет сохранение
структуры, а не качество разметки.

```python
import json

with open("rows.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(rows, ensure_ascii=False))
with open("rows.json", encoding="utf-8") as file:
    assert json.loads(file.read()) == rows
```

Пункт 4. Ошибку поднимают сразу при неверном входе, а ловят там, где знают,
что с ней делать: здесь — напечатать и продолжить.

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

Пункт 5.

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

Пункт 6. Вес модели подбирается при обучении. Аргумент вроде `--steps`
задаёт поведение программы; он может управлять обучением, но сам не является
обучаемым весом.

Пункт 7. Знакомые примеры модель могла просто запомнить, как ответы к
задачам, которые уже видела. О новых примерах это ничего не говорит:
проверка обобщения требует данных, которых модель при обучении не видела.
