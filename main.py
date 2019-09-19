from flask import Flask, request, redirect, render_template
import re
import cgi

app = Flask(__name__)

app.config['DEBUG'] = True      # displays runtime errors in the browser, too


def verify_email(email):
    pattern = "[0-9A-Za-z]+@[a-z]+.com"
    result = re.match(pattern, email)
    if result:
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

        if len(password) == 0:
            errorPass = "Password is required"

        if verify != password:
            errorVerify = "Passwords dont match"

        if not verify_email(email):
            errorEmail = "email is not correct"

        if not errorUser and not errorPass and not errorVerify and not errorEmail:
            return redirect('/registered?username={username}'.format(username=username))

    return render_template('edit.html', errorPass=errorPass, errorUser=errorUser, errorVerify=errorVerify, errorEmail=errorEmail)


app.run()
