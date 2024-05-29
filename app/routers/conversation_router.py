from fastapi import APIRouter
from app.schemas.user_conversation_schema import UserConversationSchema
from app.services.persistence_service import PersistenceService
from app.services.conversation_service import ConversationService

conversation_router = APIRouter()

@conversation_router.post(
        path = "/start_conversation/",
        tags = ["conversation"],
        summary = "Crear una nueva conversación.",
        description="Crea una nueva conversación y un registro en la base de datos de persistencia."
        )
async def start_conversation(user_conversation: UserConversationSchema):
        print("empieza")
        persistence_service = PersistenceService()
        data, filtered_data = persistence_service.get_conversation(user_conversation.id_user)

        conversation_service = ConversationService(user_conversation)
        conversation_message_greeting, conversation_message_instruction = conversation_service.start_conversation()

        data_json = conversation_service.user_conversation.model_dump()

        max_record_id = persistence_service.set_conversation(data_json, data)

        return {"message_greeting": conversation_message_greeting.encode('latin1').decode('utf-8'),
                "message_instruction": conversation_message_instruction.encode('latin1').decode('utf-8'),
                "id_conversation": max_record_id}

@conversation_router.post(
        path = "/update_conversation/",
        tags = ["conversation"],
        summary = "Actualizar una conversación.",
        description="Actualiza una conversación y un registro en la base de datos de persistencia."
)
async def update_conversation(user_conversation: UserConversationSchema):
        persistence_service = PersistenceService()
        data, filtered_data = persistence_service.get_conversation(user_conversation.id_user, user_conversation.id_conversation)

        conversation_id = str(user_conversation.id_conversation)

        filtered_data = filtered_data[str(user_conversation.id_conversation)]

        filtered_data["user_text"] = user_conversation.user_text

        user_conversation = UserConversationSchema.model_validate(filtered_data)

        conversation_service = ConversationService(user_conversation)

        conversation_message_instruction, system_instruction = conversation_service.update_conversation()
        
        data_json = conversation_service.user_conversation.model_dump()

        persistence_service.update_conversation(data_json, data, conversation_id)

        return {"message_instruction": conversation_message_instruction.encode('latin1').decode('utf-8'),
                "system_instruction": system_instruction}