# Безопасный исполнитель

1. Реализуй `validate_action(action)`. Разрешён словарь ровно с ключами
   tool/arguments, tool=read_metrics, arguments ровно с service=demo. Всё
   остальное — `ValueError`. Возвращай arguments. Ни `eval`, ни shell
   применять нельзя (почему — в [уроке](../01_theory/01_tool_calling.md)).
2. Реализуй `may_continue(steps,limit,cancelled)` — True только при
   steps<limit и cancelled=False; steps>=0, limit>0 целые, cancelled bool.
   Иначе `ValueError`.
3. Опиши, что делать после timeout изменяющего внешнего действия:
   неизвестный исход не равен гарантированному отсутствию эффекта.
4. Реализуй `handle_jsonrpc(request, tools, allowed)` — ответ хоста в
   стиле MCP из [урока о MCP](../01_theory/03_mcp.md). `tools` — словарь
   «имя → функция(arguments) → текст», `allowed` — множество имён,
   разрешённых хостом. Запрос — словарь с `jsonrpc='2.0'`, ключом `id`,
   строкой `method` и необязательным словарём `params`; иначе
   `ValueError`. Ответ — `{'jsonrpc': '2.0', 'id': <id запроса>}` плюс
   `result` или `error` (`{'code': ..., 'message': ...}`):
   - `tools/list` → `result` `{'tools': [...]}`: отсортированные имена,
     которые есть и в `tools`, и в `allowed`;
   - `tools/call` без строки `name` или словаря `arguments` в `params` →
     error `-32602`, `'Invalid params'`;
   - имя не в `allowed` → error `-32000`, `'Tool not allowed'`; функцию
     при этом не вызывать;
   - разрешено, но нет в `tools` → error `-32602`, `'Unknown tool'`;
   - функция вернула текст → `result` `{'isError': False, 'content':
     [{'type': 'text', 'text': текст}]}`; бросила `ValueError` → то же с
     `'isError': True` и текстом ошибки `str(exc)`;
   - любой другой метод → error `-32601`, `'Method not found'`.
5. Реализуй `agent_tokens(system, per_step, steps)` — входные токены
   одного агента по формуле из [урока о нескольких
   агентах](../01_theory/04_multi_agent_and_memory.md), и
   `multi_agent_cost(system, per_step, steps, workers, summary)` —
   `workers` исполнителей по `steps` шагов плюс два вызова оркестратора:
   план (`system`) и итог (`system` и `workers` сводок по `summary`
   токенов). Все аргументы — положительные целые, иначе `ValueError`.
   Проверь себя на числах урока: 19500, 112500, 63400. Затем найди, при
   каком числе областей (`workers`, у одного агента `6 × workers` шагов)
   оркестратор становится дешевле одного агента.

CPU; 2–3 часа. MODEL-пример отложен до ручного скачивания модели.

`raise ValueError('описание')` — так функция сообщает «мне дали неверные
данные» и останавливается; `check.py` проверяет, что ошибка действительно
возникает. Если исключения ещё не знакомы — см. минимум Python в
[0_lab_setup](../../0_lab_setup/README.md).

## Выполнение

Дополни `task.py`, затем из корня репы:

```bash
uv run python 9_agents_and_tools/03_exercises/check.py
```

До реализации ожидается `NotImplementedError`. Проверки должны пройти для
твоего кода. Сохрани объяснения и результаты изменённого эксперимента по
[шаблону отчёта](../../other/experiment_template.md).

[Решения](../04_exercises_answers/README.md) открывай после самостоятельной
попытки.
