from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# importing CRUD operations
# this section and the next section must always be added
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# create session and connect to db
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
session = DBSession()
DBSession = sessionmaker(bind = engine)

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			# a page where a user can add a new restaurant
			if self.path.endswith("/restaurants/new"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output = ""
				output += "<html><body>"
				output += "<h1> Make a New Restaurant </h1>"
				output += "<form method='POST' enctype='multipart/form-data' action = '/restaurants/new'>"
				output += "<input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name'>"
				output += "<input type = 'submit' value 'Create'>"
				output += "</html></body>"
				self.wfile.write(output)
				return

			if self.path.endswith("/edit"):
				# we are searching for restaurants by id, so we need to be able to grab IDs out of the URL
				# [2] is because we're grabbing the third element of a zero-indexed array
				restaurantIDPath = self.path.split("/")[2]
				# grab the restaurant entry equal to the ID 
				myRestaurantQuery = session.query(Restaurant).filter_by(jd = restaurantIdPath).one()
				# if you find the query, generate a response
				if myRestaurantQuery != []:
					self.send_response(200)
					self.send_header('Content-type', 'text/html')
					self.end_headers()
					ouput = "<html><body>"
					output += "<h1>"
					output += myRestaurantQuery.name
					output += "</h1>"
					# create a post method, passing in the ID of the restaurant we want to editi
					output += "<form method = 'POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurantIdPath
					output += "<input name = 'newRestaurantName' type='text' placeholder='%s'>" % myRestaurantQuery.name
					output += "<input type = 'submit' value = 'Rename'>"
					output += "</form>"
					output += "</body></html>"

					# add all this output to the w file
					self.wfile.write(output)

			# landing on restaurants will lead to printing all restaurants from the db
			if self.path.endswith("/restaurants"):
				restaurants = session.query(Restaurant).all()
				output = ""
				output += "<a href = '/restaurants/new'> Make a New Restaurant Here </a></br><br>"
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()
				output += ""
				output += "<html><body>"
				# creat a for loop to add all the restaurants to the output
				for restaurant in restaurants:
					output += restaurant.name
					output += "</br>"
					# add tags to edit and delete existing restaurants
					# link to the edit page for a restaurant if user is trying to edit a restaurant
					output += "<a href = '/restaurants/%s/edit'> Edit </a>"
					output += "</br>"
					output += "<a href = '#'> Delete </a>"

				output += "<body></html>"
				# write the output to w file
				self.wfile.write(output)
				return

			# look for a url that ends with /hello
			if self.path.endswith("/hello"):
				# indicate a successful get request if you find a url that ends with hello
				self.send_response(200)
				# indicate that you are responding with text and html to your client
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				# content to send back to the client
				output = ""
				output += "<html><body>"
				output += "Hello!"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return

			if self.path.endswith("/hola"):
				self.send_response(200)
				self.send_header('Content-type', 'text/html')
				self.end_headers()

				# content to send back to the client
				output = ""
				# add a link that goes back to the hello page
				output += "<html><body>"
				output += "&#161Hola <a href='/hello' >Back to Hello</a>"
				output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"
				output += "</body></html>"
				self.wfile.write(output)
				print output
				return 

		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)

		# display responses other than hola and hello
		def do_POST(self):
			try:
				if self.path.endswith("/edit"):
					ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
					if ctype == 'multipart/form-data':
						fields = cgi.parse_multipart(self.rfile, pdict) 
					messagecontent = fields.get('newRestaurantName')
					restaurantIDPath = self.path.split("/")[2]

					myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
					if myRestaurantQuery != []:
						myRestaurantQuery.name = messagecontent[0]
						session.add(myRestaurantQuery)
						session.commit()
						# add a redirect to brineg us back to the restaurants menu
						self.send_response(301)
						self.send_header('Content-type', 'text/html')
						self.send_header('Location', '/restaurants')
						self.end_headers()

				if self.path.endswith("/restaurants/new"):
					# extract the information from the form if the form meets the page address requirements
					ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
					if ctype == 'multipart/form-data':
						fields = cgi.parse_multipart(self.rfile, pdict)
					messagecontent = fields.get('newRestaurantName')

					# Create new Restaurant class
					newRestaurant = Restaurant(name = messagecontent[0])
					session.add(newRestaurant)
					session.commit()

					self.send_response(301)
					self.send_header('Content-type', 'text.html')
					self.send_header('Location', '/restaurants')
					self.end_headers()

					return

				else: 

					# send off the response that indicates a successful post
					self.send_response(301)
					self.end_headers()

					# import cgi to help us decipher the message the user has inputed
					# parse_header parses an html form header such as content type into a main value... 
					# ...and dictionary of parameters
					ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
					# check if this is form data being received
					if ctype == 'multipart/form-data':
						# colect all of the fields in a form
						fields = cgi.parse_multipart(self.rfile, pdict)
						# get value out of a field or set of fields and store them in an array
						messagecontent = fields.get('message')

					# have the server respond with
					output = ""
					output += "<html><<body>"
					output += "<h2> Okay, how about this: </h2>"
					output += "<h1> %s </h1>" % messagecontent[0]

					# message here coincides with the "message" field above in "messagecontent"
					output += "<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name='message' type='text' ><input type='submit' value='Submit'></form>"
					output += "</body></html>"
					self.wfile.write(output)
					print output

				except:
					pass

	def main():
		try:
			port = 8080
			server = HTTPServer(('', port), webserverHandler)
			print "Web server running on port %s" % port
			#keep the server constantly listening until you call cntrl+c or exit the application
			server.serve_forever()

		# exit out of the method when there is a keyboard interrupt (ctrl + c)
		except KeyboardInterrupt:
			print "^C entered, stopping web server..."
			server.socket.close()

if __name__ == '__main__':
	main()



