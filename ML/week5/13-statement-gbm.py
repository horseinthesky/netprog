#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import math
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import log_loss
# import matplotlib.pyplot as plt

# 1. Загрузите выборку из файла gbm-data.csv с помощью pandas и преобразуйте ее в массив numpy (параметр values у
# датафрейма). В первой колонке файла с данными записано, была или нет реакция. Все остальные колонки (d1 - d1776)
# содержат различные характеристики молекулы, такие как размер, форма и т.д. Разбейте выборку на обучающую и тестовую,
# используя функцию train_test_split с параметрами test_size = 0.8 и random_state = 241.
df = pd.read_csv('gbm-data.csv')
target = df['Activity'].values
data = df.loc[:, 'D1':'D1776'].values

data_train, data_test, target_train, target_test = train_test_split(data, target, test_size=0.8, random_state=241)


# 2. Обучите GradientBoostingClassifier с параметрами n_estimators=250, verbose=True, random_state=241 и для каждого
# значения learning_rate из списка [1, 0.5, 0.3, 0.2, 0.1] проделайте следующее:

def sigmoid(y_pred):
    # Преобразуйте полученное предсказание с помощью сигмоидной функции по формуле 1 / (1 + e^{−y_pred}),
    # где y_pred — предсказаное значение.
    return 1.0 / (1.0 + math.exp(-y_pred))


def log_loss_results(model, data, target):
    # Используйте метод staged_decision_function для предсказания качества на обучающей и тестовой выборке
    # на каждой итерации.
    results = []
    for pred in model.staged_decision_function(data):
        results.append(log_loss(target, [sigmoid(y_pred) for y_pred in pred]))

    return results


def plot_loss(learning_rate, test_loss, train_loss):
    # Вычислите и постройте график значений log-loss (которую можно посчитать с помощью функции
    # sklearn.metrics.log_loss) на обучающей и тестовой выборках, а также найдите минимальное значение метрики и
    # номер итерации, на которой оно достигается.
    # plt.figure()
    # plt.plot(test_loss, 'r', linewidth=2)
    # plt.plot(train_loss, 'g', linewidth=2)
    # plt.legend(['test', 'train'])
    # plt.savefig('plots/rate_' + str(learning_rate) + '.png')

    min_loss_value = min(test_loss)
    min_loss_index = test_loss.index(min_loss_value)
    return min_loss_value, min_loss_index


def model_test(learning_rate):
    model = GradientBoostingClassifier(learning_rate=learning_rate, n_estimators=250, verbose=True, random_state=241)
    model.fit(data_train, target_train)

    train_loss = log_loss_results(model, data_train, target_train)
    test_loss = log_loss_results(model, data_test, target_test)
    return plot_loss(learning_rate, test_loss, train_loss)


min_loss_results = {}
for learning_rate in [1, 0.5, 0.3, 0.2, 0.1]:
    min_loss_results[learning_rate] = model_test(learning_rate)

# 3. Как можно охарактеризовать график качества на тестовой выборке, начиная с некоторой итерации:переобучение
# (overfitting) или недообучение (underfitting)? В ответе укажите одно из слов overfitting либо underfitting.

print('answer1 is:\n{}\n'.format('overfitting'))

# 4. Приведите минимальное значение log-loss и номер итерации, на котором оно достигается, при learning_rate = 0.2.
min_loss_value, min_loss_index = min_loss_results[0.2]
print('answer2 is:\n{:.2f} {}\n'.format(min_loss_value, min_loss_index))

# 5. На этих же данных обучите RandomForestClassifier с количеством деревьев, равным количеству итераций, на котором
# достигается наилучшее качество у градиентного бустинга из предыдущего пункта, c random_state=241 и остальными
# параметрами по умолчанию. Какое значение log-loss на тесте получается у этого случайного леса? (Не забывайте, что
# предсказания нужно получать с помощью функции predict_proba)
model = RandomForestClassifier(n_estimators=min_loss_index, random_state=241)
model.fit(data_train, target_train)
y_pred = model.predict_proba(data_test)[:, 1]
test_loss = log_loss(target_test, y_pred)
print('answer3 is:\n{:.2f}'.format(test_loss))
