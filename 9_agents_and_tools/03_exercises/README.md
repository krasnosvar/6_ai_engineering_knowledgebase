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

CPU; 1–2 часа. MODEL-пример отложен до ручного скачивания модели.

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
