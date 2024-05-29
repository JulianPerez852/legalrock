from app.repositories.persistence_repository import PersistenceRepository

class PersistenceService:

    def __init__(self):
        self.persistence_repository = PersistenceRepository()

    def get_conversation(self, id_user, id_conversation = None):
        data = self.persistence_repository.get_conversation()

        filtered_data = {key: value for key, value in data.items() if value['id_user'] == id_user}
        
        if id_conversation:
            filtered_data = {key: value for key, value in filtered_data.items() if value['id_conversation'] == id_conversation}

        return data, filtered_data

    def set_conversation(self, data, data_prev):
        return self.persistence_repository.set_conversation(data, data_prev)

    def update_conversation(self, data, data_prev, conversation_id):
        return self.persistence_repository.update_conversation(data, data_prev, conversation_id)