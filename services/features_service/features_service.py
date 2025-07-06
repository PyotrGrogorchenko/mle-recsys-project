# uvicorn features_service:app --port 8010 --reload --env-file ../../.env

import os
import sys
import logging
from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI

from SimilarItems import SimilarItems

sys.path.insert(0, os.path.join(os.getcwd(), '..'))

from common.S3 import S3

logger = logging.getLogger('uvicorn.error')
sim_items_store = SimilarItems(logger)
s3 = S3('recsys/recommendations', logger)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # код ниже (до yield) выполнится только один раз при запуске сервиса
    logger.info('Starting')

    s3.download_file('similar_items.parquet', f'{sys.path[0]}/data/similar_items.parquet')

    sim_items_store.load(
        'similar',
        f'{sys.path[0]}/data/similar_items.parquet',
        columns=['item_id_1', 'item_id_2', 'score'],
    )
    logger.info('Ready!')
    
    yield
    # код ниже выполнится только один раз при остановке сервиса
    logger.info('Stopping')


# создаём приложение FastAPI
app = FastAPI(title='features', lifespan=lifespan)

@app.get('/similar_items')
async def similar_items(item_id: int, k: int = 10):
    '''
    Возвращает список похожих объектов длиной k для item_id
    '''

    i2i = sim_items_store.get(item_id, k)

    return i2i
