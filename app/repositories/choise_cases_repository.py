from app.schemas.user_conversation_schema import UserConversationSchema
from app.services.ai_agent_service import AIAgentService
import json
class ChoiseCasesRepository():
    def __init__(self):
        self.ai_agent_service = AIAgentService()
        self.switch = {
            'choise': self.choise,
            'finish': self.finish,
            'charge': self.charge,
            'obtain_data': self.obtain_data,
            'obtain_data_entity': self.obtain_data_entity
        }

    def switch_case(self, case, *args):
        return self.switch.get(case)(*args)
    
    def choise(self, data, user_conversation: UserConversationSchema):
        choises = data[user_conversation.conversation_kind]["conversation"][user_conversation.conversation_line]["options"]
        user_intention = self.ai_agent_service.obtain_message_intention(user_conversation.user_text, json.dumps(choises, ensure_ascii=False), user_conversation.temperature)

        if user_intention == "other":
            other_answer = self.ai_agent_service.answer_other_question(user_conversation.user_text, user_conversation.personality, user_conversation.temperature)
            return user_intention, other_answer, None
        
        return user_intention, None, None

    def finish(self, data, user_conversation: UserConversationSchema):
        print("Se escogió el caso de tipo finish")

    def charge(self, data, user_conversation: UserConversationSchema):
        #TODO: add logic to work with charged documents
        choises = data[user_conversation.conversation_kind]["conversation"][user_conversation.conversation_line]["options"]
        user_intention = eval(choises)["data_obtenida"]
        return user_intention, None, "esta es data obtenida de ejemplo"

    def obtain_data(self, data, user_conversation: UserConversationSchema):
        choises = data[user_conversation.conversation_kind]["conversation"][user_conversation.conversation_line]["options"]
        obtained_data, user_intention = self.ai_agent_service.obtain_data(user_conversation.user_text, choises)
        
        if user_intention == "other":
            other_answer = self.ai_agent_service.answer_other_question(user_conversation.user_text)
            return user_intention, other_answer, None
        
        return user_intention, None, obtained_data

    def obtain_data_entity(self, data, user_conversation: UserConversationSchema):
        avaliable_entities = {
            "exito" : "nit: 1212112\nrazon social: exito sa\ntelefono:5154151\nresponsable: pablito\nemail: exito.com",
            "flamingo" : "nit: 7667868\nrazon social: flamingo sa\ntelefono:778989\nresponsable: clavo\nemail: flamingo.com",
            "carulla" : "nit: 88564354\nrazon social: carulla sa\ntelefono:42343521\nresponsable: un\nemail: carulla.com",
            "coraltech" : "nit: 8973728637\nrazon social: coraltech sas\ntelefono:3001456465\nresponsable: Santiago Tirado\nemail: coraltech.com"
        }

        try:
            obtained_data = avaliable_entities[user_conversation.user_text]
        except:
            obtained_data = "no tenemos información de esta entidad"
            return "other", obtained_data, None
        
        return "7" , None, obtained_data  

