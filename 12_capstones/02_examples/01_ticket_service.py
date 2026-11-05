"""Локальный учебный HTTP-сервис. CPU; без скачивания моделей и сторонних API.
Запуск из корня: uv run python 12_capstones/02_examples/01_ticket_service.py
Это baseline: модель обучается при старте; production-выпуск требует
сохранения артефакта.
"""
from pathlib import Path
import argparse
import json
import socket
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Корень репы: здесь data/ и artifacts/.
ROOT = Path(__file__).resolve().parents[2]
VERSION = 'tfidf-demo-v1'
MAX_BODY_BYTES = 8192
MAX_TEXT_CHARS = 2000


def data(name):
    """Учебный набор из data/<name>.json."""
    return json.loads((ROOT / 'data' / (name + '.json')).read_text())


def make_server(port):
    # Модель обучается один раз при старте и переиспользуется всеми запросами.
    train = [r for r in data('tickets') if r['split'] == 'train']
    model = make_pipeline(TfidfVectorizer(),
                          LogisticRegression(random_state=42))
    model.fit([r['text'] for r in train], [r['label'] for r in train])

    # Не больше двух классификаций одновременно; остальным сразу отвечаем 429.
    slots = threading.BoundedSemaphore(2)

    # Стандартная библиотека Python создаёт объект Handler на каждый запрос и
    # вызывает его метод do_GET или do_POST. Мы описываем только эти методы:
    # «класс» здесь — набор функций, которые сервер вызывает за нас.
    class Handler(BaseHTTPRequestHandler):
        def setup(self):
            super().setup()
            self.connection.settimeout(5)  # медленный клиент получит 408

        def log_message(self, *args):
            pass  # не пишем в лог тела запросов и тексты обращений

        def respond(self, status, obj):
            payload = json.dumps(obj).encode()
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def do_GET(self):
            if self.path == '/health':
                self.respond(200, {'status': 'ok', 'version': VERSION})
            else:
                self.respond(404, {'error': 'not_found'})

        def do_POST(self):
            if self.path != '/classify':
                self.respond(404, {'error': 'not_found'})
                return
            if not slots.acquire(blocking=False):
                self.respond(429, {'error': 'busy'})
                return
            try:
                self.classify()
            except (TimeoutError, socket.timeout):
                self.respond(408, {'error': 'request_timeout'})
            finally:
                slots.release()

        def classify(self):
            # Проверки идут от дешёвых к дорогим: заголовки, размер, JSON, поля.
            if self.headers.get('Transfer-Encoding'):
                self.respond(400, {'error': 'transfer_encoding_not_supported'})
                return
            if self.headers.get_content_type() != 'application/json':
                self.respond(415, {'error': 'application_json_required'})
                return
            try:
                length = int(self.headers.get('Content-Length', '0'))
            except ValueError:
                self.respond(400, {'error': 'invalid_content_length'})
                return
            if not 0 < length <= MAX_BODY_BYTES:
                self.respond(413, {'error': 'body_size_limit'})
                return
            try:
                obj = json.loads(self.rfile.read(length))
            except (ValueError, UnicodeError):
                self.respond(400, {'error': 'invalid_json'})
                return
            # Тело — ровно {"text": "<непустая строка до 2000 символов>"}.
            valid = (
                isinstance(obj, dict)
                and set(obj) == {'text'}
                and isinstance(obj['text'], str)
                and 0 < len(obj['text'].strip()) <= MAX_TEXT_CHARS
            )
            if not valid:
                self.respond(
                    400, {'error': 'expected_nonempty_text_up_to_2000_chars'})
                return
            prediction = str(model.predict([obj['text']])[0])
            self.respond(200, {'label': prediction, 'version': VERSION})

    # 127.0.0.1 — loopback: сервис доступен только с этого компьютера.
    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    server.daemon_threads = True
    return server


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()
    if not 0 <= args.port <= 65535:
        parser.error('port outside 0..65535')

    server = make_server(args.port)
    url = 'http://127.0.0.1:' + str(server.server_port)
    print('Listening on ' + url, flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass  # Ctrl+C — штатная остановка
    finally:
        server.server_close()
