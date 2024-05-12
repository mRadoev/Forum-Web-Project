from data.models import Topic, Category
from data.database import insert_query, read_query, update_query
from data.models import User, Reply


def get_all(title=None, search = None, sort_by = None, page=1, size=10):
    sql = '''Select t.id, t.title, t.description, c.name as category_name
     FROM topics t JOIN categories c ON t.categories_id = c.id'''

    where_clauses = []
    if title:
        where_clauses.append(f"t.title like '%{title}%'")

    if search:
        where_clauses.append(f"t.title like '%{search}%' OR t.description like '%{search}%' OR "
                             f"c.name like '%{search}%'")

    if where_clauses:
        sql += ' WHERE ' + ' AND '.join(where_clauses)

    if sort_by:
        valid_sort_fields = ['id', 'title', 'description', 'category_name']
        if sort_by.split(':')[0] in valid_sort_fields:
            sort_field, sort_order = sort_by.split(':')
            if sort_order.upper() == 'DESC':
                sql += f" ORDER BY {sort_field} DESC"
            else:
                sql += f" ORDER BY {sort_field}"
        else:
            raise ValueError("Invalid sort_by parameter")

    offset = (page - 1) * size
    sql += f" LIMIT {size} OFFSET {offset}"

    return (Topic.from_query_result(*row) for row in read_query(sql))


def get_by_id(id: int):
    data = read_query('''Select t.id, t.title, t.description, c.name as category_name
     FROM topics t JOIN categories c ON t.categories_id = c.id  WHERE t.id = ?''', (id,))

    if not data:
        return None

    reply_sql = read_query('''Select id, name, topics_id, description 
    FROM replies WHERE topics_id = ? ''', (id, ))

    best_reply_id_sql = read_query('Select best_reply_id from topics where id = ?',
                                (id, ))
    best_reply_id = best_reply_id_sql[0][0]
    if best_reply_id is None:
        return Topic.from_query_result(*data[0], [Reply.from_query_result(*row) for row in reply_sql])
    else:
        best_reply_sql = read_query('SELECT id, name, topics_id, description FROM replies WHERE id = ? ',
                                (best_reply_id,))
        return Topic.from_query_result(*data[0], [Reply.from_query_result(*row) for row in reply_sql],
                                        [Reply.from_query_result(*best_reply_sql[0])])


def get_by_category_id(category_id: int):
    data = read_query('''SELECT t.id, t.title, t.description, c.name as category_name 
    FROM topics t JOIN categories c	ON t.categories_id = c.id WHERE c.id = ?''', (category_id,))

    return Topic.from_query_result(*data[0])


def create(topic: Topic, id: int):
    generated_id = insert_query('INSERT INTO topics(title, description, categories_id, users_id) VALUES(?,?,?,?)',
                                (topic.title, topic.description, topic.category_id, id))

    topic.id = generated_id

    return topic


def title_exists(title: str):
    data = read_query('SELECT COUNT(*) from topics WHERE title = ?', (title,))
    if data == [(0,)]:
        return False

    return True


def best_reply(topic_id, reply_id, user_id):
    set_best_reply = update_query('UPDATE topics SET best_reply_id = ? WHERE id = ? and users_id = ?',
                             (reply_id, topic_id, user_id))

    if set_best_reply == 1:
        return "You successfully chose the topic's best reply."

def check_topic_creator(topic_id, user_id):
    check_if_topic_creator = read_query('SELECT COUNT(*) from topics WHERE users_id = ? AND id = ?',
                                (user_id, topic_id))

    if check_if_topic_creator == [(0,)]:
        return True

    return False

def check_reply_topic_connection(topic_id, reply_id):
    check_reply_from_topic = read_query('SELECT COUNT(*) from replies WHERE topics_id = ? AND id = ?',
                                        (topic_id, reply_id))

    if check_reply_from_topic == [(0,)]:
        return True

    return False