from flask import Flask, render_template, url_for, flash, redirect,request
#from forms import RegistrationForm, LoginForm
from secrets import token_hex
from os import *
from random import choice, randint
from main import *

#global time
time = 4

#product_list

product_list = [
    {"product": "Miere", "quantity":1, "forecast":7},
    {"product": "Nuci", "quantity":2, "forecast":5},
    {"product": "Alune", "quantity":1, "forecast":5},
    {"product": "Ciocolata", "quantity":3, "forecast":10},
    {"product": "Apa", "quantity":2, "forecast":1},
    {"product": "Paine", "quantity":2, "forecast":1}
]



#daily_list

#fiecare din urmatoarele lista contine un dictionar cu name, average_price si monthly_expense
#si sunt liste cu produse cumparate zilnic, sapt, lunar
print('-----------------------------------------------')
daily_list = Site.get_items_list(Site.security("Bob"), 'daily') 
weekly_list = Site.get_items_list(Site.security("Bob"), 'weekly')
monthly_list = Site.get_items_list(Site.security("Bob"), 'monthly')

#cele 3 expensuri pe care trebuie sa le pui in html
daily_expense = Site.get_daily_forecast(Site.security("Bob"))
weekly_expense = Site.get_week_forecast(Site.security("Bob"))
monthly_expense = Site.get_month_forecast(Site.security("Bob"))

remove_list = Site.get_remove_list(Site.security("Bob"))

print(weekly_list)

print('-----------------------------------------------')


#https://stackoverflow.com/questions/31002890/how-to-reference-a-html-template-from-a-different-directory-in-python-flask/31003097

workingDirectory = path.dirname(__file__)

app = Flask(__name__, template_folder=workingDirectory)

productName =["miere", "geaca", "nuci", "baloane"]
posts = []

for i in range(10):
    posts.append({"product": choice(productName), "quantity": randint(2, 30), "forecast": randint(5, 10)})



@app.route("/", methods =['GET','POST'])
def hello_world():
    return render_template("dummy.html", posts=product_list, 
    daily_budget = daily_expense, weekly_budget = weekly_expense, 
    monthly_budget = monthly_expense)


@app.route("/post", methods =['GET','POST'])
def worker():
    global time 
    global Site

    # iti adauga 
    time += 1
    data = request.get_json()
    
    Site.add_product(Site.security("Bob"), "unknown", data['product'], float(data['price']), int(data['quantity']), time)
    #print(Site.get_daily_forecast(Site.security("Bob")))

    if Site.get_days_left(Site.security("Bob"))[data['product']]:

        if Site.get_days_left(Site.security("Bob"))[data['product']] == 1:
            data['forecast'] = str(Site.get_days_left(Site.security("Bob"))[data['product']]) + " day"
        else:
            data['forecast'] = str(Site.get_days_left(Site.security("Bob"))[data['product']]) + " days"

    else:
        data['forecast'] = "Not known yet"

    daily_list = Site.get_items_list(Site.security("Bob"), 'daily') 
    weekly_list = Site.get_items_list(Site.security("Bob"), 'weekly')
    monthly_list = Site.get_items_list(Site.security("Bob"), 'monthly')

    #cele 3 expensuri pe care trebuie sa le pui in html
    daily_expense = Site.get_daily_forecast(Site.security("Bob"))
    weekly_expense = Site.get_week_forecast(Site.security("Bob"))
    monthly_expense = Site.get_month_forecast(Site.security("Bob"))

    product_list.append(data)

    #print(Site.get_week_forecast(Site.security("Bob")))

    return redirect('/')

@app.route('/daily')
def show():
    return render_template("dummy_budget.html", posts=daily_list, 
    daily_budget = daily_expense, weekly_budget = weekly_expense, 
    monthly_budget = monthly_expense) 


@app.route('/weekly')
def show2():
    return render_template("dummy_budget.html", 
    posts=weekly_list, daily_budget = daily_expense, 
    weekly_budget = weekly_expense, monthly_budget = monthly_expense) 

@app.route('/monthly')
def show3():
    return render_template("dummy_budget.html", posts=monthly_list, 
    daily_budget = daily_expense, weekly_budget = weekly_expense, 
    monthly_budget = monthly_expense) 


if __name__ == "__main__":
 
    app.run(debug=True, use_reloader=True)



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
