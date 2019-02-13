#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.decomposition import PCA
from numpy import corrcoef

# 1. Загрузите данные close_prices.csv. В этом файле приведены цены акций 30 компаний на закрытии торгов за каждый
# день периода.
df = pd.read_csv('close_prices.csv')
data = df.loc[:, 'AXP':]

# 2. На загруженных данных обучите преобразование PCA с числом компоненты равным 10. Скольких компонент хватит,
# чтобы объяснить 90% дисперсии?
pca = PCA(n_components=10)
pca.fit(data.values)

var = 0
n_var = 0
for v in pca.explained_variance_ratio_:
    n_var += 1
    var += v
    if var >= 0.9:
        break

print(n_var)

# 3. Примените построенное преобразование к исходным данным и возьмите значения первой компоненты.
df_comp = pd.DataFrame(pca.transform(data))
comp0 = df_comp[0]

# 4. Загрузите информацию об индексе Доу-Джонса из файла djia_index.csv. Чему равна корреляция Пирсона между первой
# компонентой и индексом Доу-Джонса?
df2 = pd.read_csv('djia_index.csv')
dji = df2['^DJI']
corr = corrcoef(comp0, dji)
print('{:.2f}'.format(corr[1, 0]))

# 5. Какая компания имеет наибольший вес в первой компоненте? Укажите ее название с большой буквы.
comp0_w = pd.Series(pca.components_[0])
comp0_w_top = comp0_w.sort_values(ascending=False).index[0]
company = data.columns[comp0_w_top]
print(company)
