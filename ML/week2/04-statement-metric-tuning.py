#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from numpy import linspace
from sklearn.datasets import load_boston
from sklearn.preprocessing import scale
from sklearn.model_selection import KFold, cross_val_score
from sklearn.neighbors import KNeighborsRegressor

# 1. Загрузите выборку Boston с помощью функции sklearn.datasets.load_boston(). Результатом вызова данной функции
# является объект, у которого признаки записаны в поле data, а целевой вектор — в поле target.
dataset = load_boston()
data = dataset.data
target = dataset.target

# 2. Приведите признаки в выборке к одному масштабу при помощи функции sklearn.preprocessing.scale.
data = scale(data)

# 3. Переберите разные варианты параметра метрики p по сетке от 1 до 10 с таким шагом, чтобы всего было протестировано
# 200 вариантов (используйте функцию numpy.linspace). Используйте KNeighborsRegressor с n_neighbors=5 и
# weights='distance' — данный параметр добавляет в алгоритм веса, зависящие от расстояния до ближайших соседей.
# В качестве метрики качества используйте среднеквадратичную ошибку (параметр scoring='mean_squared_error' у
# cross_val_score; при использовании библиотеки scikit-learn версии 0.18.1 и выше необходимо указывать
# scoring='neg_mean_squared_error'). Качество оценивайте, как и в предыдущем задании, с помощью кросс-валидации
# по 5 блокам с random_state = 42, не забудьте включить перемешивание выборки (shuffle=True).


def test_accuracy(kf, data, target):
    scores = []
    p_range = linspace(1, 10, 200)
    for p in p_range:
        model = KNeighborsRegressor(p=p, n_neighbors=5, weights='distance')
        scores.append(cross_val_score(model, data, target, cv=kf, scoring='neg_mean_squared_error'))

    # Mean returns the average of 5 values and sort_values ascending=False places biggest value on 1st position
    return pd.DataFrame(scores, p_range).max(axis=1).sort_values(ascending=False)


kf = KFold(n_splits=5, shuffle=True, random_state=42)
accuracy = test_accuracy(kf, data, target)

# 4. Определите, при каком p качество на кросс-валидации оказалось оптимальным (обратите внимание,
# что показатели качества, которые подсчитывает cross_val_score, необходимо максимизировать).
# Это значение параметра и будет ответом на задачу.
top_accuracy = accuracy.head(1)
answer = top_accuracy.index[0]
print(answer)
