from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/flask'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    cars = db.relationship('Car', backref="user", lazy=True)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(120), nullable=False)
    model = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)


## Routes for users
@app.route('/users', methods=['POST', 'GET'])
def users():

    ## Create new user
    if request.method == 'POST':
        data = request.json
        new_user = User(username=data['username'], email=data['email'], password=data['password'])
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User created successfully"}
    
    ## Get all users
    elif request.method == 'GET':
        all_users = User.query.all()

        results = []

        for user in all_users:
            users = {
                "username": user.username,
                "email": user.email
            }
            results.append(users)
        return results

##Routes for cars
@app.route('/cars/<user_id>', methods=['POST', 'GET'])
def cars(user_id):

    ##Create new car
    if request.method == 'POST':
        data = request.json
        new_car = Car(make=data['make'], model=data['model'], user_id=int(user_id))
        db.session.add(new_car)
        db.session.commit()
        
        return jsonify(data)
    
    ##Get cars by user ID
    elif request.method == 'GET':
        data = Car.query.filter_by(user_id=int(user_id)).all()

        results = []

        for car in data:
            cars = {
                "make": car.make,
                "model": car.model
            }
            results.append(cars)
        
        return results

        