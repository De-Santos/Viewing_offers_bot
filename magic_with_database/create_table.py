"""HERE YOU CAN MAKE TABLES IN YOU DATA BACE"""
import psycopg2
from psycopg2 import Error
from global_variables import DataBaseSet as DBS


class TableCreator(DBS):
    def __init__(self):
        try:
            self.connection = psycopg2.connect(host=DBS.HOST,
                                               port=DBS.PORT,
                                               database=DBS.DATABASE,
                                               user=DBS.USER,
                                               password=DBS.PASSWORD)
            self.cursor = self.connection.cursor()
        except (Exception, Error) as error:
            raise error

    def create_users_tabel(self):
        try:
            self.cursor.execute(
                f"""
                CREATE TABLE  {DBS.USER_TABLE}(
                {DBS.AUTO_ID_COL} SERIAL PRIMARY KEY,
                {DBS.USER_ID_COL} bigint NOT NULL,
                {DBS.CHANCES_COL} integer NOT NULL,
                {DBS.FIRST_NAME_COL} VARCHAR); 
                """)
            self.connection.commit()
        except (Exception, Error) as error:
            raise error

    def create_messages_table(self):
        try:
            self.cursor.execute(
                f"""
                CREATE TABLE  {DBS.MESSAGE_TABLE}(
                {DBS.MESSAGE_AUTO_ID_COL} SERIAL PRIMARY KEY,
                {DBS.MESSAGE_USER_ID_COL} bigint NOT NULL,
                {DBS.MESSAGE_COL} VARCHAR NOT NULL,
                {DBS.MESSAGE_SEEN_COL} boolean NOT NULL);
                """
            )
            self.connection.commit()
        except (Exception, Error) as error:
            raise error

    def c_close(self):
        if self.connection:
            self.connection.close()
            self.cursor.close()
            return "close connection successfully."
        else:
            return "not a connection."


if __name__ == '__main__':
    db = TableCreator()
    db.create_users_tabel()
    db.create_messages_table()
    db.c_close()
