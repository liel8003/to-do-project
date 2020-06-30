from flask import Flask, render_template, request
import mysql.connector
my_db = mysql.connector.connect(host="localhost",user="root",password="toor",database="to_do_project")

app = Flask(__name__)


@app.route("/welcome_page")
def new_user():
    return render_template("welcome_page.html")

@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        password = request.form["password"]
        if firstname == '' or lastname == '' or password == '':
            message = "Please provide your details"
            return render_template('welcome_page.html', message=message)
        else:
            new_user = (firstname,lastname,password)
            cursor = my_db.cursor()
            sql_query_1 = "INSERT INTO employees (first_name,last_name,password) VALUES (%s,%s,%s)"
            cursor.execute(sql_query_1, new_user)
            my_db.commit()
            sql_query_2 = "SELECT employee_id FROM employees ORDER BY employee_id DESC LIMIT 1"
            cursor.execute(sql_query_2)
            for row in cursor.fetchall():
                your_id = row[0]
                print(row[0])
            name = firstname
            return render_template("menu_page.html", your_id=your_id,name=name)

@app.route("/sign_in", methods=['GET', 'POST'])
def sign_in():
    if request.method == "POST":
        employee_id = int(request.form["employee_id"])
        password = request.form["password"]
        if employee_id == '' or password == '':
            message = "Please provide your details"
            return render_template('welcome_page.html', message=message)
        cursor = my_db.cursor()
        sql_query_3 = "SELECT COUNT(*) from employees WHERE employee_id = %s and password = %s"
        user = (employee_id, password,)
        cursor.execute(sql_query_3, user)
        count_row = cursor.fetchone()
        count = count_row[0]
        print(count)
        if count == 0:
            message = "User ID or password are incorrect, please try again"
            return render_template('welcome_page.html', message=message)
        else:
            cursor = my_db.cursor()
            sql_query_4 = "SELECT * from employees WHERE employee_id = %s and password = %s"
            user = (employee_id, password,)
            cursor.execute(sql_query_4, user)
            user_details = []
            for row in cursor.fetchall():
                user_details.append(row)
                print(user_details)
                # user Id #
                print(user_details[0][0])
                # User name #
                print(user_details[0][1])
                # User password #
                print(user_details[0][3])
            if user_details[0][0] == employee_id and user_details[0][3] == password:
                name = user_details[0][1]
                user_id = user_details[0][0]
                your_id = user_id
                return render_template("menu_page.html", name=name,your_id=your_id)

@app.route("/create_list_view")
def create_list_view():
    return render_template("create_list.html")

@app.route("/create_task_view/<list_id>")
def create_task_view(list_id):
    return render_template("add_task.html",list_id=list_id)

@app.route("/create_list", methods=['GET', 'POST'])
def create_list():
    if request.method == "POST":
        list_name = request.form["list_name"]
        description = request.form["description"]
        employee_id = request.form["employee_id"]
        if list_name == '' or description == '' or employee_id == '':
            message = "One of the fields is empty"
            return render_template("create_list.html", message=message)
        else:
            new_list = (list_name,description,employee_id)
            cursor = my_db.cursor()
            sql_query_5 = "INSERT INTO lists (list_name,list_description,employee_id) VALUES (%s,%s,%s)"
            cursor.execute(sql_query_5, new_list)
            my_db.commit()
            sql_query_6 = "SELECT list_id FROM lists ORDER BY list_id DESC LIMIT 1, 1"
            cursor.execute(sql_query_6)
            for row in cursor.fetchall():
                list_id = row[0]
                print(row[0])
            return render_template("create_tasks.html",list_id=list_id)

@app.route("/create_tasks", methods=['GET', 'POST'])
def create_tasks():
    if request.method == "POST":
        list_id = request.form["list_id"]
        employee_id = request.form["employee_id"]
        task_name = request.form["task_name"]
        task_description = request.form["task_description"]
        status = request.form.get("status")
        priority = request.form.get("priority")
        if list_id == '' or employee_id == '' or task_name == '':
            message = "One of the fields is empty"
            return render_template("create_tasks.html", message=message)
        else:
            new_task = (task_name,task_description,list_id,status,priority,employee_id)
            cursor = my_db.cursor()
            sql_query_7 = "INSERT INTO tasks (task_name,task_description,list_id,status,priority,task_owner) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql_query_7, new_task)
            my_db.commit()
            return render_template("create_tasks.html",list_id=list_id)

@app.route("/show_list_view", methods=['GET', 'POST'])
def get_last_task():
    if request.method == "POST":
        list_id = request.form["list_id"]
        employee_id = request.form["employee_id"]
        task_name = request.form["task_name"]
        task_description = request.form["task_description"]
        status = request.form.get("status")
        priority = request.form.get("priority")
        if list_id == '' or employee_id == '' or task_name == '':
            message = "One of the fields is empty"
            return render_template("create_tasks.html", message=message)
        else:
            new_task = (task_name,task_description,list_id,status,priority,employee_id)
            cursor = my_db.cursor()
            sql_query_8 = "INSERT INTO tasks (task_name,task_description,list_id,status,priority,task_owner) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql_query_8, new_task)
            my_db.commit()
            list_id = (list_id,)
            sql_query_9 = "SELECT employees.employee_id, employees.first_name, tasks.task_name, tasks.task_description," \
                          "tasks.status, tasks.priority, tasks.list_id FROM tasks LEFT JOIN employees ON tasks.task_owner = employees.employee_id WHERE list_id = %s"
            cursor.execute(sql_query_9, list_id)
            data = cursor.fetchall()
            return render_template("show_list.html",list_id=list_id,data=data)

@app.route("/show_all_lists_view")
def show_all_lists_view():
    cursor = my_db.cursor()
    sql_query_10 = "SELECT lists.list_id, lists.list_name, lists.list_description, employees.employee_id, employees.first_name " \
                  "FROM lists LEFT JOIN employees on employees.employee_id = lists.employee_id"
    cursor.execute(sql_query_10)
    all_lists = cursor.fetchall()
    return render_template("show_all_lists.html",all_lists=all_lists)



@app.route("/menu_page_view")
def menu_page_view():
    return render_template("menu_page.html")

@app.route("/menu_page_view_2")
def menu_page_view_2():
    return render_template("menu_page_view_2.html")

@app.route("/show_all_tasks_view")
def show_all_tasks_view():
    cursor = my_db.cursor()
    sql_query_11 = "SELECT tasks.list_id, tasks.task_name, tasks.task_description, tasks.status, employees.employee_id, employees.first_name " \
                  "FROM tasks LEFT JOIN employees ON employees.employee_id = tasks.task_owner ORDER BY tasks.list_id ASC"
    cursor.execute(sql_query_11)
    all_tasks = cursor.fetchall()
    return render_template("show_all_tasks.html", all_tasks=all_tasks)

@app.route("/show_all_users_view")
def show_all_users_view():
    cursor = my_db.cursor()
    sql_query_12 = "SELECT * from employees"
    cursor.execute(sql_query_12)
    users = cursor.fetchall()
    return render_template("show_users.html", users=users)

# רציתי להוסיף Dashboard אבל כבר לא הספקתי לייצר לזה UI
@app.route("/dashboard")
def show_dashboard():
    #undone tasks - count#
    cursor = my_db.cursor()
    sql_query_13 = "SELECT employees.employee_id, employees.first_name, count(*) AS open_tasks from tasks " \
                   "LEFT JOIN employees ON tasks.task_owner = employees.employee_id " \
                   "WHERE status = 'undone' GROUP BY employees.employee_id"
    cursor.execute(sql_query_13)
    open_tasks = cursor.fetchall()
    #undone tasks - priority 1#
    sql_query_14 = "SELECT tasks.list_id, tasks.task_name, employees.employee_id,employees.first_name FROM tasks " \
                   "LEFT JOIN employees on tasks.task_owner = employees.employee_id WHERE priority = 1 and status = 'undone' ORDER BY employee_id desc"
    cursor.execute(sql_query_14)
    top_priority = cursor.fetchall()
    #open lists per employee#
    sql_query_15 = "SELECT employees.employee_id, employees.first_name, count(*) as number_of_lists FROM lists " \
                   "LEFT JOIN employees ON employees.employee_id = lists.employee_id GROUP BY employees.first_name"
    cursor.execute(sql_query_15)
    top_priority = cursor.fetchall()
    return render_template("managers_dashboard.html", open_tasks=open_tasks, top_priority=top_priority)

@app.route("/choose_a_list", methods=['GET', 'POST'])
def choose_a_list():
    if request.method == "POST":
        list_id = request.form["list_id"]
        cursor = my_db.cursor()
        list_id = (list_id,)
        sql_query_16 = "SELECT * FROM tasks LEFT JOIN employees ON tasks.task_owner = employees.employee_id WHERE list_id = %s"
        cursor.execute(sql_query_16, list_id)
        data = cursor.fetchall()
        return render_template("show_specific_list.html", data=data,list_id=list_id)

@app.route("/choose_a_list_2", methods=['GET', 'POST'])
def last_task():
    if request.method == "POST":
        list_id = request.form["list_id"]
        employee_id = request.form["employee_id"]
        task_name = request.form["task_name"]
        task_description = request.form["task_description"]
        status = request.form.get("status")
        priority = request.form.get("priority")
        if list_id == '' or employee_id == '' or task_name == '':
            message = "One of the fields is empty"
            return render_template("add_task.html", message=message)
        else:
            new_task = (task_name,task_description,list_id,status,priority,employee_id)
            cursor = my_db.cursor()
            sql_query_8 = "INSERT INTO tasks (task_name,task_description,list_id,status,priority,task_owner) VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql_query_8, new_task)
            my_db.commit()
            list_id = (list_id,)
            sql_query_20 = "SELECT * FROM tasks LEFT JOIN employees ON tasks.task_owner = employees.employee_id WHERE list_id = %s"
            cursor.execute(sql_query_20, list_id)
            data = cursor.fetchall()
            return render_template("show_specific_list.html", data=data,list_id=list_id)


@app.route("/update_your_list/<list_id>")
def update_your_list(list_id):
    list_id=list_id
    cursor = my_db.cursor()
    list_id = (list_id,)
    sql_query_17 = "SELECT * FROM tasks LEFT JOIN employees ON tasks.task_owner = employees.employee_id WHERE list_id = %s"
    cursor.execute(sql_query_17, list_id)
    data = cursor.fetchall()
    return render_template("update_your_list.html",list_id=list_id,data=data)

@app.route("/remove_task", methods=['GET', 'POST'])
def remove_task():
    if request.method == "POST":
        removed_tasks = request.form.getlist('remove_task_id')
        list_id = request.form.get('list_id')
        list_id = (list_id,)
        cursor = my_db.cursor()
        sql_query_18 = "DELETE FROM tasks WHERE task_id = %s"
        for item in removed_tasks:
            cursor.execute(sql_query_18, (item,))
            my_db.commit()
        sql_query_19 = "SELECT * FROM tasks LEFT JOIN employees ON tasks.task_owner = employees.employee_id WHERE list_id = %s"
        cursor.execute(sql_query_19, list_id)
        data = cursor.fetchall()
        print(data)
        print(list_id)
        return render_template("show_specific_list.html",data=data,list_id=list_id)


@app.route("/change_status_and_priority_view/<list_id>", methods=['GET', 'POST'])
def change_status_and_priority(list_id):
    if request.method == "POST":
        status = request.form['status']
        priority = request.form['priority']
        task_id = request.form.get('task_id')
        list_id = request.form.get('list_id')
        input_data = (status,priority,task_id)
        cursor = my_db.cursor()
        sql_query_22 = "UPDATE tasks SET status = %s, priority = %s WHERE task_id = %s"
        cursor.execute(sql_query_22,input_data)
        my_db.commit()
        list_id = list_id
        cursor = my_db.cursor()
        list_id = (list_id,)
        sql_query_17 = "SELECT * FROM tasks LEFT JOIN employees ON tasks.task_owner = employees.employee_id WHERE list_id = %s"
        cursor.execute(sql_query_17, list_id)
        data = cursor.fetchall()
        message = "Mark only one row each time, and dont forget to mark the checkboxes"
        return render_template("change_status_and_priority.html", data=data, list_id=list_id,message=message)
    else:
        cursor = my_db.cursor()
        list_id = (list_id,)
        print(list_id)
        sql_query_21 = "SELECT * FROM tasks LEFT JOIN employees ON tasks.task_owner = employees.employee_id WHERE list_id = %s"
        cursor.execute(sql_query_21, list_id)
        data = cursor.fetchall()
        message = "Change only one row each time, and dont forget to mark the checkboxes"
        return render_template("change_status_and_priority.html", data=data, list_id=list_id,message=message)




if __name__== "__main__":
    app.run(host= "localhost",port=8052,debug=True)

