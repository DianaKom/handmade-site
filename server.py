import smtplib
from email.message import EmailMessage
from flask import Flask, send_from_directory, render_template, request
from flask_admin import Admin

from handmade_shop.db import db_session, Category, Product
from flask_admin.contrib.sqla import ModelView



app = Flask(__name__, static_url_path='')
admin = Admin(app, name='shop', template_mode='bootstrap3')
admin.add_view(ModelView(Category, db_session))
admin.add_view(ModelView(Product, db_session))


@app.route("/category/<int:id>")
def category(id):
    cat = Category.query.get(id)
    products_list = Product.query.filter(Product.category_id == cat.id).all()
    print(products_list)
    return render_template("categories.html", category=cat, products_list=products_list)


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory('static', path)


@app.route("/")
def index():
    category_list = Category.query.all()
    return render_template("index.html", category_list=category_list)


@app.route("/registration")
def register():
    pass


@app.route("/products/<int:id>")
def product(id):
    pro = Product.query.get(id)
    return render_template("products.html", pro=pro)


@app.route("/buy", methods=['POST'])
def buy():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Puts connection to SMTP server in TLS mode
    server.ehlo()
    server.login("diana.mixis@gmail.com", "lindalovefire")

    msg = EmailMessage()
    msg['From'] = "diana.mixis@gmail.com"
    msg['To'] = request.form['email']
    msg['Subject'] = 'Thanks!'
    msg.set_content("""\
    Hello! Thanks for shopping! We send EMS all around the world. Please write back with the address! HandMade Dolls
    """)
    server.send_message(msg)

    msg = EmailMessage()
    msg['From'] = "diana.mixis@gmail.com"
    msg['To'] = 'dianakom@hotmail.com'
    msg['Subject'] = 'New customer'
    msg.set_content("""\
    User: {} Product: {}
    """.format(request.form['email'], request.form['product_id']))
    #msg = "Hello! Thanks for shopping! We send EMS all around the world. Please write back with the address! HandMade Dolls"
    server.send_message(msg)
    #msg2 = 'User: {} Product: {}'.format(request.form['email'], request.form['product_id'])
    #server.sendmail("diana.mixis@gmail.com", 'dianakom@hotmail.com', msg2)
    return 'User: {} Product: {}'.format(request.form['email'], request.form['product_id'])

if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)
