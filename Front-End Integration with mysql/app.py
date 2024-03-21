from flask import Flask,render_template,request
import mysql.connector

app = Flask(__name__)

my_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    database= "integration",
    password = "password"
)
@app.route('/', methods=['GET'])
def homepage():
    return render_template('response.html', context = 'you are in home page')

@app.route('/user', methods=['GET'])
def user():
    return render_template('form.html', path='/user-data' )

@app.route('/user-data', methods=['POST'])
def user_data():
    u_id = request.form['u_id']
    u_name = request.form['u_name']
    u_age = request.form['u_age']
    u_salary = request.form['u_salary']
    my_cursor = my_connection.cursor()
    q = '''
    insert into user_data(u_id, name, age, salary)
    values(%s,%s,%s,%s);
    '''
    values = (u_id, u_name, u_age, u_salary)
    my_cursor.execute(q, values)
    my_connection.commit()
    return render_template('response.html', context="Check you work bench")

@app.route('/view', methods=['GET'])
def view():
    q = '''
       select * from user_data;
    '''
    my_cursor = my_connection.cursor()
    my_cursor.execute(q)
    data = my_cursor.fetchall()
    return render_template('response.html', context=data)
@app.route('/update', methods=['GET'])
def update():
    return render_template('update.html', path='/updated-age')
@app.route('/updated-age', methods=['POST'])
def update_form():
    u_id = request.form['u_id']
    u_age = request.form['u_age']
    q = '''
    update user_data 
    set age = %s
    where u_id = %s
    '''
    values = (u_age, u_id)
    my_cursor = my_connection.cursor()
    my_cursor.execute(q, values)
    my_connection.commit()
    return render_template('response.html', context=f"Data is update for u_id {u_id} ")

# ---------------------------------------------------------------------------------------

@app.route('/delete', methods=['GET'])
def delete():
    return render_template('delete.html', path='/delete-row')
@app.route('/delete-row', methods=['POST'])
def delete_form():
    u_id = request.form['u_id']
    q = '''
    delete from user_data 
    where u_id = %s
    '''
    values = (u_id,)
    my_cursor = my_connection.cursor()
    my_cursor.execute(q, values)
    my_connection.commit()
    return render_template('response.html', context=f"Data is delete for u_id {u_id} ")

app.run()