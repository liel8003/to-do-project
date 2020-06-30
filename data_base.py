import mysql.connector

my_db = mysql.connector.connect(host="localhost",user="root",password="toor",database="to_do_project")
cursor = my_db.cursor()


#cursor.execute("CREATE DATABASE to_do_project")


#cursor.execute("CREATE TABLE employees (employee_id INT AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(255), last_name VARCHAR(255), password VARCHAR(255))")
#cursor.execute("CREATE TABLE lists (list_id INT AUTO_INCREMENT PRIMARY KEY, list_name VARCHAR(255),list_description VARCHAR(255),"
#               "employee_id INTEGER, FOREIGN KEY(employee_id) REFERENCES employees (employee_id))")


#cursor.execute("CREATE TABLE tasks (task_id INT AUTO_INCREMENT PRIMARY KEY, task_name VARCHAR(255),"
#               "task_description VARCHAR(255),list_id INTEGER, FOREIGN KEY(list_id) REFERENCES lists (list_id),"
#               "status VARCHAR(255),priority INTEGER, task_owner INTEGER, FOREIGN KEY(task_owner) REFERENCES employees (employee_id))")
