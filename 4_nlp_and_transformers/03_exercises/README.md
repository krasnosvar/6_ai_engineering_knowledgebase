# Устойчивая нормализация и причинная маска

Профиль CPU, только стандартная библиотека Python, без весов и сети.
Ориентир: 2–3 часа вместе с экспериментом.

## Задание 1. Устойчивый softmax

**Тема:** softmax из [урока о
нейроне](../../3_neural_networks/01_theory/01_neurons_and_backprop.md),
который используется в [attention](../01_theory/02_attention.md).

**Дано:** список чисел `values` — оценки (logits).

**Сделать:** функцию `softmax(values)` в `task.py`, которая возвращает
список долей той же длины с суммой 1. Используй `math.exp`, без NumPy.
Числа порядка 1000 не должны вызывать переполнение: `math.exp(1000)`
бросает `OverflowError`. Приём «вычти максимум перед экспонентой»
разобран вручную в уроке о нейроне.

**Ожидаемые ValueError:** пустой список; значение `inf`, `-inf` или `nan`
(проверка — `math.isfinite`).

## Задание 2. Причинная маска

**Тема:** causal mask из [урока об attention](../01_theory/02_attention.md).

**Дано:** целое число позиций `length`.

**Сделать:** функцию `causal_allowed(length)` в `task.py`. Она возвращает
квадратный список списков `bool`: в строке i значение `True` у столбцов
`j <= i` (себя и прошлое видно), `False` — у будущих. Для `length=3`
результат — нижний треугольник из `True`, как в уроке.

**Ожидаемые ValueError:** `length` меньше 1 или не целое число. `True` тоже
должно давать ValueError: в Python `bool` — подкласс `int`, поэтому
`isinstance(True, int)` вернёт `True`. Подумай, какая проверка типа это
отличит.

## Задание 3. Эксперимент с головами и маской

**Тема:** [блок Transformer](../01_theory/03_transformer_block.md) и
[обучение языковой
модели](../01_theory/04_architectures_and_lm_training.md).

**Сделать:** в копии
[03_tiny_transformer.py](../02_examples/03_tiny_transformer.py) измени число
голов так, чтобы `d_model=32` делилось на него, и сравни конечный loss. Затем
замени `src_mask=mask` на `src_mask=None` и заранее предскажи, какая строка
упадёт. Ожидаемо — `assert torch.allclose(...)` после обучения: без маски ранние
позиции видят изменённый последний символ, и их предсказания меняются. В отчёте
объясни, почему даже низкий train loss модели, которая подсматривает будущее, —
не достижение. Это задание не проверяется `check.py`: результат — твой отчёт по
[шаблону](../../other/experiment_template.md).

## Как проверить задания 1–2

Пиши решение в [task.py](task.py), не меняя имён функций. Затем из корня
репозитория:

```bash
uv run python 4_nlp_and_transformers/03_exercises/check.py
```

Пока функция не написана, она бросает `NotImplementedError` — это
ожидаемое начальное состояние, а не ошибка установки. `AssertionError` с
текстом `Expected ValueError` значит, что функция приняла недопустимый вход
вместо отказа. Успех — строка `PASS: 4_nlp_and_transformers student`.

`raise ValueError("...")` — так функция сообщает «мне дали недопустимый вход» и
сразу прекращает работу. Если исключения пока незнакомы, см. [урок об
исключениях](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/1_python_fundamentals/07_exceptions/01_theory/01_exceptions.md);
проверку типов через `type` и `isinstance` — в [уроке о
типах](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/1_python_fundamentals/01_variables_and_types/01_theory/01_variables_and_types.md).

[Решения](../04_exercises_answers/README.md) открывай после самостоятельной
попытки.
