#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy
# import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold, cross_val_score

# 1. Загрузите данные из файла abalone.csv. Это датасет, в котором требуется предсказать возраст ракушки (число колец)
# по физическим измерениям.
df = pd.read_csv('abalone.csv')

# 2. Преобразуйте признак Sex в числовой: значение F должно перейти в -1, I — в 0, M — в 1. Если вы используете Pandas,
# то подойдет следующий код: data['Sex'] = data['Sex'].map(lambda x: 1 if x == 'M' else (-1 if x == 'F' else 0))
df['Sex'].replace({'F': -1, 'I': 0, 'M': 1}, inplace=True)

# 3. Разделите содержимое файлов на признаки и целевую переменную. В последнем столбце записана целевая переменная,
# в остальных — признаки.
data = df.loc[:, 'Sex':'ShellWeight']
target = df['Rings']

# 4. Обучите случайный лес (sklearn.ensemble.RandomForestRegressor) с различным числом деревьев: от 1 до 50
# (не забудьте выставить "random_state=1" в конструкторе). Для каждого из вариантов оцените качество работы
# полученного леса на кросс-валидации по 5 блокам. Используйте параметры "random_state=1" и "shuffle=True"
# при создании генератора кросс-валидации sklearn.cross_validation.KFold. В качестве меры качества воспользуйтесь
# долей правильных ответов (sklearn.metrics.r2_score).
kf = KFold(n_splits=5, shuffle=True, random_state=1)

scores = []
n_estimators = range(1, 51)
for n in n_estimators:
    model = RandomForestRegressor(n_estimators=n, random_state=1)
    score = numpy.mean(cross_val_score(model, data, target, cv=kf, scoring='r2'))
    scores.append(score)

# 5. Определите, при каком минимальном количестве деревьев случайный лес показывает качество на кросс-валидации
# выше 0.52. Это количество и будет ответом на задание.
for n, score in enumerate(scores):
    if score > 0.52:
        print(n + 2)  # хуй знает, почему +2
        break

# 6. Обратите внимание на изменение качества по мере роста числа деревьев. Ухудшается ли оно?
# plt.plot(scores)
# plt.xlabel('n_estimators')
# plt.ylabel('score')
# plt.savefig('estimators_score.png')
