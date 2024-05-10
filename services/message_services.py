from data.database import insert_query, read_query
from data.models import Message
import mariadb




def send_message(sender_id: int, recipient_id: int, message: str) -> bool:
    try:
        insert_query(
            'INSERT INTO messages(sender_id, recipient_id, message) VALUES (?, ?, ?)',
            (sender_id, recipient_id, message)
        )
        return True
    except mariadb.Error as error:
        print("Error:", error)
        return False

def get_messages(user_id: int) -> list[Message]:
    try:
        data = read_query(
            'SELECT id, sender_id, recipient_id, message, timestamp FROM messages WHERE sender_id = ? OR recipient_id = ? ORDER BY timestamp DESC',
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