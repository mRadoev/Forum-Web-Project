from data.models import Topic, Category
from data.database import insert_query, read_query, update_query, query_count


def get_all(title=None):
    sql = '''Select id, title, description FROM topics'''

    where_clauses = []
    if title:
        where_clauses.append(f"title like '%{title}%'")


    if where_clauses:
        sql += ' WHERE '.join(where_clauses)

    return (Topic.from_query_result(*row) for row in read_query(sql))


def get_by_id(id: int):
    data = read_query('Select id, title, description FROM topics WHERE id = ?', (id,))
    return Topic.from_query_result(*data[0]) if data else None


def create(topic: Topic):
    generated_id = insert_query('INSERT INTO topics(title, description) VALUES(?,?)',
                                (topic.title, topic.description))

    topic.id = generated_id

    return topic


def assign_to_category(category_id: int, topic_id: int):
    return NotImplementedError()
    #TODO: create assign to category functionality


def title_exists(title: str):
    return query_count('SELECT COUNT(*) from topics WHERE title = ?', (title,)) > 0