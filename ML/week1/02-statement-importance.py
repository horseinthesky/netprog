#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv('titanic.csv', index_col='PassengerId')

data2 = data[['Pclass', 'Sex', 'Age', 'Fare', 'Survived']].dropna()
data2.replace('male', 1, inplace=True)
data2.replace('female', 0, inplace=True)
s = data2[['Survived']]
data2.drop(['Survived'], axis=1, inplace=True)

clf = DecisionTreeClassifier(random_state=241)
clf.fit(data2, s)
importances = clf.feature_importances_
anwer = 'Sex Fare'
