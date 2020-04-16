from flask import Flask, render_template, url_for, flash, redirect
#from forms import RegistrationForm, LoginForm
from secrets import token_hex
from os import *

#https://stackoverflow.com/questions/31002890/how-to-reference-a-html-template-from-a-different-directory-in-python-flask/31003097

workingDirectory = path.dirname(__file__)
workingDirectory = workingDirectory + "/templates"
print(workingDirectory)

app = Flask(__name__, template_folder=workingDirectory)



@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/budget")
def hello_world2():
    return render_template("budget.html")

@app.route("/update")
def hello_world3():
    return render_template("update.html")


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         flash(f"account created for: {form.username.data}!", "success")
#         return redirect(url_for('hello_world'))
#         #use function name, not app_route
#     return render_template('register.html', title='Register', form=form)
#
#
# @app.route('/login')
# def login():
#     form = LoginForm()
#     return render_template('login.html', title='Login', form=form)

if __name__ == "__main__":
    app.run(debug=True)

