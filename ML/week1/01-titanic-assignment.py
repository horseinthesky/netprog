#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import operator

data = pd.read_csv('titanic.csv', index_col='PassengerId')

# Какое количество мужчин и женщин ехало на корабле? В качестве ответа приведите два числа через пробел.
answer1 = '{} {}'.format(data['Sex'].value_counts()['male'], data['Sex'].value_counts()['female'])

# Какой части пассажиров удалось выжить? Посчитайте долю выживших пассажиров.
# Ответ приведите в процентах (число в интервале от 0 до 100, знак процента не нужен), округлив до двух знаков.
answer2 = '{:.2f}'.format(data['Survived'].value_counts(normalize=True)[1] * 100)

# Какую долю пассажиры первого класса составляли среди всех пассажиров?
# Ответ приведите в процентах (число в интервале от 0 до 100, знак процента не нужен), округлив до двух знаков.
answer3 = '{:.2f}'.format(data['Pclass'].value_counts(normalize=True)[1] * 100)

# Какого возраста были пассажиры? Посчитайте среднее и медиану возраста пассажиров.
# В качестве ответа приведите два числа через пробел.
answer4 = '{:.2f} {}'.format(data['Age'].mean(), data['Age'].median())

# Коррелируют ли число братьев/сестер/супругов с числом родителей/детей?
# Посчитайте корреляцию Пирсона между признаками SibSp и Parch.
answer5 = '{:.2f}'.format(data['SibSp'].corr(data['Parch']))

names = {}
for name in data[data.Sex == 'female']['Name']:
    if '(' in name:
        first_name = name.split('(')[-1].split()[0].strip('")')
    else:
        first_name = name.split('. ')[-1].split()[0]

    if first_name not in names:
        names[first_name] = 1
    else:
        names[first_name] += 1

answer6 = max(names.items(), key=operator.itemgetter(1))[0]
print(names)
print(answer6)
