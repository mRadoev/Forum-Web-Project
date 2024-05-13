from data.database import insert_query, read_query
from fastapi import HTTPException, status, Header
from services import users_service
from data.models import Conversation, Message


def find_sender_id(x_token: str = Header(...)) -> int:
    data = users_service.decode_token(x_token)
    user_id = data.get('id')
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: User ID not found"
        )
    return user_id


def all_conversations(id: int):
    user_chats = read_query('''SELECT DISTINCT mu.recipient_id
                                              FROM conversation_participants as mu
                                              JOIN messages as m ON mu.message_id = m.id
                                              WHERE m.sender_id = ?''', (id,))

    conversation_users = [recipient_id for recipient_id, in user_chats]

    if not conversation_users:
        return f"There are no current conversations for user {id}."
    else:
        # Construct the conversation message based on the users involved
        conversation_message = ", ".join([f"User {user_id}" for user_id in conversation_users])
        return f"You have conversations with: {conversation_message}"





def conversation_between_users(user1_id: int, user2_id: int):
    sent_messages: list[Message] = read_query('''SELECT m.id, m.sender_id, mu.recipient_id, m.message_text
                                                FROM conversation_participants mu
                                                JOIN messages m
                                                ON mu.message_id = m.id
                                                WHERE (m.sender_id = ? AND mu.recipient_id = ?)
                                                   OR (m.sender_id = ? AND mu.recipient_id = ?)
                                                   OR (m.sender_id = ? AND mu.recipient_id = ?)
                                                   OR (m.sender_id = ? AND mu.recipient_id = ?)''',
                                                (user1_id, user2_id, user2_id, user1_id, user1_id, user1_id, user2_id, user2_id))

    if not sent_messages:
        return "No messages have been sent"
    return [Message.from_query_result(*row) for row in sent_messages]





def create_message(message: Message):
        generated_id = insert_query('INSERT INTO messages (sender_id, message_text) VALUES (?, ?)', (message.sender_id, message.message_text))
        message.message_id = generated_id
        insert_query('INSERT INTO conversation_participants (message_id, recipient_id) VALUES (?, ?)',(message.message_id, message.recipient_id),)
        return (f"Message is sent!")

