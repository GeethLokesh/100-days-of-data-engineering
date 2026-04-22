import sqlite3

connection = sqlite3.connect("output/api_data.db")
cursor = connection.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

cursor.execute("SELECT * FROM posts LIMIT 5;")
rows = cursor.fetchall()

for row in rows:
    print(row)

connection.close()