from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage
from langchain.schema import SystemMessage
import os

class AIAgentRepository():
    def __init__(self):
        load_dotenv()

        self.azure_chat_openai = AzureChatOpenAI(
        openai_api_version = os.environ.get("AZURE_OPENAI_API_VERSION"),
        azure_deployment = os.environ.get("AZURE_DEPLOYMENT_CHAT") ,
        )

    def obtain_message_intention(self, user_text, choises, temperature):
        #TODO: add logic using LLM models to work with AI agents
        if user_text == "si" or user_text == "no" or user_text == "verbal" or user_text == "escrita":
            return eval(choises)[user_text]
        
        keys = "\n".join(eval(choises).keys())
        prompt = f"Tienes las siguientes clases para generar una clasificación: \n------\n{keys}\n------\nclasifica el texto entregado por el usuario en alguna de las anteriores."
        self._set_system_message(prompt)

        user_text_prompted = f"Por favor, clasifica el siguiente texto dado por el usuario: \ntexto dado por el usuario: '{user_text}'\nentregalo con respecto a las clases conocidas de la siguiente forma, solamente entrega la lista sin ningún texto adicional: ['clase']"
        intention = self._get_response(user_text_prompted, temperature)
        try:
            return eval(choises)[eval(intention)[0]]
        except:
            return "other"
    
    def answer_other_question(self, user_text, personality, temperature):
        #TODO: Add logic to process random questions usin LLM
        prompt = f"{personality}, responde la siguiente pregunta hecha por el usuario."
        self._set_system_message(prompt)

        return self._get_response(user_text, temperature)
    
    def obtain_data(self, user_text, choises):
        #TODO: Add logic to process data usin LLM and response choises
        if user_text != "otra":
            message_intention = choises["data_obtenida"]
        else:
            message_intention = self.obtain_message_intention(user_text, choises)

        return f"Data obtenida: {user_text}" , message_intention
    

    def _set_system_message(self, system_message:str):
        try:
            self.system_message = SystemMessage(content=system_message.encode('latin1').decode('utf-8'))
        except:
            self.system_message = SystemMessage(content=system_message)
        return self.system_message 
    
    def _get_response(self, user_text, temperature):
        question_message = HumanMessage(content=user_text)
        self.azure_chat_openai.temperature = temperature
        return self.azure_chat_openai([self.system_message, question_message]).content
    
    def format_response(self, system_text, personality, temperature):
        prompt = f"Tu personalidad es: \n{personality}"
        self._set_system_message(prompt)

        system_text_prompted = f"Por favor, reescribe el siguiente texto: \ntexto dado por el usuario: '{system_text}'\nusa tus propias palabras, agrega información si lo consideras necesarios pero no pierdas el sentido del texto."

        return self._get_response(system_text_prompted, temperature)