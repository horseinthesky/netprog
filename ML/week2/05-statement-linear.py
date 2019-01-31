# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

# 1. Загрузите обучающую и тестовую выборки из файлов perceptron-train.csv и perceptron-test.csv.
# Целевая переменная записана в первом столбце, признаки — во втором и третьем.
df_train = pd.read_csv('perceptron-train.csv', header=None)
target_train = df_train[0]
data_train = df_train.loc[:, 1:]

df_test = pd.read_csv('perceptron-test.csv', header=None)
target_test = df_train[0]
data_test = df_train.loc[:, 1:]

# 2. Обучите персептрон со стандартными параметрами и random_state=241.
model = Perceptron(random_state=241)
model.fit(data_train, target_train)

# 3. Подсчитайте качество (долю правильно классифицированных объектов, accuracy) полученного классификатора
# на тестовой выборке.
acc_before = accuracy_score(target_test, model.predict(data_test))

# 4. Нормализуйте обучающую и тестовую выборку с помощью класса StandardScaler.
scaler = StandardScaler()
data_train_scaled = scaler.fit_transform(data_train)
data_test_scaled = scaler.transform(data_test)

# 5. Обучите персептрон на новых выборках. Найдите долю правильных ответов на тестовой выборке.
model = Perceptron(random_state=241)
model.fit(data_train_scaled, target_train)
acc_after = accuracy_score(target_test, model.predict(data_test_scaled))

# 6. Найдите разность между качеством на тестовой выборке после нормализации и качеством до нее.
# Это число и будет ответом на задание.
answer = acc_after - acc_before
print('{:.3f}'.format(answer))
