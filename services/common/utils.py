def dedup_ids(ids):
    '''
    Дедублицирует список идентификаторов, оставляя только первое вхождение
    '''
    seen = set()
    ids = [id for id in ids if not (id in seen or seen.add(id))]

    return ids