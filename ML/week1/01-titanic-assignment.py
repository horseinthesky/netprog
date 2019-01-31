#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import operator

data = pd.read_csv('titanic.csv', index_col='PassengerId')

answer1 = '{} {}'.format(data['Sex'].value_counts()['male'], data['Sex'].value_counts()['female'])
answer2 = '{:.2f}'.format(data['Survived'].value_counts(normalize=True)[1] * 100)
answer3 = '{:.2f}'.format(data['Pclass'].value_counts(normalize=True)[1] * 100)
answer4 = '{:.2f} {}'.format(data['Age'].mean(), data['Age'].median())
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
