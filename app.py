
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, render_template_string, request, redirect
import mysql.connector
app = Flask(__name__)

database = mysql.connector.connect (
    host = "localhost",
    user = "root",
    password = "[DB PASSWORD HERE]",
    database = "exam"
    )

cursor = database.cursor()
#use the line under to create a database, you don't need one if you already have one on
cursor.execute("CREATE TABLE IF NOT EXISTS UserList (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")
 
# By default redirects to LOGIN page
@app.route('/', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        # check if user has the given password
        username = request.form.get("username")
        password = request.form.get("password")
        sql = f"SELECT (password = '{password}') AS correct_password FROM UserList WHERE username = '{username}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            if result[0][0] == 1: # password matches database
                return redirect("/home")
            else: 
                # password did not match
                # show a warning message
                message = "Wrong Password"
                return render_template_string("""
                <html lang="en" xmlns="http://www.w3.org/1999/xhtml">
                <head>
                    <meta charset="utf-8" />
                    <title>LOGIN</title>
                </head>
                <body>
                <div class="container text-left">
                    Please log in
                    <div class="inputbox-login-user" id="login-user">
                        <form method="POST" action="/">
                            <div class="form-group">
                                <input class="form-control user" name="username" placeholder="" required>
                                <input class="form-control user" name="password" placeholder="" required>
                                <button class="btn btn-primary" id="user-submit" type="submit">Log In</button>
                            </div>
                            <p style="color: red;">{{ message }}</p>   
                        </form>
                    </div>
                    Don't have an account? <a href="/register">Register here</a>
                </div>
                </body>
                </html>
                """, message=message)
                
        else:
            message = "Wrong Password or Username"
            return render_template_string("""
            <html lang="en" xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <meta charset="utf-8" />
                <title>LOGIN</title>
            </head>
            <body>
            <div class="container text-left">
                Please log in
                <div class="inputbox-login-user" id="login-user">
                    <form method="POST" action="/">
                        <div class="form-group">
                            <input class="form-control user" name="username" placeholder="" required>
                            <input class="form-control user" name="password" placeholder="" required>
                            <button class="btn btn-primary" id="user-submit" type="submit">Log In</button>
                        </div>
                        <p style="color: red;">{{ message }}</p>   
                    </form>
                </div>
                Don't have an account? <a href="/register">Register here</a>
            </div>
            </body>
            </html>
            """, message=message)
           
    return render_template("login.html")

@app.route('/home')
def home():
    sql = "SELECT id, username, password FROM UserList"
    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result) == 0:
        list = ""
    else:
        list = result
    return render_template("home.html", user='', list = list)

@app.route('/register', methods = ["POST", "GET"])
def register(): 
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        sql = f"SELECT (password = '{password}') AS correct_password FROM UserList WHERE username = '{username}'"
        cursor.execute(sql)
        result = cursor.fetchall()
        if result:
            if result[0][0] == 1:
                message = "Username Taken"
                return render_template_string("""
                <html lang="en" xmlns="http://www.w3.org/1999/xhtml">
                <head>
                    <meta charset="utf-8" />
                    <title>REGISTER</title>
                </head>
                <body>
                    <div class="container text-left">
                        Create an account
                        <div class="inputbox-login-user" id="login-user">
                            <form method="POST" action="/register">
                                <div class="form-group">
                                    <input class="form-control user" name="username" placeholder="" required>
                                    <input class="form-control user" name="password" placeholder="" required>
                                    <button class="btn btn-primary" id="user-submit" type="submit">Register</button>
                                </div>
                                <p style="color: red;">{{ message }}</p>              
                            </form>
                        </div>
                        Already have an account? <a href="/">Log in here</a>
                    </div>
                </body>
                </html>
                """, message=message)
            else:
                message = "Username Taken"
                return render_template_string("""
                <html lang="en" xmlns="http://www.w3.org/1999/xhtml">
                <head>
                    <meta charset="utf-8" />
                    <title>REGISTER</title>
                </head>
                <body>
                    <div class="container text-left">
                        Create an account
                        <div class="inputbox-login-user" id="login-user">
                            <form method="POST" action="/register">
                                <div class="form-group">
                                    <input class="form-control user" name="username" placeholder="" required>
                                    <input class="form-control user" name="password" placeholder="" required>
                                    <button class="btn btn-primary" id="user-submit" type="submit">Register</button>
                                </div>
                                <p style="color: red;">{{ message }}</p>              
                            </form>
                        </div>
                        Already have an account? <a href="/">Log in here</a>
                    </div>
                </body>
                </html>
                """, message=message)
                
        # check if user already exists, and fail in that case, showing Warning message
        sql = "INSERT INTO UserList (username, password) VALUES (%s, %s)"
        values = [username, password]
        cursor.execute(sql, values)
        database.commit()
        return redirect("/home")
    return render_template("register.html")


@app.route('/delete/<int:id>')
def delete(id):
    sql = "DELETE FROM UserList WHERE id = %s"
    value = [id, ]
    cursor.execute(sql, value)
    database.commit()
    return redirect("/home")


app.run(debug=True)



