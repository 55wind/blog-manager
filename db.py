import sqlite3

# UserTable
# id (autogeneration)
# naver_id (str)
# comment_count (int)
# like_count (int)
# neighbor_request_date (date) 일주일동안 안받으면 삭제하는 로직이 필요
# created_date
# updated_date

# UserPostTable
# id (user key)
# post_name (str)
# post_body (str)
# written_comment (str)
# is_liked (boolean)
# created_date
# updated_date

class DbManager:
    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.c = self.con.cursor()
        sql_create_blog = "CREATE TABLE IF NOT EXISTS blog(id integer not null primary key autoincrement," \
                          "USERNAME text not null, " \
                          "COUNT_TREATED integer default 0 not null, " \
                          "REQUESTED integer default 0 not null);"
        self.c.execute(sql_create_blog)

        #UserTable 생성
        sql_user_table = """
                    CREATE TABLE IF NOT EXISTS UserTable (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        naver_id TEXT NOT NULL,
                        comment_count INTEGER DEFAULT 0 NOT NULL,
                        like_count INTEGER DEFAULT 0 NOT NULL,
                        neighbor_request_date DATE,
                        created_date DATE DEFAULT CURRENT_DATE NOT NULL,
                        updated_date DATE DEFAULT CURRENT_DATE NOT NULL
                    );
                """
        self.c.execute(sql_user_table)

        # UserPostTable 생성
        sql_user_post_table = """
                    CREATE TABLE IF NOT EXISTS UserPostTable (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        post_name TEXT NOT NULL,
                        post_body TEXT NOT NULL,
                        written_comment TEXT,
                        is_liked BOOLEAN,
                        created_date DATE DEFAULT CURRENT_DATE NOT NULL,
                        updated_date DATE DEFAULT CURRENT_DATE NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES UserTable(id)
                    );
                """
        self.c.execute(sql_user_post_table)

    def create_user(self, username):
        sql_find_user = f'''SELECT * FROM blog where USERNAME=?'''
        self.c.execute(sql_find_user, (username, ))
        if len(self.c.fetchall()) != 0:
            raise Exception("The user already exists")

        sql_insert = f'''INSERT INTO blog (USERNAME) values (?)'''
        self.c.execute(sql_insert, (username, ))
        self.con.commit()

    def get_user(self, username):
        sql_find_user = f'''SELECT * FROM blog where USERNAME = ?'''
        self.c.execute(sql_find_user, (username, ))
        found_user = self.c.fetchall()
        if len(found_user) == 0:
            raise Exception("The user does not exist")
        if len(found_user) > 1:
            raise Exception("The database scheme has an error. There is more than one user with the same username!")

        return found_user[0]

    def update_user(self, username, ):
        sql_find_user = f'''SELECT * FROM blog where USERNAME = ?'''
        self.c.execute(sql_find_user, (username, ))
        found_user = self.c.fetchall()
        if len(found_user) == 0:
            raise Exception("The user does not exist")
        if len(found_user) > 1:
            raise Exception("The database scheme has an error. There is more than one user with the same username!")

        return found_user[0]

    #테이블 출력 함수
    def list_tables(self):
        sql_list_tables = "SELECT name FROM sqlite_master WHERE type='table';"
        self.c.execute(sql_list_tables)
        tables = self.c.fetchall()

        if not tables:
            print("Table does not exist")
        else:
            print("Table list:")
            for table in tables:
                print(table[0])


    def close(self):
        self.con.close()


db_manager = DbManager('./test.db')

# db_manager.create_user('Jae')

#테이블 리스트 출력
db_manager.list_tables()


print(db_manager.get_user('Jae'))
