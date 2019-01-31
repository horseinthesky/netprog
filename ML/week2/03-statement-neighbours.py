#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.model_selection import KFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import scale

# 1. Загрузите выборку Wine по адресу https://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data
# 2. Извлеките из данных признаки и классы. Класс записан в первом столбце (три варианта), признаки — в столбцах
# со второго по последний. Более подробно о сути признаков можно прочитать по адресу
# https://archive.ics.uci.edu/ml/datasets/Wine
df = pd.read_csv('wine.data', header=None)
classes = df[0]
params = df.loc[:, 1:]

# 3. Оценку качества необходимо провести методом кросс-валидации по 5 блокам (5-fold). Создайте генератор разбиений,
# который перемешивает выборку перед формированием блоков (shuffle=True). Для воспроизводимости результата,
# создавайте генератор KFold с фиксированным параметром random_state=42. В качестве меры качества используйте
# долю верных ответов (accuracy).
kf = KFold(shuffle=True, random_state=42, n_splits=5)

# 4. Найдите точность классификации на кросс-валидации для метода k ближайших соседей
# (sklearn.neighbors.KNeighborsClassifier), при k от 1 до 50. При каком k получилось оптимальное качество?
# Чему оно равно (число в интервале от 0 до 1)? Данные результаты и будут ответами на вопросы 1 и 2.


def test_accuracy(kf, params, classes):
    scores = []
    k_range = range(1, 51)
    for k in k_range:
        model = KNeighborsClassifier(n_neighbors=k)
        scores.append(cross_val_score(model, params, classes, cv=kf, scoring='accuracy'))

    # Mean returns the average of 5 values and sort_values ascending=False places biggest value on 1st position
    return pd.DataFrame(scores, k_range).mean(axis=1).sort_values(ascending=False)


accuracy = test_accuracy(kf, params, classes)
# Best(biggest) value is on 1st position in Series
top_accuracy = accuracy.head(1)

answer1 = top_accuracy.index[0]
answer2 = top_accuracy.values[0]

# 5. Произведите масштабирование признаков с помощью функции sklearn.preprocessing.scale.
# Снова найдите оптимальное k на кросс-валидации.
scaled_params = scale(params)
accuracy = test_accuracy(kf, scaled_params, classes)

# 6. Какое значение k получилось оптимальным после приведения признаков к одному масштабу?
# Приведите ответы на вопросы 3 и 4. Помогло ли масштабирование признаков?
top_accuracy = accuracy.head(1)
answer3 = top_accuracy.index[0]
answer4 = top_accuracy.values[0]


print(answer1, '{:.2f}'.format(answer2), answer3, '{:.2f}'.format(answer4), sep='\n')
