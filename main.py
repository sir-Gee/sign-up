from flask import Flask, request, redirect, render_template
import re
import cgi

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too

users = []


def verify_email(email):
    pattern = "[0-9A-Za-z]+@[a-z]+.[a-z]+"
    result = re.match(pattern, email)
    if result:
        return True


def verify_username(username):
    pattern = "[0-9A-Za-z]{3,20}?"
    result = re.match(pattern, username)
    if result:
        return True

def check_whitespace(username):
    for letter in username:
        if letter.isspace():
            return False
    return True


@app.route("/registered", methods=['POST', 'GET'])
def register():
    return render_template("registered.html", welcome=request.args.get('username'))


@app.route("/", methods=['POST', 'GET'])
def index():
    username = ""
    password = ""
    errorUser = ""
    errorPass = ""
    errorVerify = ""
    errorEmail = ""

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        email = request.form['email']

        if len(username) == 0:
            errorUser = "Username is required"
        elif len(username) < 3 or len(username) > 20:
            errorUser = "Username is less than 3 symbols or more than 20"
        elif not check_whitespace(username):
            errorUser = "Username should NOT have any spaces"
        elif not verify_username(username):
            errorUser = "Your username is not correct"

        if len(password) == 0:
            errorPass = "Password is required"

        if verify != password:
            errorVerify = "Passwords dont match"

        if email == "":
            pass
        elif not verify_email(email):
            errorEmail = "email is not correct"

        if not errorUser and not errorPass and not errorVerify and not errorEmail:
            users.append(username)
            return redirect('/registered?username={username}'.format(username=username))

    return render_template('edit.html', errorPass=errorPass, errorUser=errorUser, errorVerify=errorVerify,
                           errorEmail=errorEmail)


@app.route("/whosregistered")
def show_registered():

    return render_template('whosregistered.html', users=users)

app.run()
