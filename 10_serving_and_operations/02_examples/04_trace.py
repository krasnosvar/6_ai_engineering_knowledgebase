"""Крошечный регистратор spans: печатает дерево trace одного RAG-запроса.

Время учебное: вместо настоящих часов «работа» сдвигает счётчик на заданное
число миллисекунд, поэтому вывод одинаков при каждом запуске. Настоящая
библиотека трассировки (например, OpenTelemetry) берёт время из часов
системы и отправляет spans во внешнее хранилище.
"""
import contextlib
import re

clock_ms = 0          # учебные часы
stack = []            # открытые spans: последний — текущий родитель
finished = []         # закрытые корневые spans


def work(ms):
    """Имитирует работу длиной ms миллисекунд."""
    global clock_ms
    clock_ms += ms


SECRET = re.compile(r'sk-[A-Za-z0-9]+')


def redact(value):
    """Маскирует строки, похожие на ключ API, до записи в лог."""
    return SECRET.sub('sk-***', value) if isinstance(value, str) else value


@contextlib.contextmanager
def span(name, **attrs):
    """Открывает span; вложенный with становится его ребёнком."""
    # Маскируем секреты сразу при записи: в хранилище они не попадут.
    attrs = {k: redact(v) for k, v in attrs.items()}
    node = {'name': name, 'attrs': attrs, 'start': clock_ms, 'children': []}
    if stack:
        stack[-1]['children'].append(node)
    stack.append(node)
    try:
        yield node
    finally:
        node['end'] = clock_ms
        stack.pop()
        if not stack:
            finished.append(node)


def show(node, depth=0):
    duration = node['end'] - node['start']
    attrs = ' '.join(f'{k}={v}' for k, v in node['attrs'].items())
    line = f"{'  ' * depth}{node['name']:<{24 - 2 * depth}} {duration:>5} мс  "
    print((line + attrs).rstrip())
    for child in node['children']:
        show(child, depth + 1)


def handle_request(question):
    with span('request', prompt_version='v7', question=question):
        with span('retrieve', top_k=3) as r:
            with span('embed_query'):
                work(20)
            with span('vector_search'):
                work(90)
            r['attrs']['doc_ids'] = 'd12,d40,d41'
        with span('llm.generate', model='toy-1b', tokens_in=1850,
                  tokens_out=120) as g:
            work(400)                      # prefill до первого токена
            g['attrs']['ttft_ms'] = clock_ms - g['start']
            work(119 * 20)                 # ещё 119 токенов по 20 мс
        with span('check_citations'):
            work(15)


if __name__ == '__main__':
    handle_request('ключ sk-abc123 не работает, почему?')
    show(finished[0])
