#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import Ridge
from scipy.sparse import hstack

# 1. Загрузите данные об описаниях вакансий и соответствующих годовых зарплатах из файла salary-train.csv.
train = pd.read_csv('salary-train.csv')


# 2. Проведите предобработку:
def text_transform(text):
    # Приведите тексты к нижнему регистру (text.lower()).
    text = text.map(lambda t: t.lower())

    # Замените все, кроме букв и цифр, на пробелы — это облегчит дальнейшее разделение текста на слова. Для такой
    # замены в строке text подходит следующий вызов: re.sub('[^a-zA-Z0-9]', ' ', text). Также можно воспользоваться
    # методом replace у DataFrame, чтобы сразу преобразовать все тексты:
    text = text.replace('[^a-zA-Z0-9]', ' ', regex=True)
    return text


# Примените TfidfVectorizer для преобразования текстов в векторы признаков. Оставьте только те слова,
# которые встречаются хотя бы в 5 объектах (параметр min_df у TfidfVectorizer).
vec = TfidfVectorizer(min_df=5)
data_train_text = vec.fit_transform(text_transform(train['FullDescription']))

# Замените пропуски в столбцах LocationNormalized и ContractTime на специальную строку 'nan'.
train['LocationNormalized'].fillna('nan', inplace=True)
train['ContractTime'].fillna('nan', inplace=True)

# Примените DictVectorizer для получения one-hot-кодирования признаков LocationNormalized и ContractTime.
enc = DictVectorizer()
data_train_cat = enc.fit_transform(train[['LocationNormalized', 'ContractTime']].to_dict('records'))

# Объедините все полученные признаки в одну матрицу "объекты-признаки". Обратите внимание, что матрицы для текстов и
# категориальных признаков являются разреженными. Для объединения их столбцов нужно воспользоваться функцией
# scipy.sparse.hstack.
data_train = hstack([data_train_text, data_train_cat])

# 3. Обучите гребневую регрессию с параметром alpha=1 и random_state=241.
# Целевая переменная записана в столбце SalaryNormalized.
target_train = train['SalaryNormalized']
model = Ridge(alpha=1, random_state=241)
model.fit(data_train, target_train)

# 4. Постройте прогнозы для двух примеров из файла salary-test-mini.csv. Значения полученных прогнозов являются
# ответом на задание. Укажите их через пробел.
test = pd.read_csv('salary-test-mini.csv')
data_test_text = vec.transform(text_transform(test['FullDescription']))
data_test_cat = enc.transform(test[['LocationNormalized', 'ContractTime']].to_dict('records'))
data_test = hstack([data_test_text, data_test_cat])

target_test = model.predict(data_test)
answer1 = '{:.2f} {:.2f}'.format(target_test[0], target_test[1])
print(answer1)
