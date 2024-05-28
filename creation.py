import sqlite3

# Підключення до бази даних SQLite
conn = sqlite3.connect('task_management.db')
c = conn.cursor()

# Створення таблиці користувачів
def create_users_table():
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fullname VARCHAR(100),
                    email VARCHAR(100) UNIQUE
                )''')
    conn.commit()

# Створення таблиці статусів
def create_status_table():
    c.execute('''CREATE TABLE IF NOT EXISTS status (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(50) UNIQUE
                )''')
    conn.commit()

# Створення таблиці завдань
def create_tasks_table():
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(100),
                    description TEXT,
                    status_id INTEGER,
                    user_id INTEGER,
                    FOREIGN KEY (status_id) REFERENCES status(id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )''')
    conn.commit()

# Виклик функцій для створення таблиць
create_users_table()
create_status_table()
create_tasks_table()

# Закриття з'єднання з базою даних
conn.close()