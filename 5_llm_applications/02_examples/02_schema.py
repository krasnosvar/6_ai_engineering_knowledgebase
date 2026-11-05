"""Валидатор контракта, без вызова LLM."""
import json


def validate(raw):
    # Не JSON -> json.JSONDecodeError (подкласс ValueError).
    obj = json.loads(raw)
    if not isinstance(obj, dict) or set(obj) != {'ticket_id', 'label'}:
        raise ValueError('Expected exactly ticket_id and label')
    if not isinstance(obj['ticket_id'], str) or not obj['ticket_id']:
        raise ValueError('ticket_id must be a non-empty string')
    if obj['label'] not in ('database', 'network', 'access', 'unknown'):
        raise ValueError('Unknown label')
    return obj


if __name__ == '__main__':
    cases = [
        '{"ticket_id":"t1","label":"network"}',  # корректный
        '{"label":"network"}',                   # нет ticket_id
        '{"ticket_id":"t2","label":"invented"}',  # недопустимая категория
        'not json',                              # вообще не JSON
    ]
    for raw in cases:
        # try/except: пробуем проверить, а при ошибке печатаем её текст
        # вместо падения всей программы.
        try:
            print('VALID', validate(raw))
        except (ValueError, TypeError) as e:
            print('INVALID', str(e))
    print('VALID does not mean semantically correct: '
          'compare with ground truth.')
