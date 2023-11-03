from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
  
  
app = Flask(__name__)
  
  
app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user-system'
  
mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'
            return render_template('user.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (userName, email, password, ))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage = mesage)


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    if request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')

        # Insert the blog post into your database
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO blog_posts (title, content) VALUES (%s, %s)", (title, content))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"message": "Blog post created successfully"})
    elif request.method == 'GET':
        # Retrieve all blog posts from your database
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM blog_posts")
        blog_posts = cursor.fetchall()
        cursor.close()

        blog_data = [{"title": post[1], "content": post[2]} for post in blog_posts]
        return jsonify(blog_data)
    
@app.route('/blog/<int:post_id>/comments', methods=['POST'])
def add_comment(post_id):
    if request.method == 'POST':
        data = request.get_json()
        comment = data.get('comment')

        # Insert the comment into your database, associating it with the specific blog post
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO comments (post_id, comment) VALUES (%s, %s)", (post_id, comment))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"message": "Comment added successfully"})
    
    
if __name__ == "__main__":
    app.run()