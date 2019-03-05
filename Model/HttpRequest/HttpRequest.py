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
	def __init__(self,method,url,default = None,urlArgs = None):
		self.method = method
		self.url = url
		self.urlArgs = urlArgs
		self.default = default

	"""
	Returns the result.
	"""
	def getResponse(self):
		# Perform the request and get the response.
		try:
			if self.method == "GET":
				result = urlopen(self.url)
			elif self.method == "POST":
				result = urlopen(self.url,self.urlArgs.encode())
			else:
				raise RuntimeError("Unsupported method: " + str(self.method))
			response = result.read().decode()

			return response
		except URLError as e:
			print(e)
			return self.default