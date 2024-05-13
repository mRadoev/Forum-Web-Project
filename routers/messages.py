from fastapi import APIRouter, HTTPException, status, Header
from services import users_service, conversation_services
from common.auth import get_user_or_raise_401
from data.models import Message, MessagePayload
messages_router = APIRouter(prefix='/msg')


def find_sender_id(x_token: str = Header(...)) -> int:
    data = users_service.decode_token(x_token)
    user_id = data.get('id')
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: User ID not found"
        )
    return user_id


from fastapi import HTTPException


@messages_router.post('/message')
def create_new_conversation(payload: dict, x_token: str = Header(None)):
    if x_token is None:
        return "Log in first!"

    sender_id = find_sender_id(x_token)
    if sender_id is None:
        return "Invalid token or user not found"

    if "recipient_id" not in payload:
        raise HTTPException(status_code=400, detail="Recipient ID is missing in the payload!")

    message_text = payload.get("message_text", "")
    message = Message(sender_id=sender_id, recipient_id=payload["recipient_id"], message_text=message_text)
    return conversation_services.create_message(message)


@messages_router.get('/conversations')
def get_conversations(x_token: str = Header(None)):
    if x_token is None:
        return "You need to log in first!"
    user_id = find_sender_id(x_token)
    if user_id is None:
        return "Invalid token or user not found"
    return conversation_services.all_conversations(user_id)


@messages_router.get('/{id2}')
def get_messages_with_id(id2: int, x_token: str = Header(None)):
    get_user_or_raise_401(x_token)
    if x_token is None:
        return "You need to log in first!"

    data = users_service.decode_token(x_token)
    user_id = data.get("id")
    return conversation_services.conversation_between_users(user_id, id2)


