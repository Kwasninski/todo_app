from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_scss import Scss
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)
Scss(app)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Mytask model ~ row of data
class Mytask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"Task {self.id}"
    

# Define the HomePurchase model ~ row of data
class HomePurchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    bought = db.Column(db.Integer, default=0)
    date_added = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"Home Product {self.id}"
    
with app.app_context():
    db.create_all()


#home page
@app.route("/", methods=['GET', 'POST'])
def index():
    # add task
    if request.method == 'POST':
        current_task= request.form['content']
        new_task = Mytask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"there was an issue adding your task: {e}"
    # see all current task
    else:
        tasks = Mytask.query.order_by(Mytask.date_created).all()
        return render_template("index.html", tasks=tasks)



#delete an item
@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Mytask.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f"there was a problem deleting that task: {e}"


#update an item
@app.route("/update/<int:id>", methods=['GET', 'POST'])
def update(id):
    task = Mytask.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"there was an issue updating your task: {e}"
    else:
        return render_template('update.html', task=task)
    


 #### home purchases part ####   



#Route for "to buy for home" page
@app.route("/for_home", methods=["GET", "POST"])
def to_buy_for_home():
    # add new home purchase
    if request.method == "POST":
        current_home_purchase = request.form['description']
        new_home_purchase = HomePurchase(description=current_home_purchase)
        try:
            db.session.add(new_home_purchase)
            db.session.commit()
            return redirect("/for_home")
        except Exception as e:
            return f"There was an issue adding your home purchase: {e}"
    # see all home purchases
    else:
        home_purchases = HomePurchase.query.order_by(HomePurchase.date_added).all()
        return render_template("for_home.html", home_purchases=home_purchases)



#delete a home purchase
@app.route("/for_home/delete/<int:id>")
def delete_home_purchase(id):
    home_purchase_to_delete = HomePurchase.query.get_or_404(id)
    try:
        db.session.delete(home_purchase_to_delete)
        db.session.commit()
        return redirect("/for_home")
    except Exception as e:
        return f"There was a problem deleting that home purchase: {e}"
    
    
#update a home purchase
@app.route("/for_home/update/<int:id>", methods=["GET", "POST"])
def update_home_purchase(id):
    home_purchase = HomePurchase.query.get_or_404(id)
    if request.method == "POST":
        home_purchase.description = request.form['description']
        try:
            db.session.commit()
            return redirect("/for_home")
        except Exception as e:
            return f"There was a problem updating your home purchase: {e}"
    else:
        return render_template("update_home_purchase.html", home_purchase=home_purchase)

if __name__ == "__main__":
    app.run(debug=True)

