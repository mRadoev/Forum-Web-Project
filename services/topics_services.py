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

    return Topic.from_query_result(*data[0],[Reply.from_query_result(*row) for row in reply_sql])


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
