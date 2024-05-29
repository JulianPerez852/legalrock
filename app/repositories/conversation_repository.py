import os
import json
import random

class ConversationRepository:
    def __init__(self):
        self.path_conversation = os.path.join(os.getcwd(), "app", "data", "persistence_conversation.json")
        self.path_personalities = os.path.join(os.getcwd(), "app", "data", "persistence_personalities.json")

        with open(self.path_conversation, "r") as file:
            self.data = json.load(file)

    def pick_random_personality(self):
        with open(self.path_personalities, "r") as file:
            data = json.load(file)
            personalities = data["personalities"]
            random_personality = random.choice(personalities)
        return random_personality
    
    def pick_random_temperature(self):
        random_temperature = random.uniform(0.3, 0.7)
        return random_temperature
    
    def get_conversation_message(self, conversation_kind, conversation_line):
        message = self.data[conversation_kind]["conversation"][conversation_line]["text"]
        return message
    
    def get_expected_answer(self, conversation_kind, conversation_line):
        expected_answer = self.data[conversation_kind]["conversation"][conversation_line]["expected_answer"]
        return expected_answer
    
    def get_conversation_finish(self, conversation_kind, conversation_line):
        is_finish = self.data[conversation_kind]["conversation"][conversation_line]["is_finish"]
        return is_finish
    
    def get_repeat_option(self, conversation_kind, conversation_line):
        repeat_option = self.data[conversation_kind]["conversation"][conversation_line]["repeat_option"]
        return repeat_option
