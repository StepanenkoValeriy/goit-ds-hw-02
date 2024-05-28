from faker import Faker
import sqlite3

# Ініціалізація Faker для генерації випадкових даних
fake = Faker()

# Підключення до бази даних SQLite
conn = sqlite3.connect('task_management.db')
c = conn.cursor()

# Заповнення таблиці користувачів
def seed_users_table(num_users):
    for _ in range(num_users):
        fullname = fake.name()
        email = fake.email()
        c.execute("INSERT INTO users (fullname, email) VALUES (?, ?)", (fullname, email))
    conn.commit()

# Заповнення таблиці статусів
def seed_status_table():
    statuses = ['new', 'in progress', 'completed']
    for status in statuses:
        c.execute("INSERT INTO status (name) VALUES (?)", (status,))
    conn.commit()

# Заповнення таблиці завдань
def seed_tasks_table(num_tasks):
    for _ in range(num_tasks):
        title = fake.text(20)
        description = fake.text()
        status_id = fake.random_int(min=1, max=3)  # Випадковий статус (1, 2 або 3)
        user_id = fake.random_int(min=1, max=10)   # Випадковий користувач (1 до 10)
        c.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)",
                  (title, description, status_id, user_id))
    conn.commit()

# Виклик функцій для заповнення таблиць
seed_users_table(10)    # 10 користувачів
seed_status_table()     # 3 статуси
seed_tasks_table(20)    # 20 завдань

# Закриття з'єднання з базою даних
conn.close()