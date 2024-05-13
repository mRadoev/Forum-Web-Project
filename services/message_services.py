from data.database import insert_query, read_query
from fastapi import Header, HTTPException, status, Depends
from services import users_service
from data.models import Message
from data import models
import mariadb


def find_sender_id(x_token: str = Header(...)) -> int:
    data = users_service.decode_token(x_token)
    user_id = data.get('id')
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: User ID not found"
        )
    return user_id


def send_message(sender_id: int, conversation_id: int, message_text: str) -> bool:
    try:
        insert_query(
            'INSERT INTO messages(sender_id, conversation_id, message_text) VALUES (?, ?, ?)',
            (sender_id, conversation_id, message_text)
        )
        return True
    except mariadb.Error as error:
        print("Error:", error)
        return False

def create_message(conversation_id: int, message_text: str, sender_id: int = Depends(find_sender_id)) -> models.Message:
    new_message = models.Message(
        conversation_id=conversation_id,
        sender_id=sender_id,
        message_text=message_text
        # timestamp=datetime.utcnow()  # ensure your model supports this
    )
    insert_query("INSERT INTO messages(sender_id, conversation_id, message_text) VALUES (?, ?, ?)", (sender_id, conversation_id, message_text))

    return new_message


def get_messages(user_id: int) -> list[Message]:
    try:
        data = read_query(
            'SELECT id, sender_id, recipient_id, message_text, timestamp FROM messages WHERE sender_id = ? OR recipient_id = ? ORDER BY timestamp DESC',
            (user_id, user_id)
        )
        messages = [Message.from_query_result(*row) for row in data]
        return messages
    except mariadb.Error as error:
        print("Error:", error)
        return []


def get_conversations(user_id: int) -> list[int]:
    try:
        # Retrieve distinct user IDs from messages where the user is either sender or recipient
        data = read_query(
            'SELECT DISTINCT CASE WHEN sender_id = ? THEN recipient_id ELSE sender_id END AS other_user_id FROM messages WHERE sender_id = ? OR recipient_id = ?',
            (user_id, user_id, user_id)
        )
        # Extract the other user IDs from the data
        conversations = [row[0] for row in data]
        return conversations
    except mariadb.Error as error:
        print("Error:", error)
        return []