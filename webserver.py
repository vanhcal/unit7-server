from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

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
				output += "<html><body>Hello!</body></html>"
				self.wfile.write(output)
				print output
				return 

		except IOError:
			self.send_error(404, "File Not Found %s" % self.path)

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



