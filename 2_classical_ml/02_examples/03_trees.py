"""Линейная модель и деревья на синтетической нелинейной задаче.

make_moons рисует на плоскости два переплетённых «полумесяца» точек двух
классов: прямой линией их не разделить, поэтому видно, что умеют деревья.
"""
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import accuracy_score

# Мало точек и заметный шум: глубокому дереву есть что запоминать.
x, y = make_moons(n_samples=300, noise=0.3, random_state=42)
# 30% в validation; stratify=y сохраняет доли классов в обеих частях.
x_train, x_val, y_train, y_val = train_test_split(
    x, y, test_size=0.3, random_state=42, stratify=y)

models = {
    # Прямая граница: сложность ограничена самой формой модели.
    # StandardScaler стандартизует признаки перед L2-штрафом регрессии.
    'linear': make_pipeline(StandardScaler(), LogisticRegression()),
    # Без ограничения глубины: дерево делит, пока не выучит каждую точку.
    'deep_tree': DecisionTreeClassifier(random_state=42),
    # Не больше трёх вопросов подряд.
    'small_tree': DecisionTreeClassifier(max_depth=3, random_state=42),
    # 50 маленьких деревьев, каждое исправляет ошибки предыдущих.
    'boosting': HistGradientBoostingClassifier(
        max_iter=50, max_leaf_nodes=7, random_state=42),
}
for name, model in models.items():
    model.fit(x_train, y_train)
    train_acc = accuracy_score(y_train, model.predict(x_train))
    val_acc = accuracy_score(y_val, model.predict(x_val))
    print(f'{name:11s} train={train_acc:.3f} validation={val_acc:.3f} '
          f'разрыв={train_acc - val_acc:+.3f}')
print('Это validation для сравнения. '
      'Итоговому test нужны независимые новые данные.')
