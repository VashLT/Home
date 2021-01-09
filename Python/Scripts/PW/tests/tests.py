import sqlite3
import os

os.chdir('.\\Python\\Scripts\\PW\\tests')

conn = sqlite3.connect('data.db')
c = conn.cursor()

# c.execute("""CREATE TABLE IF NOT EXISTS users(
#                 user_id integer PRIMARY KEY AUTOINCREMENT,
#                 name VARCHAR(50),
#                 register_date DATE) """)
# c.execute("""
#              CREATE TABLE IF NOT EXISTS passwords(
#                 pw_id integer PRIMARY KEY AUTOINCREMENT,
#                 user_id integer,
#                 pw_ref VARCHAR(100),
#                 pw_hash VARCHAR(200),
#                 register_date DATE,
#                 FOREIGN KEY(user_id) REFERENCES users(user_id));
#         """)
c.execute("""
    INSERT INTO users VALUES (1, 'jose', '2020-27-12'),
                            (2, 'camila', '2020-27-12'),
                            (3, 'carlos', '2020-27-12');
""")
c.execute("""
    INSERT INTO passwords VALUES (1, 1, 'bbva', 'jose_hash_1', '2020-27-12'),
                                (2, 1, 'agrario', 'jose_hash_1', '2020-27-12'),
                                (3, 2, 'fb', 'camila_hash_1', '2020-27-12'),
                                (4, 2, 'amazon', 'camila_hash_2', '2020-27-12');
""")
conn.commit()
conn.close()
