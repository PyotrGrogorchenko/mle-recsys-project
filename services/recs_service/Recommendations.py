import os
import logging
import pandas as pd

class Recommendations:

    def __init__(self, logger = logging.getLogger()):

        self._logger = logger
        self._recs = {'personal': None, 'default': None}
        self._stats = {
            'request_personal_count': 0,
            'request_default_count': 0,
        }


    def load(self, type, path, **kwargs):
        '''
        Загружает рекомендации из файла
        '''

        self._recs[type] = pd.read_parquet(path, **kwargs)
        if type == 'personal':
            self._recs[type] = self._recs[type].set_index('user_id')
        self._logger.info(f'Loaded recommendations, type: {type}')


    def get(self, user_id: int, k: int=100):
        '''
        Возвращает список рекомендаций для пользователя
        '''
        try:
            recs = self._recs['personal'].loc[user_id]
            recs = recs['item_id'].to_list()[:k]
            self._stats['request_personal_count'] += 1
        except KeyError:
            recs = self._recs['default']
            recs = recs['item_id'].to_list()[:k]
            self._stats['request_default_count'] += 1
        except:
            self._logger.error('No recommendations found')
            recs = []

        return recs


    def has_personal(self, user_id: int):
        '''
        Возврящает признак наличия персональных рекомендаций для пользователя user_id
        '''
        
        try:
            is_has = user_id in self._recs['personal'].index.unique()
        except:
            is_has = False
            self._logger.error('Personal recommendations undefined')
        
        return is_has


    def stats(self):

        self._logger.info('Stats for recommendations')
        for name, value in self._stats.items():
            self._logger.info(f'{name:<30} {value}')