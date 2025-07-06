import pandas as pd


class SimilarItems:

    def __init__(self, logger):

        self._similar_items = None
        self._logger = logger
        
    def load(self, type, path, **kwargs):
        '''
        Загружаем данные из файла
        '''

        self._similar_items = pd.read_parquet(path, **kwargs)
        self._logger.info(f'Loaded data, type: {type}')

    def get(self, item_id: int, k: int = 10):
        '''
        Возвращает список похожих объектов
        '''
        try:
            i2i = self._similar_items.query('item_id_1 == @item_id').head(k)
            i2i = i2i[['item_id_2', 'score']].to_dict(orient='list')
        except KeyError:
            self._logger.error('No recommendations found')
            i2i = {'item_id_2': [], 'score': {}}

        return i2i
