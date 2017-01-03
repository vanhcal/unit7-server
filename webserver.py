from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

class webserverHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
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



