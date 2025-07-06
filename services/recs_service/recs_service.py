# uvicorn recs_service:app --port 8000 --reload --env-file ../../.env

import os
import sys
import logging
import requests

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager

from Recommendations import Recommendations

sys.path.insert(0, os.path.join(os.getcwd(), '..'))

from common.utils import dedup_ids
from common.S3 import S3

logger = logging.getLogger('uvicorn.error')
rec_store = Recommendations(logger)
s3 = S3('recsys/recommendations', logger)

features_store_url = 'http://127.0.0.1:8010'
events_store_url = 'http://127.0.0.1:8020'
# events_store_url = 'http://events-service:8020'

@asynccontextmanager
async def lifespan(app: FastAPI):
    # код ниже (до yield) выполнится только один раз при запуске сервиса
    logger.info('Starting')
    
    s3.download_file('recommendations.parquet', f'{sys.path[0]}/data/recommendations.parquet')
    s3.download_file('top_popular.parquet', f'{sys.path[0]}/data/top_popular.parquet')
        
    rec_store.load(
        'personal',
        f'{sys.path[0]}/data/recommendations.parquet',
        columns=['user_id', 'item_id', 'rank'],
    )
    
    rec_store.load(
        'default',
        f'{sys.path[0]}/data/top_popular.parquet',
        columns=['item_id', 'rank'],
    )    

    logger.info('Ready!')

    yield
    
    # этот код выполнится только один раз при остановке сервиса
    rec_store.stats()
    logger.info('Stopping')


# создаём приложение FastAPI
app = FastAPI(title='recs', lifespan=lifespan)

# обрабатываем запросы к корню приложения
@app.get('/', response_class=HTMLResponse)
def read_root():
    html = '''
    <html>
        <body>
            <h1>Welcome</h1>
        </body>
    </html>
    '''
    return HTMLResponse(content=html, status_code=200)


# обработка GET-запросов к URL /service-status
@app.get('/service-status')
def health_check():
    return {'status': 'ok'}


@app.get('/recommendations')
async def recommendations(user_id: int, k: int = 100):
    '''
    Возвращает список рекомендаций длиной k для пользователя user_id
    '''

    recs_offline = await recommendations_offline(user_id, k)
    recs_online = await recommendations_online(user_id, k)

    recs_offline = recs_offline['recs']
    recs_online = recs_online['recs']

    recs_blended = []

    min_length = min(len(recs_offline), len(recs_online))
    # чередуем элементы из списков, пока позволяет минимальная длина
    for i in range(min_length):
        recs_blended.append(recs_online[i])
        recs_blended.append(recs_offline[i])

    # добавляем оставшиеся элементы в конец
    recs_blended += recs_offline[min_length:]
    recs_blended += recs_offline[min_length:]

    # удаляем дубликаты
    recs_blended = dedup_ids(recs_blended)
    
    # оставляем только первые k рекомендаций
    recs_blended = recs_blended[:k]

    return {'recs': recs_blended} 


@app.get('/recommendations_offline')
async def recommendations_offline(user_id: int, k: int = 100):
    '''
    Возвращает список рекомендаций длиной k для пользователя user_id
    '''

    recs = rec_store.get(user_id, k)
    return {'recs': recs} 


@app.get('/recommendations_online')
async def recommendations_online(user_id: int, k: int = 100):
    '''
    Возвращает список онлайн-рекомендаций длиной k для пользователя user_id
    '''

    headers = {'ontent-type': 'application/json', 'Accept': 'text/plain'}

    # получаем последнее событие пользователя
    params = {'user_id': user_id, 'k': k}
    resp = requests.get(f'{events_store_url}/events', headers=headers, params=params)
    events = resp.json()
    events = events['events']

    # получаем список айтемов, похожих на последние три, с которыми взаимодействовал пользователь
    items = []
    scores = []
    for item_id in events:
        # для каждого item_id получаем список похожих в item_similar_items
        params = {'item_id': item_id, 'k': k}
        resp = requests.get(f'{features_store_url}/similar_items', headers=headers, params=params)
        item_similar_items = resp.json()
        items += item_similar_items['item_id_2']
        scores += item_similar_items['score']
    # сортируем похожие объекты по scores в убывающем порядке
    # для старта это приемлемый подход
    combined = list(zip(items, scores))
    combined = sorted(combined, key=lambda x: x[1], reverse=True)
    combined = [item for item, _ in combined]

    # удаляем дубликаты, чтобы не выдавать одинаковые рекомендации
    recs = dedup_ids(combined)

    return {'recs': recs} 


@app.get('/has_personal')
async def has_personal(user_id: int, k: int = 100):
    '''
    Возврящает признак наличия персональных рекомендаций для пользователя user_id
    '''

    return rec_store.has_personal(user_id)