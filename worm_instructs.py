import numpy as np

class Instructions:
	
	def __init__(self):
		'''
		Only values used in the end
		'''
		self.instructions = np.arange(64).astype(int)
		self.values = np.zeros(64).astype(int)
		self.values[:50] = [int(np.random.random_integers(0,255)) for i in range(0,50)]		#random init for first 20 instructions
		self.memory = dict(zip(self.instructions, self.values))