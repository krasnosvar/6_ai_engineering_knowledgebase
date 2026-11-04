# Минимум Python для курса

Код примеров и заданий курса написан на Python и использует ограниченный
набор конструкций. Здесь собран весь этот набор: у каждой конструкции —
короткий пример и ссылка на подробный урок в соседней [Python-базе
серии](../../4_python_my_knowledgebase/README.md). Если пример понятен с
первого взгляда, переходи к следующему; если нет — открой ссылку
«подробнее», прежде чем идти дальше.

Проверить себя можно [входной диагностикой](03_exercises/README.md): она
использует все конструкции с этой страницы.

## Функции

```python
def total_minutes(checks, per_check=2):
    return checks * per_check + 1

print(total_minutes(3))      # 7
print(total_minutes(3, 5))   # 16
```

`def` объявляет функцию, `return` возвращает результат, `per_check=2` — значение
по умолчанию, если аргумент не передан. Подробнее:
[функции](../../4_python_my_knowledgebase/1_python/1_python_fundamentals/05_functions_basics/).

## Циклы и условия

```python
for minutes in [3, 12, 7]:
    if minutes > 10:
        print("долго")
    elif minutes > 5:
        print("средне")
    else:
        print("быстро")

for i in range(3):            # 0, 1, 2
    print(i)
```

Блок кода задаётся отступом в 4 пробела. Подробнее: [ветвления и
циклы](../../4_python_my_knowledgebase/1_python/1_python_fundamentals/04_control_flow_basics/).

## f-строки

```python
precision = 2 / 3
print(f"precision={precision:.3f}")   # precision=0.667
```

Выражение в фигурных скобках подставляется в строку; `:.3f` — три знака после
запятой. Подробнее: [операторы и
выражения](../../4_python_my_knowledgebase/1_python/1_python_fundamentals/02_operators_and_expressions/).

## Списки, словари, множества

```python
times = [3, 12, 7]
times.append(5)               # [3, 12, 7, 5]
print(times[0], times[-1])    # 3 5 — первый и последний элемент
print(times[1:3])             # [12, 7] — срез: с 1 по 3, не включая 3
print(len(times))             # 4

ticket = {"text": "не работает вход", "label": "auth"}
print(ticket["label"])        # auth
print(ticket.get("owner", "нет"))  # нет — ключа нет, вернулось значение по умолчанию
for key, value in ticket.items():
    print(key, value)

labels = {"auth", "db", "auth"}
print(len(labels))            # 2 — множество хранит только уникальные значения
print("db" in labels)         # True
```

Список — упорядоченная последовательность, словарь — пары «ключ → значение»,
множество — набор без повторов. Подробнее:
[коллекции](../../4_python_my_knowledgebase/1_python/2_basics/01_theory/02_collections_lists_tuples_sets_dicts.md).

## zip, enumerate и списковые выражения

```python
x = [1, 2]
y = [3, 5]
for a, t in zip(x, y):        # пары (1, 3), затем (2, 5)
    print(a, t)

for number, text in enumerate(["вход", "оплата"], 1):
    print(number, text)       # 1 вход, затем 2 оплата

errors = [a * 2 - t for a, t in zip(x, y)]   # [-1, -1]
positive = [e for e in errors if e > 0]      # [] — фильтр по условию
```

`zip` идёт по нескольким спискам параллельно, `enumerate` добавляет номер.
Запись `[выражение for ... in ... if ...]` строит новый список, она заменяет
цикл с `append`. Подробнее:
[comprehensions](../../4_python_my_knowledgebase/1_python/2_basics/01_theory/05_comprehensions.md).

## lambda и сортировка по ключу

```python
scores = {"doc1": 0.2, "doc2": 0.9, "doc3": 0.5}
best = sorted(scores, key=lambda doc: scores[doc], reverse=True)
print(best)                   # ['doc2', 'doc3', 'doc1']
```

`lambda doc: scores[doc]` — короткая функция без имени: для каждого документа
она возвращает его оценку, и `sorted` упорядочивает по ней. Подробнее:
[lambda](../../4_python_my_knowledgebase/1_python/3_functions_and_decorators/01_theory/01_lambdas.md).

## Исключения: raise и try/except

```python
def check_text(text):
    if not text:
        raise ValueError("пустой текст")
    return text

try:
    check_text("")
except ValueError as error:
    print("ошибка:", error)   # ошибка: пустой текст
```

`raise` останавливает функцию и сообщает об ошибке. `try/except` ловит ошибку
указанного типа, и программа продолжает работу. Почти все задания курса требуют
поднимать `ValueError` на неверных входах. Подробнее:
[исключения](../../4_python_my_knowledgebase/1_python/1_python_fundamentals/06_exceptions/).

## Классы

```python
class Ticket:
    def __init__(self, text, label):
        self.text = text      # атрибуты конкретного объекта
        self.label = label

    def short(self, n):
        return self.text[:n]

ticket = Ticket("не работает вход в систему", "auth")
print(ticket.label)           # auth
print(ticket.short(10))       # не работае
```

Класс — шаблон, объект — конкретный экземпляр. `__init__` заполняет атрибуты при
создании, `self` — «этот объект». В PyTorch модель — класс, поэтому эта
конструкция встретится в разделах 3, 4 и 8. Подробнее: [что такое
класс](../../4_python_my_knowledgebase/1_python/4_oop/01_theory/01_what_is_a_class.md).

## Файлы и JSON

```python
import json

rows = [{"text": "не работает вход", "label": "auth"}]
with open("rows.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(rows, ensure_ascii=False))
with open("rows.json", encoding="utf-8") as file:
    loaded = json.loads(file.read())
print(loaded == rows)         # True
```

`with open(...)` открывает файл и гарантированно закрывает его после блока.
`json.dumps` превращает данные в текст, `json.loads` — обратно. Подробнее:
[контекстные
менеджеры](../../4_python_my_knowledgebase/1_python/3_functions_and_decorators/01_theory/06_context_managers.md).

## import и запуск скрипта

```python
import math
from pathlib import Path

print(math.sqrt(25))          # 5.0
print(Path("data") / "tickets.json")   # data/tickets.json

if __name__ == "__main__":
    print("файл запущен напрямую")
```

`import` подключает модуль. Блок `if __name__ == "__main__":` выполняется,
только когда файл запущен командой `python файл.py`, а не импортирован.
Подробнее: [модули и
import](../../4_python_my_knowledgebase/1_python/1_python_fundamentals/07_modules_and_imports/).

## Подсказки типов

В части примеров встречаются записи вида `def f(x: list[float]) -> float:`. Это
необязательные подсказки типов: Python их не проверяет при запуске, они помогают
читать код. Подробнее — раздел «Аннотации типов» в уроке о
[функциях](../../4_python_my_knowledgebase/1_python/1_python_fundamentals/05_functions_basics/01_theory/01_functions_basics.md).

[К разделу 0](README.md).
