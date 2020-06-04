import mysql.connector as mysql

DATABASE_NAME = 'pilot'


def get_database():
    while True:
        try:
            db = mysql.connect(
                host = 'localhost',
                user = 'root',
                passwd = 'chivasregal',
                database = DATABASE_NAME,
            )
            return db
        except mysql.errors.ProgrammingError:
            create_database()
        
def create_database():
    db = mysql.connect(
        host = 'localhost',
        user = 'root',
        passwd = 'chivasregal',
    )
    cursor = db.cursor()
    cursor.execute(f'CREATE DATABASE {DATABASE_NAME}')
