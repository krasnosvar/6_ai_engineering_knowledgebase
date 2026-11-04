# Примеры и эксперименты

Команды из корня репы после установки зависимостей. CPU-примеры не требуют
весов. MODEL и embedding читают только локальные файлы:
[где взять модели](../../data/models.md). Пока веса не подготовлены, эти
команды завершаются с пояснением; это не успешный запуск. Для каждого опыта
сначала предскажи результат, затем измени одно условие.

## 01_memory.py

Профиль: **CPU**. Оценки памяти; удвоение контекста удваивает KV cache.

```bash
uv run python 10_serving_and_operations/02_examples/01_memory.py
```

Сравни число KV-heads и query-heads.

## 02_benchmark.py

Профиль: **MODEL**. Прогрев отдельно и три end-to-end замера в
`artifacts/benchmark.json`.

```bash
uv run python 10_serving_and_operations/02_examples/02_benchmark.py
```

Не называй полный generate временем первого токена.

## 03_release_gate.py

Профиль: **CPU**. Качество и скорость не компенсируют провал авторизации;
видны причины отказа выпуска.

```bash
uv run python 10_serving_and_operations/02_examples/03_release_gate.py
```

Добавь минимальный размер eval-набора и критерий отката; пороги выбери до
test.
