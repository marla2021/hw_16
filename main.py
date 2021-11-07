import json

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from data import users, orders, offers


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///table.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False
db = SQLAlchemy(app)



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text(50))
    last_name = db.Column(db.Text(50))
    age = db.Column(db.Integer)
    email = db.Column(db.Text(50))
    role = db.Column(db.Text(30))
    phone = db.Column(db.Text(15))
    def to_dict(self):
        return {
            "id":self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(50))
    description = db.Column(db.Text(200))
    start_date = db.Column(db.Integer)
    end_date = db.Column(db.Integer)
    address = db.Column(db.Text(70))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def to_dict(self):
        return {
            "id":self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id,
        }
class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer,db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def to_dict(self):
        return {
            "id":self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id,
        }


db.drop_all()
db.create_all()


for user in users:
    new_user = User(
        id = user["id"],
        first_name=user["first_name"],
        last_name = user["last_name"],
        age = user["age"],
        email = user["email"],
        role = user["role"],
        phone = user["phone"],
    )
    db.session.add(new_user)
    db.session.commit()


for order in orders:
    new_order = Order(
        id = order["id"],
        name=order["name"],
        description = order["description"],
        start_date = order["start_date"],
        end_date = order["end_date"],
        address = order["address"],
        price = order["price"],
        customer_id=order["customer_id"],
        executor_id=order["executor_id"],
    )
    db.session.add(new_order)
    db.session.commit()


for offer in offers:
    new_offer = Offer(
        id = offer["id"],
        order_id=offer["order_id"],
        executor_id= offer["executor_id"]
    )
    db.session.add(new_offer)
    db.session.commit()




@app.route("/users", methods=['GET','POST'])
def users():
    if request.method == "GET":
        res =[]
        for u in User.query.all():
            res.append(u.to_dict())
        return json.dumps(res), 200,{'Content-Type':'application/json; charset=UTF-8'}
    elif request.method == "POST":
        user = json.loads(request.data)
        new_user = User(
            id = user["id"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            age=user["age"],
            email=user["email"],
            role=user["role"],
            phone=user["phone"],
        )
        db.session.add(new_user)
        db.session.commit()
        return "", 204


@app.route("/user/<int:id>", methods=['GET','POST', 'DELETE', 'PUT'])
def user(id):
    if request.method == "GET":
        return json.dumps(User.query.get(id).to_dict()), 200,{'Content-Type':'application/json; charset=UTF-8'}
    elif request.method == 'DELETE':
        u = User.query.get(id)
        db.session.delete(u)
        db.session.commit()
        return "",204
    elif request.method == 'PUT':
        data = json.loads(request.data)
        u = User.query.get(id)
        u.first_name = user["first_name"],
        u.last_name = user["last_name"],
        u.age = user["age"],
        u.email = user["email"],
        u.role = user["role"],
        u.phone = user["phone"],
        db.session.add(u)
        db.session.commit()
        return "", 204


@app.route("/orders", methods=['GET','POST'])
def orders():
    if request.method == "GET":
        res =[]
        for ord in Order.query.all():
            res.append(ord.to_dict())
        return json.dumps(res), 200,{'Content-Type':'application/json; charset=UTF-8'}
    elif request.method == "POST":
        order = json.loads(request.data)
        new_order = Order(
            id=order["id"],
            name=order["name"],
            description=order["description"],
            start_date=order["start_date"],
            end_date=order["end_date"],
            address=order["address"],
            price=order["price"],
            customer_id=order["customer_id"],
            executor_id=order["executor_id"],
        )
        return "", 204


@app.route("/order/<int:id>", methods=['GET','POST', 'DELETE', 'PUT'])
def order(id):
    if request.method == "GET":
        return json.dumps(Order.query.get(id).to_dict()), 200
    elif request.method == 'DELETE':
        order = Order.query.get(id)
        db.session.delete(order)
        db.session.commit()
        return "",204
    elif request.method == 'PUT':
        data = json.loads(request.data)
        order = Order.query.get(id)
        order.id = order["id"],
        order.name = order["name"],
        order.description = order["description"],
        order.start_date = order["start_date"],
        order.end_date = order["end_date"],
        order.address = order["address"],
        order.price = order["price"],
        order.customer_id = order["customer_id"],
        order.executor_id = order["executor_id"]
        db.session.add(order)
        db.session.commit()
        return "", 204


@app.route("/offers", methods=['GET','POST'])
def offers():
    if request.method == "GET":
        res =[]
        for ofe in Offer.query.all():
            res.append(ofe.to_dict())
        return json.dumps(res), 200
    elif request.method == "POST":
        offer = json.loads(request.data)
        new_offer = Offer(
            id=offer["id"],
            order_id=offer["order_id"],
            executor_id=offer["executor_id"],
        )
        return "", 204


@app.route("/offer/<int:id>", methods=['GET','POST', 'DELETE', 'PUT'])
def offer(id):
    if request.method == "GET":
        return json.dumps(Offer.query.get(id).to_dict()), 200
    elif request.method == 'DELETE':
        offe = Offer.query.get(id)
        db.session.delete(offe)
        db.session.commit()
        return "",204
    elif request.method == 'PUT':
        data = json.loads(request.data)
        offer = Offer.query.get(id)
        offer.id = offer["id"],
        offer.order_id = offer["order_id"],
        offer.executor_id = offer["executor_id"]
        db.session.add(offer)
        db.session.commit()
        return "", 204







if __name__ == '__main__':
    app.run(debug=True)




