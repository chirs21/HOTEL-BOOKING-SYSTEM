from hotel import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_admin(admin_id):
    return admins.query.get(int(admin_id))

class booking(db.Model):
    roomno = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(20), nullable=False)
    checkin = db.Column(db.DateTime,  default=datetime.date)
    checkout = db.Column(db.DateTime, default=datetime.date)
    name = db.Column(db.String(40),  nullable=False)
    mobno = db.Column(db.Integer,  nullable=False)
    status = db.Column(db.String(20), default = "AVAILABLE")

    def __repr__(self):
        return f"event('{self.roomno}', '{self.category}', '{self.checkin}', '{self.checkout}', '{self.name}', '{self.mobno}', '{self.status}')"

class rooms(db.Model):
    category = db.Column(db.String(20), primary_key=True)
    quantity = db.Column(db.Integer, default=5)
    beds = db.Column(db.Integer,  nullable=False)
    available = db.Column(db.Integer, default=5)
    booked = db.Column(db.Integer, default=0)
    price = db.Column(db.Integer,  nullable=False)
    facilities = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"event('{self.category}', '{self.quantity}', '{self.beds}', '{self.available}', '{self.booked}', '{self.price}', '{self.facilities}')"

class admins(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"event( '{self.username}', '{self.password}', '{self.name}')"
