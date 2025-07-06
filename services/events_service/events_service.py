# uvicorn events_service:app --port 8020 --reload

from fastapi import FastAPI

from EventStore import EventStore

events_store = EventStore()

# создаём приложение FastAPI
app = FastAPI(title='events')

@app.post('/event')
async def post(user_id: int, item_id: int):
    '''
    Сохраняет событие для user_id, item_id
    '''

    events_store.put(user_id, item_id)

    return {'result': 'ok'}

@app.get('/events')
async def get(user_id: int, k: int = 10):
    '''
    Возвращает список последних k событий для пользователя user_id
    '''

    events = events_store.get(user_id, k)

    return {'events': events}