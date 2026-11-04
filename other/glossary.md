# Словарь терминов: где что объяснено

Эта страница нужна, чтобы вернуться к объяснению забытого слова. У каждого
понятия в курсе один «домашний» урок, где оно разобрано с нуля и на
примере; остальные уроки дают короткое пояснение и ссылку туда. Читать
таблицу до начала курса не нужно.

| Если встретилось слово | Куда вернуться |
|---|---|
| Baseline, обучение, инференс | [Первое решение и применение модели](../0_lab_setup/01_theory/01_rules_and_learning.md) |
| Функции, словари, исключения, классы в Python | [Минимум Python для курса](../0_lab_setup/python_minimum.md) |
| Вектор, матрица, cosine | [Представление задачи числами](../1_math_and_data/01_theory/01_vectors_and_linear_model.md) |
| Loss, градиент, learning rate | [Один шаг изменения весов](../1_math_and_data/01_theory/02_gradients.md) |
| Форма массива, оси, broadcasting | [Массивы и оси](../1_math_and_data/01_theory/04_arrays_and_axes.md) |
| exp, ln, sigmoid, `-ln(p)`, цепное правило вероятности | [Экспонента и логарифм](../1_math_and_data/01_theory/05_exp_and_log.md) |
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
| Prompt, few-shot, chat template, structured output | [Структурированный ответ](../5_llm_applications/01_theory/01_structured_output.md) |
| Timeout, retry, backoff, ключ API, rate limit | [Контракт вызова модели](../5_llm_applications/01_theory/02_runtime_contract.md) |
| RAG, источник, grounding | [Ответ по своим документам](../6_retrieval_and_rag/01_theory/01_rag_basics.md) |
| Eval, рубрика, prompt injection | [Проверка качества приложения](../7_evaluation_and_safety/01_theory/01_free_text_evaluation.md) |
| LoRA, ранг, адаптер | [Обучение небольшой поправки](../8_fine_tuning/01_theory/03_lora.md) |
| QLoRA, квантизация | [Как хранятся веса](../8_fine_tuning/01_theory/04_qlora.md) |
| Workflow, агент, tool calling, роль `tool`, MCP | [Модель и инструменты](../9_agents_and_tools/01_theory/01_tool_calling.md) |
| Идемпотентность, повтор действия | [Состояние и повторы](../9_agents_and_tools/01_theory/02_state_and_retries.md) |
| Serving, KV cache, TTFT, TPOT | [Обслуживание запросов](../10_serving_and_operations/01_theory/01_serving_basics.md) |
| vLLM, PagedAttention, prefix caching, GGUF, speculative decoding | [Как serving-движки экономят ресурсы](../10_serving_and_operations/01_theory/02_inference_optimizations.md) |
| Drift, выпуск, откат | [Изменения данных и версий](../10_serving_and_operations/01_theory/03_release_and_drift.md) |
| Свёртка, kernel, padding, stride | [Основы свёрток](../11_multimodal_and_cv/01_theory/01_convolutions_basics.md) |

[К оглавлению](../README.md).
