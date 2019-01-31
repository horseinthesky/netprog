#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from pandas import DataFrame
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import KFold, GridSearchCV

from sklearn import datasets

# 1. Загрузите объекты из новостного датасета 20 newsgroups, относящиеся к категориям "космос" и
# "атеизм" (инструкция приведена выше). Обратите внимание, что загрузка данных может занять несколько минут
newsgroups = datasets.fetch_20newsgroups(
    subset='all',
    categories=['alt.atheism', 'sci.space']
)

target = newsgroups.target
data = newsgroups.data

# 2. Вычислите TF-IDF-признаки для всех текстов. Обратите внимание, что в этом задании мы предлагаем вам
# вычислить TF-IDF по всем данным. При таком подходе получается, что признаки на обучающем множестве используют
# информацию из тестовой выборки — но такая ситуация вполне законна, поскольку мы не используем значения целевой
# переменной из теста. На практике нередко встречаются ситуации, когда признаки объектов тестовой выборки известны на
# момент обучения, и поэтому можно ими пользоваться при обучении алгоритма.
vectorizer = TfidfVectorizer()
vectorizer.fit_transform(data)

# 3. Подберите минимальный лучший параметр C из множества [10^-5, 10^-4, ... 10^4, 10^5] для SVM с
# линейным ядром (kernel='linear') при помощи кросс-валидации по 5 блокам. Укажите параметр random_state=241 и для SVM,
# и для KFold. В качестве меры качества используйте долю верных ответов (accuracy).
grid = {'C': np.power(10.0, np.arange(-5, 6))}
cv = KFold(n_splits=5, shuffle=True, random_state=241)
model = SVC(kernel='linear', random_state=241)
gs = GridSearchCV(model, grid, scoring='accuracy', cv=cv)
gs.fit(vectorizer.transform(data), target)

C = gs.best_params_.get('C')

# 4. Обучите SVM по всей выборке с оптимальным параметром C, найденным на предыдущем шаге.
model = SVC(kernel='linear', random_state=241, C=C)
model.fit(vectorizer.transform(data), target)

# 5. Найдите 10 слов с наибольшим по модулю весом. Они являются ответом на это задание. Укажите их через запятую или
# пробел, в нижнем регистре, в лексикографическом порядке.
words = vectorizer.get_feature_names()
coef = DataFrame(model.coef_.data, model.coef_.indices)
# Тут берётся Series coef[0] из DataFrame coef, все его значения заменяются абсолютными (т.е. модуль)
# Далее отключается сортировка по возрастанию, чтобы наибольшие значение были вначале
# Берутся первые 10 значений индексов, как того требует задание, и по этому индексу находится слово из words
# map возвращает итератор этих слов
top_words = coef[0].map(lambda w: abs(w)).sort_values(ascending=False).head(10).index.map(lambda i: words[i])
# Тут слова сортируются и выводятся
print(' '.join(top_words.sort_values()))
