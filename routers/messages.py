from fastapi import APIRouter, Depends, HTTPException, Form, status
from data.models import Message
from services.users_service import find_by_id_and_username
from services.message_services import send_message, get_messages

messages_router = APIRouter()


def get_user_id(user_id: int, username: str) -> int:
    # gets the id from the request
    user_exists = find_by_id_and_username(user_id, username)
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user_id


@messages_router.get('/messages', response_model=None)
def get_user_messages(user_id: int = Depends(get_user_id)):
    messages = get_messages(user_id)
    # messages is already a list of Message objects, return it directly
    return messages


@messages_router.post('/send_message', status_code=201)
def send_user_message(recipient_id: int = Form(...), message: str = Form(...), sender_id: int = Depends(get_user_id)):
    send_message(sender_id, recipient_id, message)

