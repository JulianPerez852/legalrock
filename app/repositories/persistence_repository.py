import os
import json


class PersistenceRepository:
    def __init__(self):
        self.path = os.path.join(os.getcwd(), "app", "data", "persistence_data.json")


    def get_conversation(self):
        with open(self.path, "r") as file:
            data = json.load(file)
            return data
        
    def set_conversation(self, data, data_prev):
        max_record = max(data_prev.values(), key=lambda x: int(x['id_conversation']))
        max_record_id = max_record["id_conversation"] + 1
        data["id_conversation"] = max_record_id
        data_record =  {}
        data_record[str(max_record_id)] = data
        data_prev.update(data_record)
        with open(self.path, "w") as file:
            json.dump(data_prev, file, indent=4)

        return max_record_id

    def update_conversation(self, data, data_prev, conversation_id):
        data_record =  {}
        data_record[str(conversation_id)] = data
        data_prev.update(data_record)
        with open(self.path, "w") as file:
            json.dump(data_prev, file, indent=4)