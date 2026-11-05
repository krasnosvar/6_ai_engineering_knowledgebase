# Контракт ответа, стоимость вызова и память модели

Профиль CPU, только стандартная библиотека Python, без весов и сети.
Ориентир: 2–3 часа плюс отчёт. Задания 1–2 можно делать после урока 1,
остальные — после урока, указанного в задании. Решения пиши в
[task.py](task.py), не меняя имён и порядка аргументов функций.

## Задание 1. Строгий разбор ответа

**Тема:** [проверка ответа по слоям](../01_theory/01_structured_output.md).

**Дано:** строка `raw` — ответ модели.

**Сделать:** `parse_ticket(raw)` возвращает словарь, если `raw` — JSON-объект
ровно с полями `ticket_id` и `label`, где `ticket_id` — непустая строка, а
`label` — одно из `database`, `network`, `access`, `unknown`.

**Ожидаемые ValueError:** не JSON (`'prose'`), не объект (`'[]'`), нет
поля, лишнее поле, ID не строка, чужая категория. `json.loads` на тексте,
который не является JSON, сам бросает `json.JSONDecodeError` — это
подкласс `ValueError`, так что этот случай уже подходит. Не извлекай JSON
из прозы и не исправляй значения молча.

## Задание 2. Остаток окна контекста

**Тема:** [«Уложимся в контекст»](../01_theory/01_structured_output.md).

**Дано:** `limit` — окно контекста, `input_tokens` — вход,
`reserved_output` — резерв на ответ.

**Сделать:** `remaining_tokens(limit, input_tokens, reserved_output)`
возвращает `limit - input_tokens - reserved_output`. Пример из проверки:
`100 - 60 - 20 = 20`.

**Ожидаемые ValueError:** любое значение не целое или меньше 0; результат
меньше 0 (бюджет превышен). `True` тоже недопустим: `bool` в Python —
подкласс `int`, поэтому проверяй `type(x) is not int`, а не `isinstance`.

## Задание 3. Валидный, но неверный ответ (отчёт)

**Тема:** урок 1, слой 4 проверки — смысл.

Напиши пять ответов, которые проходят `parse_ticket`, но неверны по
смыслу (например, чужой `ticket_id` или `database` для «забыл пароль»), и
опиши, какими данными или проверкой их поймать. Это задание не
проверяется `check.py`. Пример с моделью (`01_generate.py`) — позже, после
ручной подготовки весов.

## Задание 4. Стоимость вызова

**Тема:** [расчёт стоимости и кэш](../01_theory/04_api_tokens_cost_caching.md).

**Дано:** число входных, выходных и закэшированных токенов и словарь цен
`prices` за миллион токенов с ключами `input`, `cached_input`, `output`.

**Сделать:** `call_cost(input_tokens, output_tokens, cached_tokens, prices)`
по формуле урока. `cached_tokens` — часть входа, а не добавка к нему: для
1500 входных, из них 1200 из кэша, и 200 выходных при ценах 1 / 0.1 / 4
ответ `0.00122`. Цены в проверках выдуманные, как в уроке.

**Ожидаемые ValueError:** токены не целые, отрицательные или `bool`;
`cached_tokens > input_tokens`; в `prices` лишний или недостающий ключ;
цена отрицательная, не конечная (`inf`, `nan`) или не число (например,
строка `'4'`).

## Задание 5. Разделители для недоверенного текста

**Тема:** [разделители](../01_theory/03_prompting_and_context.md).

**Сделать:** `wrap_untrusted(text, tag)` возвращает
`<tag>\ntext\n</tag>`, где каждое `</tag>` внутри текста заменено на
`</ tag>`. Текст пользователя не выбрасывается.

**Ожидаемые ValueError:** `text` не строка; `tag` пустой или содержит не
только строчные латинские буквы (`'Ticket'`, `'tic>ket'`). В отчёте
объясни, почему разделители снижают риск prompt injection, но не
устраняют его.

## Задание 6. Память под веса

**Тема:** [расчёт памяти](../01_theory/05_local_runtimes.md).

**Сделать:** `weights_memory_gb(params, bits)` — память в GB (10⁹ байтов):
`params × bits / 8 / 10⁹`. Для 7 млрд параметров при 16 битах — 14.

**Ожидаемые ValueError:** аргумент не целый или не больше 0, а также
`bool`. `7e9` — это float, поэтому пиши `7_000_000_000`. В отчёте объясни,
почему реальный файл Q4 больше результата и что ещё займёт память при
запуске.

## Как проверить

Из корня репозитория:

```bash
uv run python 5_llm_applications/03_exercises/check.py
```

Пока функция не написана, она бросает `NotImplementedError` — это
ожидаемое начальное состояние. Проверка идёт по порядку заданий, поэтому
первым упадёт `parse_ticket`. `AssertionError` с текстом
`Expected ValueError` значит, что функция приняла недопустимый вход.
Успех — строка `PASS: 5_llm_applications student`. Отчёт по заданиям 3,
5 и 6 оформи по [шаблону](../../other/experiment_template.md).

Если исключения незнакомы, см. [урок об
исключениях](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/1_python_fundamentals/07_exceptions/01_theory/01_exceptions.md);
`json.loads` — [урок о
json](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/6_standard_library/01_theory/05_json_csv_serialization.md);
`type()` — [урок о
типах](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/1_python_fundamentals/01_variables_and_types/01_theory/01_variables_and_types.md).

[Решения](../04_exercises_answers/README.md) открывай после самостоятельной
попытки.
