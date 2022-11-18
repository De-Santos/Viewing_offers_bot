import psycopg2
from psycopg2 import Error
from global_variables import DataBaseSet as DBS, BotSet as BUS


class DataBaseInterface(DBS, BUS):
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

    def add_message_row(self, user_id, message):
        try:
            new_row = \
                f"""INSERT INTO {DBS.MESSAGE_TABLE} ({DBS.MESSAGE_USER_ID_COL}, 
                {DBS.MESSAGE_COL}, 
                {DBS.MESSAGE_SEEN_COL}) 
            VALUES (%s, %s, %s)"""
            new_row_val = (user_id, message, False)
            self.cursor.execute(new_row, new_row_val)
            self.connection.commit()
            return "row add successfully."
        except(Exception, Error) as error:
            self.c_close()
            raise error

    def add_user(self, user_id: int, first_name: [str, None]):
        try:
            new_row = f"""INSERT INTO {DBS.USER_TABLE} ({DBS.USER_ID_COL}, {DBS.CHANCES_COL}, {DBS.FIRST_NAME_COL}) 
            VALUES (%s, %s, %s)"""
            new_row_val = (user_id, 0, first_name)
            self.cursor.execute(new_row, new_row_val)
            self.connection.commit()
        except(Exception, Error) as error:
            self.c_close()
            raise error

    def clean_db(self):
        try:
            self.cursor.execute(
                f"""
                DELETE
                FROM {DBS.MESSAGE_TABLE}
                WHERE {DBS.MESSAGE_SEEN_COL} = true;
                """
            )
            self.connection.commit()
            return True
        except(Exception, Error) as error:
            self.c_close()
            raise error

    def del_all_seen_messages(self, user_id: int):
        try:
            self.cursor.execute(
                f"""
                DELETE
                FROM {DBS.MESSAGE_TABLE}
                WHERE {DBS.MESSAGE_USER_ID_COL} = {user_id} and {DBS.MESSAGE_SEEN_COL} = true;
                """
            )
            self.connection.commit()
            return True
        except(Exception, Error) as error:
            self.c_close()
            raise error

    def user_in_table(self, user_id: int):
        try:
            self.cursor.execute(
                f"""
                SELECT EXISTS (
                SELECT FROM
                    {DBS.USER_TABLE}
                WHERE
                    {DBS.USER_ID_COL} ='{user_id}');
                """
            )
            return any(list(map(lambda x: True in x, self.cursor.fetchall())))  # Power by Sergey Fomichev
        except(Exception, Error) as error:
            self.c_close()
            raise error

    def user_have_three_chance(self, user_id: int):
        try:
            self.cursor.execute(
                f"""
                SELECT EXISTS(
                SELECT FROM {DBS.USER_TABLE}
                WHERE
                    {DBS.USER_ID_COL} = {int(user_id)} and
                    {DBS.CHANCES_COL} >= {BUS.USER_CHANCES}
                    );
                """
            )
            return self.cursor.fetchall()[0][0]
        except(Exception, Error) as error:
            self.c_close()
            raise error

    def get_first_name(self, user_id: int):
        try:
            self.cursor.execute(
                f"""
                SELECT {DBS.FIRST_NAME_COL} FROM {DBS.USER_TABLE}
                WHERE {DBS.USER_ID_COL} = {int(user_id)};
                """
            )
            return self.cursor.fetchall()[0][0]
        except(Exception, Error) as error:
            self.c_close()
            raise error

    def get_user_chance(self, user_id: int):
        try:
            self.cursor.execute(
                f"""
                SELECT {DBS.CHANCES_COL} FROM {DBS.USER_TABLE} 
                WHERE {DBS.USER_ID_COL} = {int(user_id)};
                """
            )
            return self.cursor.fetchall()[0][0]
        except(Exception, Error) as error:
            self.c_close()
            raise error

    def get_user_offers(self, user_id: int):
        try:
            if self.user_in_table(user_id) is True:
                self.cursor.execute(
                    f"""
                    SELECT {DBS.MESSAGE_COL}, {DBS.MESSAGE_AUTO_ID_COL} FROM {DBS.MESSAGE_TABLE}
                    WHERE {DBS.MESSAGE_USER_ID_COL} = {user_id}
                    """
                )
                # in old version
                # result = []
                # for obj in self.cursor.fetchall():
                #     result.append(obj[0])
                # return result
                return self.cursor.fetchall()
            else:
                return None
        except(Exception, Error) as error:
            self.c_close()
            raise error

    def get_message_info(self, message_id: int):
        try:
            self.cursor.execute(
                f"""
                SELECT {DBS.MESSAGE_SEEN_COL} FROM {DBS.MESSAGE_TABLE}
                WHERE {DBS.MESSAGE_AUTO_ID_COL} = {message_id}
                """
            )
            if self.cursor.fetchall()[0][0] is True:
                return "yes"
            else:
                return "no"
        except(Exception, Error) as error:
            self.c_close()
            raise error

    def get_seen_offer(self):
        try:
            self.cursor.execute(
                f"""
                SELECT {DBS.MESSAGE_COL}, {DBS.MESSAGE_USER_ID_COL}, {DBS.MESSAGE_AUTO_ID_COL} FROM {DBS.MESSAGE_TABLE}
                WHERE {DBS.MESSAGE_SEEN_COL} = TRUE
                ORDER BY {DBS.MESSAGE_AUTO_ID_COL} 
                LIMIT 100
                """
            )
            return self.cursor.fetchall()
        except(Exception, Error) as error:
            self.c_close()
            raise error

    def get_one_no_seen_offers(self):
        try:
            self.cursor.execute(
                f"""
                SELECT {DBS.MESSAGE_COL}, {DBS.MESSAGE_USER_ID_COL}, {DBS.MESSAGE_AUTO_ID_COL} FROM {DBS.MESSAGE_TABLE}
                WHERE {DBS.MESSAGE_SEEN_COL} = FALSE
                ORDER BY {DBS.MESSAGE_AUTO_ID_COL} 
                LIMIT 1
                """
            )
            result = self.cursor.fetchall()
            if result != []:
                result = result[0]
                self.cursor.execute(
                    f"""
                    UPDATE {DBS.MESSAGE_TABLE}
                    SET {DBS.MESSAGE_SEEN_COL} = TRUE
                    WHERE {DBS.MESSAGE_AUTO_ID_COL} = {result[2]} 
                    """
                )
                self.connection.commit()
                return result
            else:
                return None
        except(Exception, Error) as error:
            self.c_close()
            raise error

    def plus_chance(self, user_id: int):
        try:
            if self.get_user_chance(user_id=user_id) < BUS.USER_CHANCES:
                self.cursor.execute(
                    f"""
                    UPDATE {DBS.USER_TABLE}
                    SET {DBS.CHANCES_COL} = {DBS.CHANCES_COL} + 1
                    WHERE {DBS.USER_ID_COL} = {int(user_id)};
                    """
                )
                self.connection.commit()
                self.cursor.execute(
                    f"""
                    SELECT {DBS.CHANCES_COL} FROM {DBS.USER_TABLE}
                    WHERE {DBS.USER_ID_COL} = {user_id}
                    """
                )
                return self.cursor.fetchall()[0][0]
            else:
                return False
        except(Exception, Error) as error:
            self.c_close()
            raise error

    def change_message_new_offer(self, user_id: int, new_message: str):
        try:
            self.cursor.execute(
                f"""
                UPDATE {DBS.MESSAGE_TABLE}
                SET {DBS.MESSAGE_COL} = {new_message}
                WHERE {DBS.MESSAGE_USER_ID_COL} = {int(user_id)};
                """
            )
            self.connection.commit()
        except(Exception, Error) as error:
            self.c_close()
            raise error

    def user_del_one_chance(self, user_id: int):
        try:
            if self.get_user_chance(user_id=user_id) > 0:
                self.cursor.execute(
                    f"""
                    UPDATE {DBS.USER_TABLE} 
                    SET {DBS.CHANCES_COL} = {DBS.CHANCES_COL} - 1
                    WHERE {DBS.USER_ID_COL} = {int(user_id)};
                    """
                )
                self.connection.commit()
                return True
            else:
                return False
        except(Exception, Error) as error:
            self.c_close()
            raise error

    def c_close(self):
        if self.connection:
            self.connection.close()
            self.cursor.close()
            return "close connection successfully."
        else:
            return "not a connection."
