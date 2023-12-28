import sqlite3


class DbManager:
    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.c = self.con.cursor()
        sql_create_blog = "CREATE TABLE IF NOT EXISTS blog(id integer not null primary key autoincrement," \
                          "USERNAME text not null, " \
                          "COUNT_TREATED integer default 0 not null, " \
                          "REQUESTED integer default 0 not null);"
        self.c.execute(sql_create_blog)

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

    def close(self):
        self.con.close()


db_manager = DbManager('./test.db')

# db_manager.create_user('Jae')

print(db_manager.get_user('Jae'))
