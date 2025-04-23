import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password123", 
    database="testdb"
)

cursor = conn.cursor()

def delete_user(username):
    query = f"DELETE FROM users WHERE username = '{username}'"
    print(f"Executing query: {query}")
    cursor.execute(query)
    conn.commit()

user_input = input("Enter username to delete: ")
delete_user(user_input)

conn.close()
