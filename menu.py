#!/usr/bin/env python

from flask import Flask, request, render_template, flash

from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/menu/')
def first_menu():
    restaurant = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    output = ''
    for i in items:
        output += i.name
        output += '</br>'
        output += i.price
        output += '</br>'
        output += i.description
        output += '</br></br>'
    return output

@app.route('/all/')
def all_menus():
    output = "<CENTER><h1>WE'RE WORKING ON IT DAMMIT</H1></CENTER>"
    restaurants = session.query(Restaurant.id, Restaurant.name).all()
    menu_items = session.query(MenuItem.restaurant_id, MenuItem.name,
      MenuItem.price, MenuItem.description).all()
    for id, name in restaurants:
        #output += (str(id) + " has a name of " + name + "</br>")
        output += "<h2>" + name + "</h2></br>"
        for item in menu_items:
            if item.restaurant_id == id:
                output += item.name + "</br>" + item.price + "</br>"\
                  + item.description + "</br>"
    return output

@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template("menu.html",restaurant=restaurant, items=items)

@app.route('/restaurants/menus/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
    newItem = MenuItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
return render_template('newmenuitem.html', restaurant_id=restaurant_id)

@app.route('/restaurants/menus/<int:restaurant_id>/<int:menu_id>/edit/',
  methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    item=session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            item.name = request.form['name']
            item.course = request.form['course']
            item.price = request.form['price']
            item.description = request.form['description']
            session.add(item)
            session.commit()
            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    print(item)
    return render_template("edit_menu.html", restaurant_id=restaurant_id,
      menu_id=menu_id, item=item)

@app.route('/restaurants/menus/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    item=session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        print(request)
        if request.form['name']:
            item.id = request.form['ID']
            session.delete(item)
            session.commit()
            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    print(item)
    return render_template("delete_menu_item.html", restaurant_id=restaurant_id,
      menu_id=menu_id, item=item)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
