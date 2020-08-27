import sqlite3

# db = sqlite3.connect('sample.db')
# cursor = db.cursor()

# # cursor.execute(""" CREATE TABLE users
# #     (id integer PRIMARY KEY, name text)
# # """)
# #insert values
# values = (12412, 'Nathalia')
# # sql_command = """ INSERT INTO users (id,name)
# #                 VALUES(?,?)
# # """
# #Modify data
# # sql_command = """ UPDATE users SET id = 10025 where name = "Diego"
# # """
# #show data
# sql_command = "SELECT name,id FROM users"
# sql_command = "INSERT INTO users (id,name) VALUES (?,?)"
# sql_command = "SELECT name FROM users WHERE id > 1000"
# sql_command = "UPDATE users SET id = 312 WHERE id = 6"

# #check if the table exists
# # sql_command = "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"


# cursor.execute(sql_command)
# data = cursor.fetchone()[0]
# print(data)


# db.commit()

# db.close()

def iterativeMethod(transitions):
    top = len(transitions)
    output = {}
    for i in range(top):
        k = i
        matrix = []
        for j in range(top):
            matrix[i][j] =  transitions[i][j] + ' + ' + transitions[i][k] + f'({transitions[k][k]})*'+ transitions[k][j]

        output.setdefault(k, matrix)