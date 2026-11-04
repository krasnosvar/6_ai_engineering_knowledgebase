"""Проверка упражнения. Без флага проверяет task.py, с --answers — эталон."""
import argparse
import importlib.util
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--answers', action='store_true')
options = parser.parse_args()

folder = Path(__file__).resolve().parent
if options.answers:
    source = folder.parent / '04_exercises_answers/solution.py'
else:
    source = folder / 'task.py'

# Загружаем файл с решением как модуль m, чтобы вызывать его функции:
# m.validate_action(...)
spec = importlib.util.spec_from_file_location('student', source)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def expect_value_error(fn):
    """Вызывает fn() и требует, чтобы она бросила ValueError."""
    try:
        fn()
    except ValueError:
        return  # ожидаемая ошибка — проверка пройдена
    raise AssertionError('Expected ValueError')


good_action = {'tool': 'read_metrics', 'arguments': {'service': 'demo'}}
assert m.validate_action(good_action) == {'service': 'demo'}

bad_actions = (
    # чужой инструмент
    {'tool': 'shell', 'arguments': {}},
    # чужой сервис
    {'tool': 'read_metrics', 'arguments': {'service': 'private'}},
    # лишнее поле
    {'tool': 'read_metrics', 'arguments': {'service': 'demo', 'cmd': 'x'}},
    # не словарь
    [],
)
for a in bad_actions:
    # `lambda a=a:` фиксирует ТЕКУЩЕЕ a в момент создания функции. Без `a=a`
    # лямбда брала бы a в момент вызова; здесь вызов сразу, но в отложенных
    # вызовах все лямбды увидели бы последнее значение цикла.
    expect_value_error(lambda a=a: m.validate_action(a))

assert m.may_continue(0, 2, False)
assert not m.may_continue(2, 2, False)   # бюджет исчерпан
assert not m.may_continue(0, 2, True)    # задачу отменили
expect_value_error(lambda: m.may_continue(-1, 2, False))

# --- handle_jsonrpc: сервер знает два инструмента, хост разрешил один ---
calls = []  # имена инструментов, которые реально запускались


def read_metrics(arguments):
    calls.append('read_metrics')
    if arguments.get('service') != 'demo':
        raise ValueError('unknown service')
    return 'error_rate=0.15'


def restart_service(arguments):
    calls.append('restart_service')
    return 'restarted'


tools = {'restart_service': restart_service, 'read_metrics': read_metrics}
allowed = {'read_metrics', 'create_ticket'}


def rpc(rid, method, params=None):
    """Собирает запрос и передаёт его функции студента."""
    request = {'jsonrpc': '2.0', 'id': rid, 'method': method}
    if params is not None:
        request['params'] = params
    return m.handle_jsonrpc(request, tools, allowed)


def call(rid, name, arguments):
    return rpc(rid, 'tools/call', {'name': name, 'arguments': arguments})


def text_result(rid, text, is_error):
    return {'jsonrpc': '2.0', 'id': rid, 'result': {
        'isError': is_error, 'content': [{'type': 'text', 'text': text}]}}


def rpc_error(rid, code, message):
    return {'jsonrpc': '2.0', 'id': rid,
            'error': {'code': code, 'message': message}}


# Список — только пересечение умений сервера и политики хоста.
assert rpc(1, 'tools/list') == {
    'jsonrpc': '2.0', 'id': 1, 'result': {'tools': ['read_metrics']}}
assert call(2, 'read_metrics', {'service': 'demo'}) == text_result(
    2, 'error_rate=0.15', False)
# Неудача инструмента — результат с isError, а не ошибка протокола.
assert call(3, 'read_metrics', {'service': 'billing'}) == text_result(
    3, 'unknown service', True)
assert calls == ['read_metrics', 'read_metrics']
# Запрещённый хостом инструмент не запускается вовсе.
assert call(4, 'restart_service', {}) == rpc_error(
    4, -32000, 'Tool not allowed')
assert 'restart_service' not in calls
# Разрешён хостом, но сервер его не знает.
assert call(5, 'create_ticket', {}) == rpc_error(5, -32602, 'Unknown tool')
assert rpc(6, 'tools/call', {'name': 'read_metrics'}) == rpc_error(
    6, -32602, 'Invalid params')
assert rpc(7, 'resources/list') == rpc_error(7, -32601, 'Method not found')
assert len(calls) == 2
for bad in ([], {'id': 1, 'method': 'tools/list'},
            {'jsonrpc': '2.0', 'method': 'tools/list'},
            {'jsonrpc': '2.0', 'id': 1, 'method': 'tools/call', 'params': []}):
    expect_value_error(lambda bad=bad: m.handle_jsonrpc(bad, tools, allowed))

# --- agent_tokens и multi_agent_cost: числа из урока ---
assert m.agent_tokens(2000, 500, 1) == 2000
assert m.agent_tokens(2000, 500, 6) == 19500
assert m.agent_tokens(2000, 500, 18) == 112500
assert m.multi_agent_cost(2000, 500, 6, 3, 300) == 63400
assert m.multi_agent_cost(100, 10, 1, 1, 5) == 100 + 100 + 105
expect_value_error(lambda: m.agent_tokens(2000, 500, 0))
expect_value_error(lambda: m.agent_tokens(2000.0, 500, 6))
expect_value_error(lambda: m.multi_agent_cost(2000, 500, 6, True, 300))
expect_value_error(lambda: m.multi_agent_cost(2000, 500, 6, 3, -1))

mode = 'answers' if options.answers else 'student'
print('PASS:', source.parent.parent.name, mode)
