import tornado.ioloop
import tornado.web
from pymongo import * 
import simplejson as json

class Blog(tornado.web.RequestHandler):		
	def get(self):
		# Db stuff
		connection = Connection()
        # Query the db
		db = connection.Blog
		posts = db.Posts
		# Get the posts
		myPosts = posts.find()
		# List
		results = []
		# Construct a list that will be
		# converted into JSON format
		for post in myPosts:
			print post['message']
			results.append({"message" : post['message']})

		# print the results
		print json.JSONEncoder().encode(results)
		# send the results out in json format
		self.set_header("Content-Type", "application/json")
		self.set_header('Access-Control-Allow-Origin', '*')
		self.write(json.JSONEncoder().encode(results))

	def post(self):
		# Read in the request data
		data = tornado.escape.json_decode(self.request.body)
		# Print to server console
		print data["message"]
		# Construct Document
		dbData = {
					"message": str(data["message"])
				}
		# Make connection
		connection = Connection()
		db = connection.Blog
		posts = db.Posts
		# Add document
		posts.insert(dbData)

# Global server settings
app_settings = {
	"debug": True
}

# URL Routing
application = tornado.web.Application([
									(r"/blog", Blog)
], app_settings)

# server constructor
if __name__ == "__main__":
	# Define the port to listen on
	application.listen(8080)
	# Start the server
	tornado.ioloop.IOLoop.instance().start()