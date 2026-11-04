# Градиенты и masked pooling

1. Реализуй `one_step(model,optimizer,x,y)` для классификатора PyTorch. Обнули
   градиенты, вычисли cross entropy по logits, backward и шаг, верни float loss.
2. Реализуй `masked_mean(hidden,mask)`: hidden имеет форму (B,T,D), mask — (B,T)
   с 0/1. Верни (B,D), усредняя только позиции с 1. Полностью пустая строка —
   ValueError. Обозначения: B — число последовательностей в batch, T — длина
   последовательности (число позиций, включая добавленные пустые), D — длина
   вектора в каждой позиции. Приём с маской разобран в уроке [о
   стабильности](../01_theory/05_stability_and_checkpoints.md), оси и
   суммирование по оси — в уроке [массивы и
   оси](../../1_math_and_data/01_theory/04_arrays_and_axes.md). `ValueError`
   поднимается командой `raise ValueError('текст')`.
3. Объясни, почему model.eval() не заменяет no_grad(). CPU, PyTorch; 2–3 часа.
   Дополнительный опыт: убери zero_grad и сравни два шага.

## Выполнение

Дополни `task.py`, затем из корня репы:

```bash
uv run python 3_neural_networks/03_exercises/check.py
```

До реализации ожидается `NotImplementedError`. Проверки должны пройти для твоего
кода. Сохрани объяснения и результаты изменённого эксперимента по [шаблону
отчёта](../../other/experiment_template.md).

[Решения](../04_exercises_answers/README.md) открывай после самостоятельной
попытки.
