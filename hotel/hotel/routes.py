import os
import secrets
from flask import render_template, url_for, flash, redirect
from hotel import app, db, bcrypt
from hotel.forms import BookRoom, AdminForm, LoginForm, RegistrationForm, NewRoom
from hotel.models import booking, rooms, admins
from flask_login import login_user, current_user, logout_user

lg=0

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html",title="HOME")

@app.route('/availibility')
def availibility():
    return render_template("availibility.html",title="CHECK AVAILIBILITY")

@app.route('/book', methods = ['GET', 'POST'])
def book():
    form = BookRoom()
    if form.validate_on_submit():
        a = rooms.query.filter_by(category=form.category.data).first()
        if (a.available >=form.quantity.data):
            var = form.quantity.data
            for var in range(0,var):
                b = booking(category= form.category.data, checkin= form.checkin.data, checkout= form.checkout.data, name= form.name.data, mobno= form.mobno.data, status='NOT AVAILABLE')
                db.session.add(b)
                db.session.commit()
            a.available = a.available - form.quantity.data
            a.booked = a.booked + form.quantity.data
            db.session.commit()
            flash("Your Room has been Successfully Booked", 'success')
        else:
            flash("Not enough rooms available for the selected category!", 'danger')
        return redirect(url_for('rdirect'))
    return render_template("book.html", title="Book Now",form= form)

@app.route('/rdirect')
def rdirect():
    return render_template("redirect.html")

@app.route('/room_types')
def room_types():
    room = rooms.query.all()
    return render_template("rooms.html",title="ROOM CATEGORIES",room=room)

@app.route('/register', methods = ['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        ad = admins (username=form.username.data, password=hashed_password, name=form.name.data)
        db.session.add(ad)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html", title = 'Register', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
        if current_user.is_authenticated:
            return redirect(url_for("admin"))
        form = LoginForm()
        if form.validate_on_submit():
            ad = admins.query.filter_by(username=form.username.data).first()
            if ad and bcrypt.check_password_hash(ad.password, form.password.data):
                login_user(ad)
                return redirect(url_for('admin'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
        return render_template("login.html", title = "Login",form=form)

@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    return render_template("admin.html", title = "Admin")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/newroom', methods = ['GET', 'POST'])
def newroom():
    form = NewRoom()
    if form.validate_on_submit():
        rtype = rooms (category=form.category.data, quantity=form.quantity.data, beds=form.beds.data, available=form.quantity.data, price=form.price.data, facilities= form.facilities.data)
        db.session.add(rtype)
        db.session.commit()
        flash("Your Room has been Successfully Booked", 'success')
        return redirect(url_for('rdirect'))
    return render_template("room_category.html", title = "Add RoomType", form=form)

@app.route('/bookings')
def bookings():
    booked = booking.query.all()
    return render_template("bookings.html",title="ROOM CATEGORIES",booked=booked)