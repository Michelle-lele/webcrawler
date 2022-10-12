import datetime

from nauka.read_config import read_db_config
import mysql.connector


class DB:
    def __init__(self):
        config = read_db_config('config.ini', 'mysql')
        print(config)
        try:
            self.conn = mysql.connector.connect(**config)
        except mysql.connector.Error as e:
            print(e)

    def create_publications_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS publications(
            id 	INT AUTO_INCREMENT PRIMARY KEY,
            category VARCHAR(45),
            URL VARCHAR(400),
            title VARCHAR(120), 
            date DATETIME,
            content VARCHAR(5000)
        );
        """

        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            self.conn.commit()
            print('Table publications created!')

    def drop_publications_table(self):
        sql = "DROP TABLE IF EXISTS publications;"

        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            self.conn.commit()
            print('Table publications dropped!')

    def add_publication(self, pub_data):
        sql = """
            INSERT IGNORE INTO publications
            (date, title, URL, category, content)
            VALUES ( %s, %s, %s, %s, %s)
            """

        with self.conn.cursor(prepared=True) as cursor:
            cursor.execute(sql, tuple(pub_data.values()))
            self.conn.commit()

    def select_all_publications(self):
        sql = "SELECT category, date, title, content FROM publications;"

        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            return result

    def create_crawler_table(self):
        print("Creating crawler table!")
        sql = """
            CREATE TABLE IF NOT EXISTS crawler( 
            last_crawled_date DATETIME
        );
        """
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            self.conn.commit()
            print('Table crawler created!')

    def add_crawler_data(self):
        print("Adding crawler data!")
        sql = """
                    INSERT IGNORE INTO crawler
                    (last_crawled_date)
                    VALUES ( %s)
              """
        data = (datetime.datetime.now(), )
        with self.conn.cursor(prepared=True) as cursor:
            cursor.execute(sql, data)
            self.conn.commit()

    def select_crawler_data(self):
        print("Selecting crawler data!")

        sql = """
            SELECT last_crawled_date FROM crawler LIMIT 1;
            """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
                return result
        except mysql.connector.errors.ProgrammingError:
            self.create_crawler_table()


    def drop_crawler_table(self):
        print("Dropping crawler table!")
        sql = "DROP TABLE IF EXISTS crawler;"

        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            self.conn.commit()
            print('Table crawler dropped!')

if __name__ == '__main__':
    db = DB()
    db.create_crawler_table()
    db.add_crawler_data()
    db.select_crawler_data()
