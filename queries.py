import sqlite3

# Підключення до бази даних SQLite
conn = sqlite3.connect('task_management.db')
c = conn.cursor()

# Отримати всі завдання певного користувача
def get_user_tasks(user_id):
    c.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
    return c.fetchall()

# Вибрати завдання за певним статусом
def get_tasks_by_status(status):
    c.execute("SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = ?)", (status,))
    return c.fetchall()

# Оновити статус конкретного завдання
def update_task_status(task_id, new_status):
    c.execute("UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = ?) WHERE id = ?", (new_status, task_id))
    conn.commit()

# Отримати список користувачів, які не мають жодного завдання
def get_users_without_tasks():
    c.execute("SELECT * FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks)")
    return c.fetchall()

# Додати нове завдання для конкретного користувача
def add_task(title, description, status_id, user_id):
    c.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)", (title, description, status_id, user_id))
    conn.commit()

# Отримати всі завдання, які ще не завершено
def get_incomplete_tasks():
    c.execute("SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed')")
    return c.fetchall()

# Видалити конкретне завдання
def delete_task(task_id):
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()

# Знайти користувачів з певною електронною поштою
def get_users_by_email_domain(domain):
    c.execute("SELECT * FROM users WHERE email LIKE ?", ('%'+domain,))
    return c.fetchall()

# Оновити ім'я користувача
def update_user_name(user_id, new_name):
    c.execute("UPDATE users SET fullname = ? WHERE id = ?", (new_name, user_id))
    conn.commit()

# Отримати кількість завдань для кожного статусу
def get_task_count_by_status():
    c.execute("SELECT status.name, COUNT(tasks.id) as task_count FROM status LEFT JOIN tasks ON status.id = tasks.status_id GROUP BY status.name")
    return c.fetchall()

# Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти
def get_tasks_by_email_domain(domain):
    c.execute("SELECT tasks.* FROM tasks JOIN users ON tasks.user_id = users.id WHERE users.email LIKE ?", ('%'+domain,))
    return c.fetchall()

# Отримати список завдань, що не мають опису
def get_tasks_without_description():
    c.execute("SELECT * FROM tasks WHERE description IS NULL OR description = ''")
    return c.fetchall()

# Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
def get_users_and_tasks_in_progress():
    c.execute("SELECT users.fullname, tasks.title FROM users INNER JOIN tasks ON users.id = tasks.user_id INNER JOIN status ON tasks.status_id = status.id WHERE status.name = 'in progress'")
    return c.fetchall()

# Отримати користувачів та кількість їхніх завдань
def get_users_and_task_count():
    c.execute("SELECT users.fullname, COUNT(tasks.id) as task_count FROM users LEFT JOIN tasks ON users.id = tasks.user_id GROUP BY users.id")
    return c.fetchall()

# Приклади використання:
print("Завдання користувача з ID=1:", get_user_tasks(1))
print("Завдання зі статусом 'new':", get_tasks_by_status('new'))
update_task_status(1, 'in progress')
print("Користувачі без завдань:", get_users_without_tasks())
add_task("New Task", "Description", 1, 1)
print("Незавершені завдання:", get_incomplete_tasks())
delete_task(1)
print("Користувачі з поштою '@example.com':", get_users_by_email_domain('@example.com'))
update_user_name(1, "New Name")
print("Кількість завдань за кожним статусом:", get_task_count_by_status())
print("Завдання для користувачів з поштою '@example.com':", get_tasks_by_email_domain('@example.com'))
print("Завдання без опису:", get_tasks_without_description())
print("Користувачі та їхні завдання, які є у статусі 'in progress':", get_users_and_tasks_in_progress())
print("Користувачі та кількість їхніх завдань:", get_users_and_task_count())

# Закриття з'єднання з базою даних
conn.close()