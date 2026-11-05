# Словарь терминов: где что объяснено

Эта страница нужна, чтобы вернуться к объяснению забытого слова. У каждого
понятия в курсе один «домашний» урок, где оно разобрано с нуля и на
примере; остальные уроки дают короткое пояснение и ссылку туда. Читать
таблицу до начала курса не нужно.

| Если встретилось слово | Куда вернуться |
|---|---|
| Baseline, обучение, инференс, AI/ML/NLP/LLM | [Как компьютер учится на примерах](../1_math_and_data/01_theory/00_rules_and_learning.md) |
| Python: какие темы нужны и где их повторить | [Какой Python нужен для курса](../0_lab_setup/python_minimum.md) |
| Зачем математика ML-инженеру | [Назначение математики](../1_math_and_data/01_theory/01_why_math.md) |
| Данные, предсказание, ошибка, параметры, MAE | [Предсказание, ошибка, параметры](../1_math_and_data/01_theory/02_prediction_and_error.md) |
| Вектор, скалярное произведение, линейная модель | [Векторы](../1_math_and_data/01_theory/03_vectors_and_linear_model.md) |
| Матрица, форма, умножение на вектор | [Матрицы](../1_math_and_data/01_theory/04_matrices.md) |
| Косинусное сходство | [Косинус](../1_math_and_data/01_theory/05_cosine.md) |
| Производная, частная производная, цепное правило | [Изменение параметра](../1_math_and_data/01_theory/06_derivatives.md) |
| MSE, loss, градиент, learning rate | [Ошибка и градиент](../1_math_and_data/01_theory/07_gradients.md) |
| Среднее, медиана, дисперсия, стандартное отклонение | [Среднее и разброс](../1_math_and_data/01_theory/08_descriptive_statistics.md) |
| Вероятность, условная вероятность, формула Байеса | [Вероятность и условие](../1_math_and_data/01_theory/09_probability.md) |
| Стандартная ошибка доли, bootstrap (идея) | [Неопределённость оценки](../1_math_and_data/01_theory/10_uncertainty_and_data.md) |
| Форма массива, оси, broadcasting | [Массивы и оси](../1_math_and_data/01_theory/11_arrays_and_axes.md) |
| Матричное умножение, форма тензоров | [Операции с тензорами](../1_math_and_data/01_theory/12_tensor_operations.md) |
| Стандартизация, масштаб признаков | [Стандартизация](../1_math_and_data/01_theory/13_standardization.md) |
| exp, ln, цепное правило вероятности | [Экспонента и логарифм](../1_math_and_data/01_theory/14_exp_and_log.md) |
| Сигмоида, softmax, логарифмическая потеря | [Вероятности классов](../1_math_and_data/01_theory/15_classification_probabilities.md) |
| Logits, logprobs, temperature, perplexity | [Вероятности токенов](../1_math_and_data/01_theory/16_llm_probabilities.md) |
| Признак, метка, класс, классификатор, TF-IDF, логистическая регрессия, scikit-learn `fit`/`predict`, Pipeline, дерево, случайный лес, boosting | [Классификация текста](../2_classical_ml/01_theory/01_classification_basics.md) |
| Train, validation, test, утечка, гиперпараметр, accuracy | [Как проверить новые обращения](../2_classical_ml/01_theory/02_model_selection.md) |
| Confusion matrix, precision, recall, F1, macro F1, порог, калибровка, coverage | [Ошибки и их последствия](../2_classical_ml/01_theory/03_metrics.md) |
| Кросс-валидация, fold, GroupKFold | [Перекрёстная проверка](../2_classical_ml/01_theory/04_cross_validation.md) |
| Недообучение, переобучение, L2, learning curve | [Регуляризация](../2_classical_ml/01_theory/05_regularization.md) |
| Нейрон, слой, ReLU, backprop, устойчивый softmax, cross entropy | [Нейрон и обратное распространение](../3_neural_networks/01_theory/01_neurons_and_backprop.md) |
| Тензор, autograd, граф вычислений, `nn.Module` | [PyTorch с нуля](../3_neural_networks/01_theory/02_pytorch_basics.md) |
| Batch, epoch, накопление градиента, BatchNorm | [Организация обучения сети](../3_neural_networks/01_theory/03_batches_and_training_loop.md) |
| Dropout, `train()`/`eval()`, `inference_mode`, early stopping | [Переобучение и проверка](../3_neural_networks/01_theory/04_overfitting_and_validation.md) |
| Token, BPE, embedding, padding, truncation | [Путь от текста к числам](../4_nlp_and_transformers/01_theory/01_tokenization.md) |
| Attention, Q/K/V, causal mask | [Связи между позициями текста](../4_nlp_and_transformers/01_theory/02_attention.md) |
| Clipping, masked mean, warmup, `state_dict`, checkpoint | [Стабильность и сохранение](../3_neural_networks/01_theory/05_stability_and_checkpoints.md) |
| Multi-head, residual, LayerNorm, RoPE, pre-norm | [Блок Transformer](../4_nlp_and_transformers/01_theory/03_transformer_block.md) |
| Encoder, decoder, perplexity | [Архитектуры и обучение LM](../4_nlp_and_transformers/01_theory/04_architectures_and_lm_training.md) |
| Temperature, sampling | [Жизненный цикл модели](../4_nlp_and_transformers/01_theory/05_model_lifecycle.md) |
| Prompt, few-shot, chat template, structured output, JSON Schema, constrained decoding | [Структурированный ответ](../5_llm_applications/01_theory/01_structured_output.md) |
| Timeout, retry, backoff, ключ API, rate limit | [Контракт вызова модели](../5_llm_applications/01_theory/02_runtime_contract.md) |
| Prompt/context engineering, динамический few-shot, lost in the middle, разделители недоверенных данных, версия prompt | [Prompt и контекст](../5_llm_applications/01_theory/03_prompting_and_context.md) |
| Окно контекста, стоимость вызова, prompt caching в API, batch API, каскад моделей, usage | [Токены, стоимость и кэширование](../5_llm_applications/01_theory/04_api_tokens_cost_caching.md) |
| llama.cpp, Ollama, LM Studio, OpenAI-совместимый endpoint | [Локальный запуск моделей](../5_llm_applications/01_theory/05_local_runtimes.md) |
| RAG, источник, grounding, Recall@k, MRR | [Ответ по своим документам](../6_retrieval_and_rag/01_theory/01_rag_basics.md) |
| BM25, dense retrieval, pooling, RRF, reranker | [Ранжирование](../6_retrieval_and_rag/01_theory/03_ranking.md) |
| ANN, IVF, HNSW, FAISS, pgvector, векторная база | [Векторные хранилища](../6_retrieval_and_rag/01_theory/04_vector_stores.md) |
| Eval, рубрика | [Проверка качества приложения](../7_evaluation_and_safety/01_theory/01_free_text_evaluation.md) |
| Парный bootstrap, интервал, срез | [Сравнение версий](../7_evaluation_and_safety/01_theory/02_comparing_versions.md) |
| Agreement, Cohen's kappa, критерии выпуска | [Судьи и выпуск](../7_evaluation_and_safety/01_theory/03_judges_and_release.md) |
| LLM-as-judge, pointwise/pairwise, позиционное смещение, verbosity bias, self-preference, калибровка судьи | [LLM как судья](../7_evaluation_and_safety/01_theory/04_llm_as_judge.md) |
| Prompt injection (прямая/косвенная), guardrails, allow-list, разделение привилегий | [Guardrails и prompt injection](../7_evaluation_and_safety/01_theory/05_guardrails_and_injection.md) |
| SFT, labels `-100`, сдвиг целей | [Когда нужно дообучение](../8_fine_tuning/01_theory/01_sft_basics.md) |
| Packing, обрезка диалогов | [Подготовка данных](../8_fine_tuning/01_theory/02_data_preparation.md) |
| LoRA, ранг, alpha, адаптер, merge | [Обучение небольшой поправки](../8_fine_tuning/01_theory/03_lora.md) |
| QLoRA, квантизация, деквантизация, масштаб группы, NF4 | [Как хранятся веса](../8_fine_tuning/01_theory/04_qlora.md) |
| DPO, reference model, policy, RLHF, reward hacking | [Обучение по предпочтениям](../8_fine_tuning/01_theory/05_preferences.md) |
| Workflow, агент, tool calling, роль `tool` | [Модель и инструменты](../9_agents_and_tools/01_theory/01_tool_calling.md) |
| Идемпотентность, повтор действия | [Состояние и повторы](../9_agents_and_tools/01_theory/02_state_and_retries.md) |
| MCP, host/client/server, JSON-RPC, tool poisoning | [MCP](../9_agents_and_tools/01_theory/03_mcp.md) |
| Orchestrator–worker, subagent, изоляция контекста, память агента | [Несколько агентов и память](../9_agents_and_tools/01_theory/04_multi_agent_and_memory.md) |
| Serving, KV cache, TTFT, TPOT | [Обслуживание запросов](../10_serving_and_operations/01_theory/01_serving_basics.md) |
| vLLM, PagedAttention, prefix caching, GGUF, speculative decoding | [Как serving-движки экономят ресурсы](../10_serving_and_operations/01_theory/02_inference_optimizations.md) |
| Drift, выпуск, откат, p95 (nearest rank), SLO, shadow, canary | [Изменения данных и версий](../10_serving_and_operations/01_theory/03_release_and_drift.md) |
| Observability, trace, span, OpenTelemetry, head/tail sampling | [Наблюдаемость LLM](../10_serving_and_operations/01_theory/04_llm_observability.md) |
| Свёртка, kernel, padding, stride, pooling, аугментация | [Основы свёрток](../11_multimodal_and_cv/01_theory/01_convolutions_basics.md) |
| IoU, Dice, OCR, VLM, перенос обучения | [Следующие шаги в CV](../11_multimodal_and_cv/01_theory/02_next_steps.md) |
| Карточка проекта, baseline проекта, рубрика | [Как вести проект](../12_capstones/01_theory/01_project_workflow.md) |

[К оглавлению](../README.md).
