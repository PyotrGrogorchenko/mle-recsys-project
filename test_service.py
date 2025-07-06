import requests
import logging
import sys

log_file = logging.FileHandler('test_service.log', mode='w')
log_file.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))

console_out = logging.StreamHandler(sys.stdout)
console_out.setFormatter(logging.Formatter('%(message)s'))

logging.basicConfig(handlers=(log_file, console_out), level=logging.INFO)


# events_service
events_store_url = 'http://127.0.0.1:8020'


def get_events(user_id, k = 100):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    params = {'user_id': user_id, 'k': k}

    url = f'{events_store_url}/events'

    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code == 200:
        result = resp.json()
    else:
        result = None
        logging.info(f'GET {url}. status code: {resp.status_code}')
    
    logging.info(f'GET {url}. response: {result}')


def post_events(user_id, item_ids):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

    url = f'{events_store_url}/event'

    for item_id in item_ids:
        params = {'user_id': user_id, 'item_id': item_id}

        resp = requests.post(url, headers=headers, params=params)
        if resp.status_code == 200:
            result = resp.json()
        else:
            result = None
            logging.info(f'POST {url}. status code: {resp.status_code}')
        
        logging.info(f'POST {url}. response: {result}')

# features_service
features_store_url = 'http://127.0.0.1:8010'


def get_similar_items(item_id, k = 100):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    params = {'item_id': item_id, 'k': k}
    
    url = f'{features_store_url}/similar_items'

    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code == 200:
        result = resp.json()
    else:
        result = None
        logging.info(f'GET {url}. status code: {resp.status_code}')
    
    logging.info(f'GET {url}. response: {result}')


#recs_service
recs_url = 'http://127.0.0.1:8000'


def get_recommendations_online(user_id, k = 100):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    params = {'user_id': user_id, 'k': k}

    url = f'{recs_url}/recommendations_online'

    resp = requests.get(url, headers=headers, params=params)

    if resp.status_code == 200:
        result = resp.json()
    else:
        result = []
        logging.info(f'GET {url}. status code: {resp.status_code}')
        
    logging.info(f'GET {url}. response: {result}')


def get_recommendations_offline(user_id, k = 100):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    params = {'user_id': user_id, 'k': k}

    url = f'{recs_url}/recommendations_offline'

    resp = requests.get(url, headers=headers, params=params)

    if resp.status_code == 200:
        result = resp.json()
    else:
        result = []
        logging.info(f'GET {url}. status code: {resp.status_code}')
        
    logging.info(f'GET {url}. response: {result}')


def get_recommendations(user_id, k = 100):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    params = {'user_id': user_id, 'k': k}

    url = f'{recs_url}/recommendations'

    resp = requests.get(url, headers=headers, params=params)

    if resp.status_code == 200:
        result = resp.json()
    else:
        result = []
        logging.info(f'GET {url}. status code: {resp.status_code}')
        
    logging.info(f'GET {url}. response: {result}')


def get_has_personal(user_id):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    params = {'user_id': user_id}

    url = f'{recs_url}/has_personal'

    resp = requests.get(url, headers=headers, params=params)

    if resp.status_code == 200:
        result = resp.json()
    else:
        result = []
        logging.info(f'GET {url}. status code: {resp.status_code}')
        
    logging.info(f'GET {url}. response: {result}')


user_id = 0
logging.info(f'Пользователь без персональных рекомендаций и онлайн-истории. user_id: {user_id}')
get_has_personal(user_id)
get_events(user_id)
get_recommendations_online(user_id)
get_recommendations_offline(user_id)
get_recommendations(user_id)
logging.info('-' * 100)

user_id = 1
logging.info(f'Пользователь без персональных рекомендаций, но с онлайн-историей. user_id: {user_id}')
get_has_personal(user_id)
get_events(user_id)
post_events(user_id, [66786934, 57123340, 24144596, 46781719, 88159074])
get_events(user_id)
get_recommendations_online(user_id)
get_recommendations_offline(user_id)
get_recommendations(user_id)
logging.info('-' * 100)

user_id = 493820
logging.info(f'Пользователь с персональными рекомендациями, но без онлайн-истории. user_id: {user_id}')
get_has_personal(user_id)
get_events(user_id)
get_recommendations_online(user_id)
get_recommendations_offline(user_id)
get_recommendations(user_id)
logging.info('-' * 100)

user_id = 974780
logging.info(f'Пользователь с персональными рекомендациями и онлайн-историей. user_id: {user_id}')
get_has_personal(user_id)
get_events(user_id)
post_events(user_id, [66786934, 57123340, 24144596, 46781719, 88159074])
get_recommendations_online(user_id)
get_recommendations_offline(user_id)
get_recommendations(user_id)
