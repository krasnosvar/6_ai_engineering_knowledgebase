# Словарь терминов: где что объяснено

Эта страница нужна, чтобы вернуться к объяснению забытого слова. У каждого
понятия в курсе один «домашний» урок, где оно разобрано с нуля и на
примере; остальные уроки дают короткое пояснение и ссылку туда. Читать
таблицу до начала курса не нужно.

| Если встретилось слово | Куда вернуться |
|---|---|
| Baseline, обучение, инференс | [Первое решение и применение модели](../0_lab_setup/01_theory/01_rules_and_learning.md) |
| Функции, словари, исключения, классы в Python | [Минимум Python для курса](../0_lab_setup/python_minimum.md) |
| Зачем математика LLM-инженеру | [Зачем математика](../1_math_and_data/01_theory/00_why_math.md) |
| Вектор, матрица, cosine | [Представление задачи числами](../1_math_and_data/01_theory/01_vectors_and_linear_model.md) |
| Loss, градиент, learning rate | [Один шаг изменения весов](../1_math_and_data/01_theory/02_gradients.md) |
| Стандартная ошибка доли | [Почему одного результата недостаточно](../1_math_and_data/01_theory/03_probability_and_data.md) |
| Форма массива, оси, broadcasting | [Массивы и оси](../1_math_and_data/01_theory/04_arrays_and_axes.md) |
| exp, ln, sigmoid, `-ln(p)`, цепное правило вероятности, logits, logprobs | [Экспонента и логарифм](../1_math_and_data/01_theory/05_exp_and_log.md) |
| Train, validation, test, утечка | [Как проверить новые обращения](../2_classical_ml/01_theory/02_model_selection.md) |
| Precision, recall, F1 | [Ошибки и их последствия](../2_classical_ml/01_theory/03_metrics.md) |
| Softmax | [Нейрон и обратное распространение](../3_neural_networks/01_theory/01_neurons_and_backprop.md) |
| Тензор, autograd, граф вычислений, `nn.Module` | [PyTorch с нуля](../3_neural_networks/01_theory/02_pytorch_basics.md) |
| Batch, epoch | [Организация обучения сети](../3_neural_networks/01_theory/03_batches_and_training_loop.md) |
| Dropout, `train()`/`eval()`, переобучение | [Переобучение и проверка](../3_neural_networks/01_theory/04_overfitting_and_validation.md) |
| Token, embedding, padding | [Путь от текста к числам](../4_nlp_and_transformers/01_theory/01_tokenization.md) |
| Attention, Q/K/V, causal mask | [Связи между позициями текста](../4_nlp_and_transformers/01_theory/02_attention.md) |
| Multi-head, residual, LayerNorm, RoPE, pre-norm | [Блок Transformer](../4_nlp_and_transformers/01_theory/03_transformer_block.md) |
| Encoder, decoder, perplexity | [Архитектуры и обучение LM](../4_nlp_and_transformers/01_theory/04_architectures_and_lm_training.md) |
| Temperature, sampling | [Жизненный цикл модели](../4_nlp_and_transformers/01_theory/05_model_lifecycle.md) |
| Prompt, few-shot, chat template, structured output | [Структурированный ответ](../5_llm_applications/01_theory/01_structured_output.md) |
| Timeout, retry, backoff, ключ API, rate limit | [Контракт вызова модели](../5_llm_applications/01_theory/02_runtime_contract.md) |
| Prompt/context engineering, динамический few-shot, lost in the middle, разделители недоверенных данных, версия prompt | [Prompt и контекст](../5_llm_applications/01_theory/03_prompting_and_context.md) |
| Окно контекста, стоимость вызова, prompt caching в API, batch API, каскад моделей, usage | [Токены, стоимость и кэширование](../5_llm_applications/01_theory/04_api_tokens_cost_caching.md) |
| llama.cpp, Ollama, LM Studio, OpenAI-совместимый endpoint | [Локальный запуск моделей](../5_llm_applications/01_theory/05_local_runtimes.md) |
| RAG, источник, grounding | [Ответ по своим документам](../6_retrieval_and_rag/01_theory/01_rag_basics.md) |
| ANN, IVF, HNSW, FAISS, pgvector, векторная база | [Векторные хранилища](../6_retrieval_and_rag/01_theory/04_vector_stores.md) |
| Eval, рубрика | [Проверка качества приложения](../7_evaluation_and_safety/01_theory/01_free_text_evaluation.md) |
| Agreement, Cohen's kappa, критерии выпуска | [Судьи и выпуск](../7_evaluation_and_safety/01_theory/03_judges_and_release.md) |
| LLM-as-judge, pointwise/pairwise, позиционное смещение, verbosity bias, self-preference, калибровка судьи | [LLM как судья](../7_evaluation_and_safety/01_theory/04_llm_as_judge.md) |
| Prompt injection (прямая/косвенная), guardrails, allow-list, разделение привилегий | [Guardrails и prompt injection](../7_evaluation_and_safety/01_theory/05_guardrails_and_injection.md) |
| LoRA, ранг, адаптер | [Обучение небольшой поправки](../8_fine_tuning/01_theory/03_lora.md) |
| QLoRA, квантизация | [Как хранятся веса](../8_fine_tuning/01_theory/04_qlora.md) |
| Workflow, агент, tool calling, роль `tool` | [Модель и инструменты](../9_agents_and_tools/01_theory/01_tool_calling.md) |
| Идемпотентность, повтор действия | [Состояние и повторы](../9_agents_and_tools/01_theory/02_state_and_retries.md) |
| MCP, host/client/server, JSON-RPC, tool poisoning | [MCP](../9_agents_and_tools/01_theory/03_mcp.md) |
| Orchestrator–worker, subagent, изоляция контекста, память агента | [Несколько агентов и память](../9_agents_and_tools/01_theory/04_multi_agent_and_memory.md) |
| Serving, KV cache, TTFT, TPOT | [Обслуживание запросов](../10_serving_and_operations/01_theory/01_serving_basics.md) |
| vLLM, PagedAttention, prefix caching, GGUF, speculative decoding | [Как serving-движки экономят ресурсы](../10_serving_and_operations/01_theory/02_inference_optimizations.md) |
| Drift, выпуск, откат | [Изменения данных и версий](../10_serving_and_operations/01_theory/03_release_and_drift.md) |
| Observability, trace, span, OpenTelemetry, head/tail sampling | [Наблюдаемость LLM](../10_serving_and_operations/01_theory/04_llm_observability.md) |
| Свёртка, kernel, padding, stride | [Основы свёрток](../11_multimodal_and_cv/01_theory/01_convolutions_basics.md) |

[К оглавлению](../README.md).
