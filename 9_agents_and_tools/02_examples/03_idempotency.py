"""Симуляция побочного эффекта и повторного запроса после потери ответа."""


# Sandbox хранит журнал операций и счётчик реальных эффектов вместе.
class Sandbox:
    def __init__(self):
        self.operations = {}  # ID операции -> (сервис, результат)
        self.restarts = 0     # сколько раз эффект реально произошёл

    def restart(self, operation_id, service):
        if not operation_id or service != 'demo':
            raise ValueError('Invalid or unauthorized operation')
        if operation_id in self.operations:
            # Повтор той же операции: эффект не повторяем, отдаём прежний
            # результат.
            old_service, result = self.operations[operation_id]
            if old_service != service:
                raise ValueError('Operation ID reused with different arguments')
            return result
        self.restarts += 1
        result = {'status': 'done', 'number': self.restarts}
        self.operations[operation_id] = (service, result)
        return result


s = Sandbox()
# Представим, что ответ потерялся после успешного выполнения.
s.restart('op1', 'demo')
result = s.restart('op1', 'demo')  # повтор с тем же ID
assert s.restarts == 1 and result['number'] == 1
s.restart('op2', 'demo')  # новый ID — новое действие
assert s.restarts == 2
print('Retries for op1 caused one effect; new op2 caused a second effect.')
print('In production the journal must survive process restart '
      'and handle concurrent calls atomically.')
