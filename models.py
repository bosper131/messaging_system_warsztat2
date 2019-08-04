from hashings import password_hash
class User(object):
    __id = None
    username = None
    __hashed_password = None
    email = None

    @property
    def id(self):
        return self.__id

    @property
    def hashed_password(self):
        return self.__hashed_password

    def set_password(self, password, salt):
        self.__hashed_password = password_hash(password, salt)

    def save(self, cursor):
        if self.__id is None:
            query = f"""INSERT INTO public."User"(username, hashed_password, email) VALUES ('{self.username}','{self.__hashed_password}','{self.email}') RETURNING id;"""
            cursor.execute(query)
            id = cursor.fetchone()[0]
            self.__id = id
        else:
            query = f"""
            UPDATE public."User"
            SET username='{self.username}', 
                hashed_password='{self.__hashed_password}', 
                email='{self.email}'
            WHERE id={self.__id}
            """
            cursor.execute(query)

    @staticmethod
    def get_item_by_id(id, cursor):
        query = f"""
            SELECT username, hashed_password, email
	        FROM "User" WHERE id = {id};
        """
        cursor.execute(query)
        item = cursor.fetchone()
        u = User()
        u._User__id = id
        u.username = item[0]
        u._User__hashed_password = item[1]
        u.email = item[2]
        return u

    @staticmethod
    def get_item_by_login(username, cursor):
        query = f"""
                SELECT id,username, hashed_password, email
    	        FROM "User" WHERE username = '{username}';
            """
        cursor.execute(query)
        item = cursor.fetchone()
        return item

    @staticmethod
    def get_item_by_email(email, cursor):
        query = f"""
                    SELECT id,username, hashed_password, email
        	        FROM "User" WHERE email = '{email}';
                """
        cursor.execute(query)
        item = cursor.fetchone()
        return item

    @staticmethod
    def get_user_by_password(username, cursor):
        query = f"""
                        SELECT id,hashed_password,email
            	        FROM "User" WHERE username= '{username}';
                    """
        cursor.execute(query)
        item = cursor.fetchone()
        return item

    def delete_user(self, username, cursor):
        query = f"""
                            DELETE FROM "User" WHERE username= '{username}';
                        """
        cursor.execute(query)
        self.__id = None
        return True

    @staticmethod
    def show_users(cursor):
        query = f"""
                            SELECT id,username,email FROM "User" ORDER BY id;
                        """
        cursor.execute(query)
        item = cursor.fetchall()
        return item

    @staticmethod
    def get_create_sql():
        return """
            CREATE TABLE "User" (
            id serial,
            username varchar(200),
            hashed_password varchar(200),
            email varchar(200),
            PRIMARY KEY (id)
        );
        """

    def __str__(self):
        return f"{self.username}, {self.__hashed_password}, {self.email}"


class Message:

    def __init__(self):
        self.id = None
        self.body = None
        self.from_user = None
        self.to_user = None
        self.creation_date = None

    @staticmethod
    def get_create_sql():
        return """
            CREATE TABLE "Message" (
                id serial,
                body varchar(200),
                creation_date TIMESTAMP, 
                from_user integer,
                to_user  integer,
                PRIMARY KEY (id),
                FOREIGN KEY (from_user) references "User"(id),
                FOREIGN KEY (to_user) references "User"(id)
        );
        """

    @staticmethod
    def load_message_by_id(id, cursor):
        query = f"""
                SELECT body, creation_date, from_user, to_user
    	        FROM "Message" WHERE id = {id};
            """
        cursor.execute(query)
        item = cursor.fetchall()
        return item

    @staticmethod
    def load_all_messages_for_user(toUserID, cursor):
        query = f"""
                    SELECT body, creation_date, from_user
        	        FROM "Message" WHERE to_user = {toUserID} ORDER BY creation_date DESC;
                """
        cursor.execute(query)
        item = cursor.fetchall()
        return item

    @staticmethod
    def load_all_messages(cursor):
        query = f"""
                        SELECT body, creation_date, from_user,to_user
            	        FROM "Message" order by id;
                    """
        cursor.execute(query)
        item = cursor.fetchall()
        return item


    def save_message(self, cursor):
        if self.id is None:
            query = f"""INSERT INTO public."Message"(body, creation_date, from_user,to_user) VALUES ('{self.body}','{self.creation_date}','{self.from_user}','{self.to_user}') RETURNING id;"""
            cursor.execute(query)
            id = cursor.fetchone()[0]
            self.id = id
        else:
            query = f"""
               UPDATE public."Message"
               SET body='{self.body}', 
                   creation_date='{self.creation_date}', 
                   from_user='{self.from_user}',
                   to_user = '{self.to_user}'
               WHERE id={self.id}
               """
            cursor.execute(query)

if __name__ == "__main__":
    from connection import get_connection

    c = get_connection()
    cursor = c.cursor()
    # u = Message.save_message(2,c.cursor())
    # u.username = "Attt"
    # u.set_password("olo12","1")
    # u.email = "jan55@op.pl"
    # u.save(c.cursor())
    # print (u)
    u = Message()
    # u.body = 'Natika slodka'
    # u.creation_date = '21/08/2219'
    # u.from_user = "1"
    # u.to_user = "6"
    # u.save_message(cursor)
    #print(u.load_message_by_id(1,cursor))
    print(u.load_all_messages(cursor))
    c.close()