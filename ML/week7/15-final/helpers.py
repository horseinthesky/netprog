# coding=utf-8
import os
import pandas


def save_clean_data(cleaner, data_train, target_train, data_test, name='simple'):
    path = './data/clean/' + name
    if not os.path.exists(path):
        os.makedirs(path)

    target_train.to_csv(path + '/target_train.csv')
    cleaner(data_train).to_csv(path + '/data_train.csv')
    cleaner(data_test).to_csv(path + '/data_test.csv')


def get_clean_data(cleaner_name='simple'):
    path = './data/clean/' + cleaner_name
    data_train = pandas.read_csv(path + '/data_train.csv', index_col='match_id')
    target_train = pandas.read_csv(path + '/target_train.csv', index_col='match_id')
    data_test = pandas.read_csv(path + '/data_test.csv', index_col='match_id')
    return data_train, target_train['radiant_win'], data_test


def kaggle_save(name, model, data_test):
    target_test = model.predict_proba(data_test)[:, 1]
    result = pandas.DataFrame({'radiant_win': target_test}, index=data_test.index)
    result.index.name = 'match_id'
    result.to_csv('./data/kaggle/{}.csv'.format(name))
