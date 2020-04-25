from flask import Flask, render_template, url_for, flash, redirect,request
#from forms import RegistrationForm, LoginForm
from secrets import token_hex
from os import *
from random import choice, randint
from main import *

time = 0

#https://stackoverflow.com/questions/31002890/how-to-reference-a-html-template-from-a-different-directory-in-python-flask/31003097

workingDirectory = path.dirname(__file__)
#workingDirectory = workingDirectory + "/Templates/Front-FoodTracker-master"
#print(workingDirectory)

app = Flask(__name__, template_folder=workingDirectory)

productName =["miere", "geaca", "nuci", "baloane"]
posts = []

for i in range(10):
    posts.append({"product": choice(productName), "quantity": randint(2, 30), "forecast": randint(5, 10)})

print(posts)

@app.route("/", methods =['GET','POST'])
def hello_world():
    return render_template("table.html", posts=posts)


@app.route("/post", methods =['GET','POST'])
def worker():
    global time 
    global Site
    time += 1
    data = request.get_json()
    
    Site.add_product(Site.security("Bob"), "unknown", data['product'], float(data['price']), int(data['quantity']), time)

    if Site.get_days_left(Site.security("Bob"))[data['product']]:

        if Site.get_days_left(Site.security("Bob"))[data['product']] == 1:
            data['forecast'] = str(Site.get_days_left(Site.security("Bob"))[data['product']]) + " day"
        else:
            data['forecast'] = str(Site.get_days_left(Site.security("Bob"))[data['product']]) + " days"

    else:
        data['forecast'] = "Not known yet"

    posts.append(data)
    
    print(Site.get_week_forecast(Site.security("Bob")))

    return redirect('/')

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
    #Site = siteFunctions()
    app.run(debug=True, use_reloader=True)

