import os
import urllib
import datetime
import random
import base64

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import images
from google.appengine.api import urlfetch

# TAKE NODE IMAGE OBJECT
class TNImage(db.Model):
    image_id = db.StringProperty(multiline=False)
    image_file = db.BlobProperty(default=None)
    image_date = db.DateTimeProperty(auto_now_add=True)

# TAKE NODE MAIN PAGE
class TNMain(webapp.RequestHandler):
	def get(self):       
		self.response.out.write('Driven By TakeNode')

# TAKE NODE SAVE IMAGE
class TNSave(webapp.RequestHandler):
	# SERVER SET
	takenode_server_id = 0
	takenode_server_url = 'http://img-0.foread.me'
	
	def post(self):
		takenode_image = TNImage()
		takenode_image.image_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S')+str(random.randint(100000, 999999))+str(TNSave.takenode_server_id)
		takenode_image.image_file = db.Blob(self.request.get('takenode'))
		if (len(takenode_image.image_file) > 0):
			takenode_image.put()
			self.response.out.write('{"node":'+str(TNSave.takenode_server_id)+',"id":"'+takenode_image.image_id+'","url":"'+TNSave.takenode_server_url+'/view/'+takenode_image.image_id+'"}')
		else:
			self.response.out.write('{"node":0}')

	def get(self, image_url):	
		takenode_image = TNImage()
		takenode_image.image_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S')+str(random.randint(100000, 999999))+str(TNSave.takenode_server_id)
		takenode_image.image_file = db.Blob(urlfetch.Fetch(base64.b64decode(urllib.unquote(image_url))).content)
		if (len(takenode_image.image_file) > 0):
			takenode_image.put()
			self.response.out.write('{"node":'+str(TNSave.takenode_server_id)+',"id":"'+takenode_image.image_id+'","url":"'+TNSave.takenode_server_url+'/view/'+takenode_image.image_id+'"}')
		else:
			self.response.out.write('{"node":0}')

class TNView(webapp.RequestHandler):
	def get(self, id):
		result = db.GqlQuery("SELECT * FROM TNImage WHERE image_id = :1 LIMIT 1", id).fetch(1)
		if (len(result) > 0):
			image_result = result[0]
			if (image_result and image_result.image_file):
				# WIDTH x HEIGHT
				if ('x' in self.request.query_string):
					# READ IMAGE
					image = images.Image(image_result.image_file)
					# ACTION
					image.resize(int(self.request.query_string.split('x')[0]), int(self.request.query_string.split('x')[1]))
					# OUTPUT IMAGE
					new_image = image.execute_transforms(output_encoding = images.PNG)
					self.response.headers['Content-Type'] = 'image/png'
					self.response.out.write(new_image)
					return

				# CROP
				if (':' in self.request.query_string):
					# READ IMAGE
					image = images.Image(image_result.image_file)
					# ACTION
					image.crop(float(self.request.query_string.split(':')[0]), float(self.request.query_string.split(':')[1]), float(self.request.query_string.split(':')[2]), float(self.request.query_string.split(':')[3]))
					# OUTPUT IMAGE
					new_image = image.execute_transforms(output_encoding = images.PNG)
					self.response.headers['Content-Type'] = 'image/png'
					self.response.out.write(new_image)
					return

				# HORIZONTAL FLIP
				if ('h' in self.request.query_string):
					# READ IMAGE
					image = images.Image(image_result.image_file)
					# ACTION
					image.horizontal_flip()
					# OUTPUT IMAGE
					new_image = image.execute_transforms(output_encoding = images.PNG)
					self.response.headers['Content-Type'] = 'image/png'
					self.response.out.write(new_image)
					return

				# VERTICAL FLIP
				if ('v' in self.request.query_string):
					# READ IMAGE
					image = images.Image(image_result.image_file)
					# ACTION
					image.vertical_flip()
					# OUTPUT IMAGE
					new_image = image.execute_transforms(output_encoding = images.PNG)
					self.response.headers['Content-Type'] = 'image/png'
					self.response.out.write(new_image)
					return

				# ROTATE
				if ('90' in self.request.query_string):
					# READ IMAGE
					image = images.Image(image_result.image_file)
					# ACTION
					image.rotate(90)
					# OUTPUT IMAGE
					new_image = image.execute_transforms(output_encoding = images.PNG)
					self.response.headers['Content-Type'] = 'image/png'
					self.response.out.write(new_image)
					return

				if ('180' in self.request.query_string):
					# READ IMAGE
					image = images.Image(image_result.image_file)
					# ACTION
					image.rotate(180)
					# OUTPUT IMAGE
					new_image = image.execute_transforms(output_encoding = images.PNG)
					self.response.headers['Content-Type'] = 'image/png'
					self.response.out.write(new_image)
					return

				if ('270' in self.request.query_string):
					# READ IMAGE
					image = images.Image(image_result.image_file)
					# ACTION
					image.rotate(270)
					# OUTPUT IMAGE
					new_image = image.execute_transforms(output_encoding = images.PNG)
					self.response.headers['Content-Type'] = 'image/png'
					self.response.out.write(new_image)
					return

				# DEFAULT
				if (self.request.query_string == ''):
					self.response.headers['Content-Type'] = 'image/png'
					self.response.out.write(image_result.image_file)	
			else:
				# SHOW NOIMAGE
				self.response.out.write('ERROR')
		else:
			# SHOW NOIMAGE
			self.response.out.write('ERROR')

class TNStats(webapp.RequestHandler):
	def get(self):
		takenode_image = TNImage()
		takenode_count = takenode_image.all().count()
		if (takenode_count):
			self.response.out.write(takenode_count)
		else:
			self.response.out.write('0')

application = webapp.WSGIApplication([
	('/', TNMain),
	('/save', TNSave),
	('/save/(.*)', TNSave),
	('/view/(.*)', TNView),
	('/stats', TNStats)
	],
	debug=True
)

def main():
	run_wsgi_app(application)

if __name__ == '__main__':
	main()