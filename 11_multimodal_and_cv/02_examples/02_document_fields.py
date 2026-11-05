"""Оценка извлечения полей на fixtures. Здесь нет OCR или VLM."""
truth = [
    {'id': 'a', 'date': '2026-01-02', 'amount': '100.00'},
    {'id': 'b', 'date': '2026-02-03', 'amount': '200.00'},
    {'id': 'c', 'date': '2026-03-04', 'amount': '300.00'},
]
pred = [
    # всё верно:
    {'id': 'a', 'date': '2026-01-02', 'amount': '100.00'},
    # перепутаны день и месяц:
    {'id': 'b', 'date': '2026-03-02', 'amount': '200.00'},
    # потерян ноль в сумме:
    {'id': 'c', 'date': '2026-03-04', 'amount': '30.00'},
]
fields = ('date', 'amount')

# Точность полей: доля верных полей среди всех полей всех документов.
correct_fields = 0
for p, t in zip(pred, truth):
    for k in fields:
        if p.get(k) == t[k]:
            correct_fields += 1
field_accuracy = correct_fields / (len(truth) * len(fields))

# Точность документов: документ засчитывается, только если верны ВСЕ его поля.
correct_documents = 0
for p, t in zip(pred, truth):
    if all(p.get(k) == t[k] for k in fields):
        correct_documents += 1
document_accuracy = correct_documents / len(truth)

print('field accuracy:', field_accuracy,
      'fully correct documents:', document_accuracy)
assert document_accuracy < field_accuracy
