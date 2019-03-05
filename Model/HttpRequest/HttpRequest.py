"""
Zachary Cook

Base class for an http request.
"""

from urllib.request import urlopen
from urllib.error import URLError

"""
"Abstract" class for an http request.
"""
class HttpRequest():
	"""
	Creates the http request.
	"""
	def __init__(self,method,url,default = None):
		self.method = method
		self.url = url
		self.default = default

	"""
	Returns the result.
	"""
	def getResponse(self):
		# Perform the request and get the response.
		try:
			result = urlopen(self.url)
			response = result.read().decode()

			return response
		except URLError as e:
			return self.default