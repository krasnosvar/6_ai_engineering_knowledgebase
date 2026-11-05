# Входная диагностика Python

Диагностика показывает, хватает ли Python, чтобы читать код курса и не
разбираться одновременно с синтаксисом и с машинным обучением. Профиль
CPU, без модели и скачиваний, 45–90 минут. Выполняй после уроков раздела
0 или сразу, если хочешь сначала проверить себя.

## Где писать и как проверять

Создай каталог `artifacts/`, если его ещё нет: он исключён из Git и в
свежем клоне может отсутствовать. Например, из корня репозитория:

```bash
mkdir -p artifacts
```

Создай в нём файл `diagnostic.py` и решай пункты 1–5. Запуск из корня:

```bash
uv run python artifacts/diagnostic.py
```

Проверочного скрипта у диагностики нет: в каждом пункте указано, что
должно получиться. Добавляй в конец файла `assert`, сравнивающие твой
результат с ожидаемым, например
`assert count_labels(rows) == {"auth": 2, "billing": 1}`. Если все
проверки верны, программа завершится молча; если нет, Python покажет
`AssertionError` и номер строки.

Если пункт не получается за 15–20 минут, открой урок Python-базы по ссылке
в этом пункте, затем вернись. Полный список нужных тем — на странице
[какой Python нужен для курса](../python_minimum.md).

## Задания

1. Создай список `rows` из трёх обращений. Каждое обращение — словарь с ключами
   `text` и `label`, у двух из них метка `auth`, у одного — `billing`. Тема:
   [коллекции](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/1_python_fundamentals/05_collections/01_theory/01_lists_tuples_sets_dicts.md).
2. Напиши функцию `count_labels(rows)`, которая возвращает словарь «метка →
   число обращений»: для списка из пункта 1 — `{"auth": 2, "billing": 1}`.
   Исходный список меняться не должен. Темы:
   [функции](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/1_python_fundamentals/06_functions_basics/01_theory/01_functions_basics.md),
   [изменяемость](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/1_python_fundamentals/05_collections/01_theory/02_mutability_and_references.md).
3. Сохрани `rows` в файл `artifacts/rows.json`, прочитай его обратно и проверь,
   что прочитанный список равен исходному. Русские буквы в файле должны остаться
   читаемыми. Тема: [json и
   csv](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/6_standard_library/01_theory/05_json_csv_serialization.md).
4. Напиши `validate(row)`: если `text` пустой, функция поднимает
   `ValueError("пустой текст обращения")`, если нет ключа `label` —
   `ValueError("нет метки")`; иначе возвращает `row`. Вызови её на строке
   `{"text": "", "label": "auth"}` внутри `try`/`except` и напечатай сообщение
   ошибки. Программа после этого должна продолжить работу. Тема:
   [исключения](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/1_python_fundamentals/07_exceptions/01_theory/01_exceptions.md).
5. Напиши класс `Ticket` с `__init__(self, text, label)` и методом `short(self,
   n)`, который возвращает первые `n` символов текста. Преврати `rows` в список
   объектов `Ticket` и напечатай `short(6)` для второго. Тема: [что такое
   класс](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/3_oop/01_theory/01_what_is_a_class.md).

## Когда диагностика пройдена

Пункты 1–5 решены без подсказок и все твои `assert` проходят. Если не
получились 1–2 пункта, повтори указанные уроки и реши их снова. Если не
получилось больше половины, сначала пройди основы в Python-базе: иначе
код курса будет отвлекать от его идей.

[Разбор](../04_exercises_answers/README.md) открывай после своей попытки.
