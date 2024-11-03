import sqlite3
import time
import math
import datetime



class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
    
    def addUser(self, username, email, password_hash):
        try:
            self.__cur.execute('SELECT COUNT() as "count" FROM users WHERE email = ?', (email,))
            res = self.__cur.fetchone()
            if res['count'] > 0:
                return False
            
            tm = math.floor(time.time())
            self.__cur.execute('INSERT INTO users VALUES (NULL, ?, ?, ?, ?, ?)', (username, email, password_hash, 0, tm))
            self.__db.commit()
            return True
        except sqlite3.Error as e:
            print(f'Ошибка добавления пользователя: {str(e)}')
            return False
    
    def getUser(self, user_id):
        try:
            self.__cur.execute('SELECT * FROM users WHERE id = ? LIMIT 1', (user_id,))
            return self.__cur.fetchone()
        except sqlite3.Error as e:
            print(f'Ошибка получения пользователя: {str(e)}')
            return None
    
    def getUserByEmail(self, email):
        try:
            self.__cur.execute('SELECT * FROM users WHERE email = ? LIMIT 1', (email,))
            return self.__cur.fetchone()
        except sqlite3.Error as e:
            print(f'Ошибка поиска пользователя по email: {str(e)}')
            return None
    
    # Обновление данных пользователя
    def updateUser(self, user_id, username, email):
        try:
            self.__cur.execute('UPDATE users SET username = ?, email = ? WHERE id = ?', (username, email, user_id))
            self.__db.commit()
            return True
        except sqlite3.Error as e:
            print('Ошибка обновления пользователя: ' + str(e))
            return False

    # Обновление пароля
    def updatePassword(self, user_id, password_hash):
        try:
            self.__cur.execute('UPDATE users SET password = ? WHERE id = ?', (password_hash, user_id))
            self.__db.commit()
            return True
        except sqlite3.Error as e:
            print('Ошибка обновления пароля: ' + str(e))
            return False