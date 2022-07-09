from read_config import read_db_config
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
        pass

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
        pass

    def create_crawler_table(self):
        pass

    def drop_crawler_table(self):
        pass
if __name__ == '__main__':
    db = DB()