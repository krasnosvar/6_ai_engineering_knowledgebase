"""Учебная имитация обмена в стиле MCP: JSON-RPC по stdio, без SDK и сети.

Это не реализация протокола MCP, а игрушка, повторяющая форму сообщений:
initialize, tools/list и tools/call. Клиент запускает сервер дочерним
процессом этого же файла и общается с ним строками JSON через stdin/stdout.
"""
import json
import subprocess
import sys

# --- Сервер: знает свои инструменты, но не знает политику хоста ---

TOOLS = [
    {'name': 'read_metrics',
     'description': 'Прочитать метрики сервиса',
     'inputSchema': {'type': 'object',
                     'properties': {'service': {'type': 'string'}},
                     'required': ['service']}},
    {'name': 'restart_service',
     'description': 'Перезапустить сервис',
     'inputSchema': {'type': 'object',
                     'properties': {'service': {'type': 'string'}},
                     'required': ['service']}},
]


def handle(request):
    """Возвращает JSON-RPC ответ на один запрос."""
    rid, method = request['id'], request['method']
    params = request.get('params', {})
    if method == 'initialize':
        result = {'serverInfo': {'name': 'toy-metrics'},
                  'capabilities': {'tools': {}}}
    elif method == 'tools/list':
        result = {'tools': TOOLS}
    elif method == 'tools/call' and params.get('name') == 'read_metrics':
        service = params.get('arguments', {}).get('service')
        if service != 'demo':
            # Ошибка исполнения инструмента — это результат с isError,
            # а не ошибка протокола: модель может её прочитать.
            result = {'isError': True, 'content': [
                {'type': 'text', 'text': f'unknown service: {service}'}]}
        else:
            text = json.dumps({'service': 'demo', 'error_rate': 0.15})
            result = {'isError': False,
                      'content': [{'type': 'text', 'text': text}]}
    elif method == 'tools/call':
        return {'jsonrpc': '2.0', 'id': rid,
                'error': {'code': -32602, 'message': 'Unknown tool'}}
    else:
        return {'jsonrpc': '2.0', 'id': rid,
                'error': {'code': -32601, 'message': 'Method not found'}}
    return {'jsonrpc': '2.0', 'id': rid, 'result': result}


def serve():
    """Цикл сервера: одна строка stdin — один запрос, одна строка stdout."""
    for line in sys.stdin:
        print(json.dumps(handle(json.loads(line))), flush=True)


# --- Клиент внутри хоста: решает, что показать модели и что выполнить ---

ALLOWED_TOOLS = {'read_metrics'}   # политика хоста, а не сервера


def main():
    server = subprocess.Popen([sys.executable, __file__, '--server'],
                              stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              text=True)
    next_id = 0

    def call(method, params=None):
        nonlocal next_id
        next_id += 1
        request = {'jsonrpc': '2.0', 'id': next_id, 'method': method}
        if params is not None:
            request['params'] = params
        line = json.dumps(request, ensure_ascii=False, separators=(',', ':'))
        print('->', line)
        server.stdin.write(line + '\n')
        server.stdin.flush()
        response = json.loads(server.stdout.readline())
        print('<-', json.dumps(response, ensure_ascii=False,
                               separators=(',', ':')))
        return response

    call('initialize', {'clientInfo': {'name': 'toy-host'}})
    offered = [t['name'] for t in call('tools/list')['result']['tools']]
    shown = [name for name in offered if name in ALLOWED_TOOLS]
    print('сервер предлагает:', offered, '| модели показываем:', shown)

    # Предложения «модели» заданы заранее: этот пример проверяет обмен,
    # а не выбор инструмента.
    proposals = [('read_metrics', {'service': 'demo'}),
                 ('read_metrics', {'service': 'billing'}),
                 ('restart_service', {'service': 'demo'})]
    for name, arguments in proposals:
        if name not in ALLOWED_TOOLS:
            print('хост отклонил без вызова сервера:', name)
            continue
        call('tools/call', {'name': name, 'arguments': arguments})

    server.stdin.close()
    server.wait()


if __name__ == '__main__':
    if '--server' in sys.argv:
        serve()
    else:
        main()
