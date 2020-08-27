import mysql.connector as mysql
from db_config import read_db_config

# WORKING_DATABASE_NAME = 'test'

# db = mysql.connect(
#     host = 'localhost',
#     user = 'root',
#     passwd = '1408jose',
#     database = WORKING_DATABASE_NAME,
# )

# cursor = db.cursor()

# query = """
#     DESCRIBE info
#     """

# cursor.execute(query)
# try:
#     databases = cursor.fetchall()
#     for index,value in enumerate(databases,1):
#         print(f'[{index}] -> {value}'))
# except mysql.errors.InternalError:
#     print(f"[ERROR] Can't fetch that command.")
