# Источники и обновление курса

Теоретическая редакция проверена 2026-11-04. Изложение авторское; ссылки служат
первоисточниками и дальнейшим чтением. Курс не является переводом одного
источника. Базовые алгоритмы стабильнее API библиотек и модельных рейтингов.

| Раздел | Первоисточник |
|---|---|
| ML, утечки, pipeline | [scikit-learn](https://scikit-learn.org/stable/common_pitfalls.html) |
| Нейросети, autograd | [PyTorch basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html) |
| Attention | [Attention Is All You Need](https://arxiv.org/abs/1706.03762) |
| NLP, токенизация, LLM | [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/chapter1/1) |
| Генерация и chat templates | [Transformers](https://huggingface.co/docs/transformers/chat_templating) |
| Длинный контекст | [Lost in the Middle](https://arxiv.org/abs/2307.03172) |
| Локальный запуск | [llama.cpp](https://github.com/ggml-org/llama.cpp), [Ollama](https://github.com/ollama/ollama) |
| RAG | [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401) |
| Векторный поиск | [HNSW](https://arxiv.org/abs/1603.09320), [FAISS](https://github.com/facebookresearch/faiss), [pgvector](https://github.com/pgvector/pgvector) |
| Модель-судья | [Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685) |
| Prompt injection | [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) |
| LoRA | [Статья](https://arxiv.org/abs/2106.09685), [PEFT](https://huggingface.co/docs/peft/quicktour) |
| QLoRA | [Статья](https://arxiv.org/abs/2305.14314) |
| DPO | [Статья](https://arxiv.org/abs/2305.18290) |
| Агенты | [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) |
| Оценка агентов | [Demystifying evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) |
| MCP | [Спецификация](https://modelcontextprotocol.io/specification/latest), [JSON-RPC 2.0](https://www.jsonrpc.org/specification) |
| Serving | [vLLM](https://docs.vllm.ai/en/latest/) |
| Наблюдаемость LLM | [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) |
| Intel GPU | [PyTorch XPU](https://docs.pytorch.org/docs/2.8/notes/get_start_xpu.html) |
| Учебная модель | [SmolLM2-135M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-135M-Instruct) |

## Процедура обновления

1. Проверить первоисточник и changelog изменившегося API.
2. Обновить пример и точные зависимости в отдельном изменении; пересоздать
   `uv.lock`.
3. Запустить CPU-примеры изменённых разделов и `03_exercises/check.py --answers`
   в каждом разделе; при изменении модельного пути — MODEL-примеры.
4. Сравнить сохранённые evals, описать новые ошибки и различия.
5. Обновить дату редакции в разделе «Актуальность» корневого README.

Не менять модель на лидера рейтинга автоматически. Для новой модели проверить
лицензию, доступ без учётной записи, язык, размер, chat template,
CPU-совместимость и повторить лабы. Новый revision весов — изменение
эксперимента, даже если имя модели осталось тем же.

## Где повторить незнакомое понятие

Таблица «термин → урок» вынесена в [словарь терминов](glossary.md).
