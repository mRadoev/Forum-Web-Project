from data.models import Category, Topic
from data.database import read_query,insert_query,update_query

def get_all(name):
    sql = '''SELECT id, name, type FROM categories'''

    where_clauses = []
    if name:
        where_clauses.append(f"name like '%{name}%'")

    if where_clauses:
        sql += ' WHERE ' .join(where_clauses)

    return (Category.from_query_result(*row) for row in read_query(sql))


def get_by_id(id: int):
    raw = read_query('SELECT id, name, type FROM categories WHERE id = ?', (id,))

    if not raw:
        return None

    topics_sql = read_query('''Select id, title, description, categories_id 
    FROM topics WHERE categories_id = ? ''', (id, ))

    return Category.from_query_result(*raw[0],[Topic.from_query_result(*row) for row in topics_sql])


def create(category: Category):
    generated_id = insert_query(
        'INSERT INTO categories(name,type) VALUES(?,?)',
        (category.name, 1 if category.type == 'public' else 'private'))

    category.id = generated_id
    return category


def name_exists(name: str):
    data = read_query('SELECT COUNT(*) from categories WHERE name = ?', (name,))
    if data == [(0,)]:
        return False

    return True