import psycopg2
import config

db = psycopg2.connect(dbname=config.DBNAME, user=config.DBUSR,
                        password=config.DBPSWD, host=config.DBHOST)
sql = db.cursor()

class Database():

    def __init__(self):
        pass

    def Init(self):
        sql.execute("""CREATE TABLE IF NOT EXISTS users (
            id BIGINT,
            notes TEXT,
            input_status TEXT,
            last_input TEXT
        )""")
        db.commit()

    def UserInit(self, user):
        sql.execute(f"SELECT id FROM users WHERE id = {user.id}")

        if sql.fetchone() is None:
            id              = int(user.id)
            users           = [(id, '{}', "{'name_input': False, 'description_input': False}", '')]
            user_records    = ", ".join(["%s"] * len(users))
            insert_query    = (f"INSERT INTO users VALUES {user_records}")

            sql.execute(insert_query, users)
            db.commit()

    def get(self, table, arg, userID):
        if (userID != None):
            sql.execute(f"SELECT {arg} FROM {table} WHERE id = {userID}")
        else:
            sql.execute(f"SELECT {arg} FROM {table}")
        return sql.fetchone()[0]

    def set(self, table, arg, userID, setArg):
        if (userID != None):
            if isinstance(setArg, str):
                sql.execute(f"UPDATE {table} SET {arg} = %s WHERE id = %s", ( setArg, userID))
            else:
                sql.execute(f"UPDATE {table} SET {arg} = {setArg} WHERE id = {userID}")
        else:
            if isinstance(setArg, str):
                sql.execute(f"UPDATE {table} SET {arg} = %s", [setArg])
            else:
                sql.execute(f"UPDATE {table} SET {arg} = {setArg}")
        db.commit()


