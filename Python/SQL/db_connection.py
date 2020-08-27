from mysql.connector import MySQLConnection, Error
from db_config import read_db_config

def connect():
    """ Connect to MySQL database """
    db_config = read_db_config() 
    conn = None
    try:
        print("[INFO] Connecting to MySQL database...")
        conn = MySQLConnection(**db_config)
        
        if conn.is_connected():
            print("[INFO] Connection established.")
        else:
            print("[ERROR] Connection failed.")
    except Error as error:
        print(error)
    
    finally:
        if conn is not None and conn.is_connected():
            conn.close()
            print("[INFO] Connection closed.")

if __name__ == "__main__":
    connect()
    
