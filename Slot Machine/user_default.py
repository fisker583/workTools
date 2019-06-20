# _*_ coding: utf-8
import random
import math

# Returns a random integer between min (included) and max (included)
# Using Math.round() will give you a non-uniform distribution!
class UserDefault:
	"""docstring for PRNG"""

	def newValue(self,min,max):
		return math.floor(random.random() * (max - min + 1)) + min
