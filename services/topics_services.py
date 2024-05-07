from data.models import Topic, Category
from data.database import insert_query, read_query, update_query
from data.models import User

def get_all(title=None):
    sql = '''Select t.id, t.title, t.description, c.name as category_name
     FROM topics t JOIN categories c ON t.categories_id = c.id'''

    where_clauses = []
    if title:
        where_clauses.append(f"title like '%{title}%'")


    if where_clauses:
        sql += ' WHERE '.join(where_clauses)

    return (Topic.from_query_result(*row) for row in read_query(sql))


def get_by_id(id: int):
    data = read_query('''Select t.id, t.title, t.description, c.name as category_name
     FROM topics t JOIN categories c ON t.categories_id = c.id WHERE t.id = ?''', (id,))
    return Topic.from_query_result(*data[0]) if data else None

def get_by_category_id(category_id: int):
    data = read_query('''SELECT t.id, t.title, t.description, c.name as category_name 
    FROM topics t JOIN categories c	ON t.categories_id = c.id WHERE c.id = ?''', (category_id,))


    return Topic.from_query_result(*data[0])

def create(topic: Topic):
    generated_id = insert_query('INSERT INTO topics(title, description, categories_id, users_id) VALUES(?,?,?,1)',
                                (topic.title, topic.description, topic.category_id))

    topic.id = generated_id

    return topic


def assign_to_category(category_id: int, topic_id: int):
    return NotImplementedError()


def title_exists(title: str):
    data = read_query('SELECT COUNT(*) from topics WHERE title = ?', (title,))
    if data == [(0,)]:
        return False

    return True