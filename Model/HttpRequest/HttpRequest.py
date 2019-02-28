"""
Zachary Cook

Base class for an http request.
"""

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
		# TODO: Send HTTP request
		return self.default