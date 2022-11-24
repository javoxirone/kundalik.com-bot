import sqlite3


class Db:
    def __init__(self):
        self.db = sqlite3.connect(f'beislam.db', check_same_thread=False)
        self.cursor = self.db.cursor()

    def check_user(self, telegram_id):
        """Checking user if he exists in db or not"""
        self.cursor.execute('''SELECT telegram_id FROM users WHERE telegram_id = ?''', (telegram_id,))
        result = self.cursor.fetchall()
        print(bool(len(result)))
        return bool(len(result))

    def get_user(self, telegram_id):
        """Checking user if he exists in db or not"""
        self.cursor.execute('''SELECT login, password FROM users WHERE telegram_id = ?''', (telegram_id,))
        result = self.cursor.fetchone()
        return result

    def close(self):
        """Close connection with db"""
        self.db.close()

    def create_users(self):
        self.cursor.executescript('''
            DROP TABLE IF EXISTS users;
            CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                first_name TEXT,
                last_name TEXT,
                username TEXT UNIQUE,
                login TEXT UNIQUE,
                password TEXT
            );
        ''')
        self.db.commit()

    def add_user(self, telegram_id, first_name, last_name, username, login, password):
        """Adding user to db"""
        self.cursor.execute('''
            INSERT INTO users(telegram_id, first_name, last_name, username, login, password) VALUES (?,?,?,?,?,?)
        ''', (telegram_id, first_name, last_name, username, login, password))
        self.db.commit()

    def update_user(self, telegram_id, login, password):
        """Adding user to db"""
        self.cursor.execute('''
        UPDATE users SET login=?, password=? WHERE telegram_id=?
        ''', (login, password, telegram_id))
        self.db.commit()
