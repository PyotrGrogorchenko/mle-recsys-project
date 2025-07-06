class EventStore:

    def __init__(self, max_events_per_user=10):

        self.events = {}
        self.max_events_per_user = max_events_per_user

    def put(self, user_id, item_id):
        '''
        Сохраняет событие
        '''

        user_events = self.events[user_id] if user_id in self.events.keys() else []
        self.events[user_id] = [item_id] + user_events[: self.max_events_per_user]

        print(self.events)


    def get(self, user_id, k):
        '''
        Возвращает события для пользователя
        '''
        
        user_events = self.events[user_id] if user_id in self.events.keys() else []
        user_events = user_events[: k]

        return user_events