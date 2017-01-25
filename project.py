# the same hello world function as before, but using flask
# input request to get data from a form
# flash is imported for message flashing, jsonify is used to send api data
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# create an instance of the Flask application with the name as the argument
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Making an API Endpoint (GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
		restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
		items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
		return jsonify(MenuItems=[i.serialize for i in items])

# API endpoint for a specific menu item
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
	menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
	return jsonify(MenuItem = menuItem.serialize)

# if we end up at either page/ or page/hello, the hello world function runs
@app.route('/')
# is a way of navigating to restaurants/1, restaurants/2, etc., given the restaurants_id parameter that is passed in
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	# grab first restaurant from db
	restaurant = session.query(Restaurant).first()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
	# instead of manually adding to the ouput, as below, use a template, where restaurant and items are table items being passed in
	#output = '' 
	#for i in items:
		#output += i.name
		#output += '</br>'
		#output += i.price
		#output += '</br>'
		#output += i.description
		#output += '</br>'
	#return output
	return render_template('menu.html', restaurant=restaurant, items=items)

# by default, flask methods only respond to get requests, so we amend the methods to handle both get and post
@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		# obtain inputs from form; extract name field from form
		newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
		# add to session and commit session to db
		session.add(newItem)
		session.commit()
		flash("new menu item created!")
		# redirect user back to main user page
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else: 
		return render_template('new_menu_item.html', restaurant_id = restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		session.add(editedItem)
		session.commit()
		flash("item has been edited!")
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else: 
		return render_template('edit_menu_item.html', restaurant_id = restaurant_id, menu_id = menu_id, i = editedItem)

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		session.delete(itemToDelete)
		session.commit()
		flash("item has been deleted!")
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('delete_menu_item.html', i = itemToDelete)

# restaurant_id will be passed in as the id for the new restaurant
@app.route('/restaurant/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):

# the application run by the python interpreter is named main
# imported python files get __name of file__
# if you're running from python interpreter, run this function; if you're importing, don't do this function

if __name__ == '__main__':
# create a secret key which flask will use to create sessions for our users; usually you'd want a more secure password than this
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)