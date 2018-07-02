import numpy as np

class Loader:
	
	def __init__(self, filename):
		self.f = np.genfromtxt(filename, delimiter= ' ', dtype = str)
		#print(self.f.shape)
		 
		
loader = Loader('map.txt')