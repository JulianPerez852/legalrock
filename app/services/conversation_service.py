from app.repositories.conversation_repository import ConversationRepository
from app.schemas.user_conversation_schema import UserConversationSchema
from app.repositories.choise_cases_repository import ChoiseCasesRepository
from app.services.ai_agent_service import AIAgentService

class ConversationService:
    def __init__(self, user_conversation: UserConversationSchema):
        self.conversation_repository = ConversationRepository()
        self.user_conversation = user_conversation


    def start_conversation(self):
        random_personality = self.conversation_repository.pick_random_personality()
        random_temperature = self.conversation_repository.pick_random_temperature()

        conversation_message_greeting = self.conversation_repository.get_conversation_message(self.user_conversation.conversation_kind, "0")
        conversation_message_instruction = self.conversation_repository.get_conversation_message(self.user_conversation.conversation_kind, "1")

        ai_agent_service = AIAgentService()

        conversation_message_greeting = ai_agent_service.format_responde(
            conversation_message_greeting, 
            self.user_conversation.personality, 
            self.user_conversation.temperature
            )

        conversation_message_instruction = ai_agent_service.format_responde(
            conversation_message_instruction, 
            self.user_conversation.personality, 
            self.user_conversation.temperature
            )


        self.user_conversation.is_finish = False
        self.user_conversation.conversation_line = "1"
        self.user_conversation.personality = random_personality
        self.user_conversation.temperature = random_temperature

        return conversation_message_greeting.encode("utf-8").decode("latin1"), conversation_message_instruction.encode("utf-8").decode("latin1")
        

    def check_conversation_finish(self):
        is_finish = self.conversation_repository.get_conversation_finish(
            self.user_conversation.conversation_kind, 
            self.user_conversation.conversation_line
        )

        return is_finish

    def update_conversation(self):
        expected_answer = self.conversation_repository.get_expected_answer(
            self.user_conversation.conversation_kind, 
            self.user_conversation.conversation_line
            )
        

        choise_repository = ChoiseCasesRepository()
        user_intention, other_answer, obtained_data = choise_repository.switch_case(
            expected_answer, 
            self.conversation_repository.data, 
            self.user_conversation
            )

        if user_intention == "other":
            repeat_option_message = self.conversation_repository.get_repeat_option(
            self.user_conversation.conversation_kind, 
            self.user_conversation.conversation_line
            )
            
            answer_to_user = f"{other_answer} \n\n\n{repeat_option_message}".encode("utf-8").decode("latin1")

            return answer_to_user, expected_answer
        
        if obtained_data:
            self.user_conversation.obtained_data = f"{self.user_conversation.obtained_data}\n{obtained_data}"
        
        self.user_conversation.conversation_line = user_intention

        conversation_message_instruction = self.conversation_repository.get_conversation_message(self.user_conversation.conversation_kind, user_intention)

        expected_answer = self.conversation_repository.get_expected_answer(
            self.user_conversation.conversation_kind, 
            self.user_conversation.conversation_line
            )

        self.user_conversation.conversation_need = expected_answer

        self.user_conversation.is_finish = self.check_conversation_finish()
        #TODO: obtener la data si así lo requiere (esto puede ser dentro del choise answer)

        if expected_answer == "finish_correctly":
            conversation_message_instruction = conversation_message_instruction.replace("<datos>", self.user_conversation.obtained_data)

        ai_agent_service = AIAgentService()

        conversation_message_instruction = ai_agent_service.format_responde(
            conversation_message_instruction, 
            self.user_conversation.personality, 
            self.user_conversation.temperature
            ).encode("utf-8").decode("latin1")

        return conversation_message_instruction, expected_answer