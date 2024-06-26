from data.models import Topic, Category
from data.database import insert_query, read_query, update_query
from data.models import User, Reply, Vote


def create_reply(reply: Reply, topic_id: int, user_id:int):

    generated_id = insert_query('INSERT INTO replies(name,topics_id, description, users_id) VALUES(?,?,?,?)',
                                (reply.name, topic_id, reply.description, user_id))

    reply.id = generated_id

    return reply


def vote_to_reply(vote: Vote, reply_id: int, user_id: int):

    insert_query('INSERT INTO votes(type, users_id, replies_id) VALUES(?,?,?)',
                         (vote.type, user_id, reply_id))

    return "liked" if vote.type == 1 else "disliked"


def update_vote(vote: Vote, reply_id: int, user_id: int):
    update = update_query('UPDATE votes SET type = ? WHERE users_id = ? and replies_id = ?',
                          (vote.type, user_id, reply_id))

    if not update:
        return None

    return update


def get_reply_info(reply_id:int):
    reply_sql = read_query('''Select id, name, topics_id, description 
        FROM replies WHERE id = ? ''', (reply_id,))

    likes = read_query('SELECT COUNT(*) as likes from votes where type = 1 and replies_id = ?', (reply_id,))
    dislikes = read_query('SELECT COUNT(*) as dislikes from votes where type = 0 and replies_id = ?', (reply_id,))

    return Reply.from_query_result(*reply_sql[0], [{"likes": likes[0], "dislikes": dislikes[0]}])


def check_id_existence(id: int):
    data = read_query('SELECT COUNT(*) from replies WHERE id = ?', (id,))
    if data == [(0,)]:
        return True

    return False


def check_reply_vote_existence(user_id: int, reply_id: int):
    data = read_query('SELECT COUNT(*) from votes WHERE users_id = ? AND replies_id = ?',
                      (user_id, reply_id))

    if data == [(0,)]:
        return False

    return True
