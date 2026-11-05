# Какой Python нужен для курса

Этот курс не учит Python: язык подробно разобран в отдельной [Python-базе
серии](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/README.md).
Здесь только перечислено, какие конструкции встречаются в коде курса, где именно
и в каком уроке Python-базы их повторить.

## Как пользоваться страницей

1. Пройди [входную диагностику](03_exercises/README.md). Она занимает
   45–90 минут и проверяет то, без чего код первых разделов не прочитать.
2. Если пункт диагностики не получился, найди его тему в таблице ниже и
   прочитай указанный урок. Возвращайся к диагностике, пока не решишь все
   пункты без подсказок.
3. Темы из второй таблицы можно не учить заранее: они встречаются в
   отдельных примерах, и там кратко объяснено, зачем они нужны.

NumPy, PyTorch и scikit-learn знать заранее не нужно: они объясняются в
самом курсе: первое знакомство с NumPy — в [уроке о
матрицах](../1_math_and_data/01_theory/04_matrices.md).

## Нужно до начала

| Тема | Где встретится | Урок Python-базы |
|---|---|---|
| Функции, `return`, значения по умолчанию | каждый пример и каждое задание | [функции](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/1_python_fundamentals/06_functions_basics/01_theory/01_functions_basics.md) |
| `if`, `for`, `range` | каждый пример | [ветвления и циклы](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/1_python_fundamentals/04_control_flow/01_theory/01_control_flow.md) |
| `print` и f-строки, формат `:.3f` | вывод всех примеров | [ввод и вывод](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/1_python_fundamentals/03_input_output/01_theory/01_input_output.md) |
| Списки, словари, множества, срезы | данные обращений, метрики | [коллекции](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/1_python_fundamentals/05_collections/01_theory/01_lists_tuples_sets_dicts.md) |
| Изменяемость: почему функция не должна менять входной список | условия заданий | [изменяемость и ссылки](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/1_python_fundamentals/05_collections/01_theory/02_mutability_and_references.md) |
| Списковые выражения `[... for ... in ... if ...]` | формулы ошибок и метрик в коде | [comprehensions](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/1_python_fundamentals/05_collections/01_theory/03_comprehensions.md) |
| `raise`, `try`/`except`, `ValueError` | почти каждое задание проверяет ошибки входа | [исключения](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/1_python_fundamentals/07_exceptions/01_theory/01_exceptions.md) |
| `import`, `if __name__ == "__main__":` | запуск примеров командой `python файл.py` | [модули и import](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/1_python_fundamentals/08_modules_and_imports/01_theory/01_modules_and_imports.md) |
| `lambda` и `sorted(..., key=...)` | ранжирование документов, проверки заданий | [lambda](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/2_functions_and_decorators/01_theory/01_lambdas.md) |
| Класс, `__init__`, `self` | модели PyTorch с раздела 3 | [что такое класс](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/3_oop/01_theory/01_what_is_a_class.md) |
| Наследование и `super().__init__()` | `class Model(nn.Module)` в разделах 3, 4, 8 | [наследование](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/3_oop/01_theory/03_inheritance_and_super.md) |
| JSON | учебные данные в `data/*.json` | [json и csv](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/6_standard_library/01_theory/05_json_csv_serialization.md) |
| `pathlib.Path` | пути к данным в примерах | [pathlib](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/6_standard_library/01_theory/06_pathlib_os_filesystem.md) |
| Виртуальное окружение | `uv sync` и каталог `.venv` | [venv и pip](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/other/01_environments_and_packaging/01_theory/01_venv_and_pip.md) |

## `zip` и `enumerate`

В Python-базе нет отдельного урока об этих двух функциях, а в курсе они
встречаются часто, поэтому коротко здесь. `zip` идёт по нескольким
спискам параллельно: в формулах ошибок так берутся пары «вход —
правильный ответ». `enumerate` добавляет к элементу его номер.

```python
x = [1, 2]
y = [3, 5]
for a, t in zip(x, y):
    print(a, t)            # 1 3, затем 2 5

for number, text in enumerate(["вход", "оплата"], 1):
    print(number, text)    # 1 вход, затем 2 оплата
```

## Можно не учить заранее

Эти конструкции встречаются в одном-двух примерах. Пример работает и без
глубокого понимания; ссылка нужна, если захочешь разобраться.

| Тема | Где встретится | Урок Python-базы |
|---|---|---|
| Подсказки типов `def f(x: list) -> float` | разделы 3 и 11 | [аннотации типов](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/other/02_typing_and_static_analysis/01_theory/01_type_hints_and_mypy.md) |
| `with` и контекстные менеджеры | `with torch.inference_mode():` с раздела 3, trace в разделе 10 | [контекстные менеджеры](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/2_functions_and_decorators/01_theory/06_context_managers.md) |
| `*args`, `**kwargs` | HTTP-сервис раздела 12 | [args и kwargs](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/2_functions_and_decorators/01_theory/02_args_kwargs.md) |
| `collections.Counter` | BPE в разделе 4 | [модуль collections](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/6_standard_library/01_theory/01_collections_module.md) |
| Регулярные выражения | маскирование секретов в разделе 10 | [модуль re](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/6_standard_library/01_theory/04_re_regular_expressions.md) |
| Генераторы и `yield` | trace в разделе 10 | [генераторы](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/1_python/4_iterators_generators/01_theory/02_generators_and_yield.md) |
| HTTP-сервер | итоговые проекты, раздел 12 | [HTTP и первое приложение](https://github.com/krasnosvar/4_python_my_knowledgebase/blob/main/3_web_frameworks/1_fastapi/01_theory/01_http_and_first_app.md) |

Файлы `03_exercises/check.py` используют `argparse` и `importlib`, чтобы
загрузить твоё решение или эталон. Разбираться в них не нужно: достаточно
запускать команду из README задания.

[К разделу 0](README.md).
