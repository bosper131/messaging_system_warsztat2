from connection import get_connection
from models import User, Message

def create_table(classes = None):
    if classes is None:
        classes = [Message, User]
    connection = get_connection()
    cursor = connection.cursor()
    for item in classes:
        query = item.get_create_sql()
        cursor.execute(query)


if __name__ == "__main__":
    create_table()