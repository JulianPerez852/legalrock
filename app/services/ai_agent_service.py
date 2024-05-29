from app.repositories.ai_agent_repository import AIAgentRepository

class AIAgentService:

    def __init__(self):
        self.ai_agent_repository = AIAgentRepository()

    def obtain_message_intention(self, user_text, choises, temperature):
        return self.ai_agent_repository.obtain_message_intention(user_text, choises, temperature)
    
    def answer_other_question(self, user_text, personality, temperature):
        return self.ai_agent_repository.answer_other_question(user_text, personality, temperature)
    
    def obtain_data(self, user_text, choises):
        return self.ai_agent_repository.obtain_data(user_text, choises)
    
    def format_responde(self, system_text, personality, temperature):
        return self.ai_agent_repository.format_response(system_text, personality, temperature)