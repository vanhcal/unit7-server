# the same hello world function as before, but using flask
from flask import Flask
# create an instance of the Flask application with the name as the argument
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# if we end up at either page/ or page/hello, the hello world function runs
@app.route('/')
# is a way of navigating to restaurants/1, restaurants/2, etc., given the restaurants_id parameter that is passed in
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	# grab first restaurant from db
	restaurant = session.query(Restaurant).first()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
	output = ''
	for i in items:
		output += i.name
		output += '</br>'
		output += i.price
		output += '</br>'
		output += i.description
		output += '</br>'
	return output

@app.route('/restaurant/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
	return "page to create a new menu item. Task 1 complete!"

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
	return "page to edit a new menu item. Task 2 complete!"

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
	return "page to delete a new menu item. Task 3 complete!"

# restaurant_id will be passed in as the id for the new restaurant
@app.route('/restaurant/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):

# the application run by the python interpreter is named main
# imported python files get __name of file__
# if you're running from python interpreter, run this function; if you're importing, don't do this function
if __name__ == '__main__'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)