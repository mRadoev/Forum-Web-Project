from data.models import Topic, Category
from data.database import insert_query, read_query, update_query
from data.models import User, Reply


def create_reply(reply: Reply, topic_id: int, user_id:int):

    generated_id = insert_query('INSERT INTO replies(name,topics_id, description, users_id) VALUES(?,?,?,?)',
                                (reply.name, topic_id, reply.description, user_id))

    reply.id = generated_id

    return reply