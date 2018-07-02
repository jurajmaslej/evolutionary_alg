from data_loader import Loader
from worm_instructs import Instructions
import numpy as np
import copy

class Wallee:
	''' ToDos> do not die
	
	On instructions:
		incerement
		decrement
		jump
		printout
	
	On map (7x7 shape):
		up, down, left, right
	'''
	
	def __init__(self, instructions, name= None):
		l = Loader('map.txt')
		self.wmap = l.f		#frickin mint syntax, world map created
		
		self.boundaries = np.array([self.wmap.shape[0], self.wmap.shape[1]])
		if self.boundaries[0] == self.boundaries[1]:
			self.boundaries = self.boundaries[0]
		
		self.name = name
		pos = np.where(self.wmap == 'S')
		self.row = pos[0][0]
		self.col = pos[1][0]
		self.instructions = instructions
		self.__instructions2 = instructions
		self.treasures = 0
		self.steps = 0
		self.path = []
		self.complete_path = []
		self.onway = []
	
	def __repr__(self):
		return 'Walle tr:' + str(self.treasures) + ' st:' + str(self.steps) + ' |' + str(self.name) + '| ' + ''.join(self.path)
		
	def treasure_count(self):
		count = 0
		for i in self.wmap:
			if 'P' in i:
				count += 1
		return count
	
	def restore_robot(self):
		l = Loader('map2.txt')
		self.wmap = l.f
		pos = np.where(self.wmap == 'S')
		self.row = pos[0][0]
		self.col = pos[1][0]

	def translate_one(self, one_inst):
		one_inst = bin(one_inst)
		return one_inst[:2] + '0'*(10 - len(one_inst)) + one_inst[2:]
		
	def trim_0b(self, instructions):
		return [b[2:] for b in instructions]
	
	def in_bounds(self, num):
		if 0 <= num < self.boundaries:
			return True
		return False
		
	def execute_robot_inst(self, inst):	#inst = one binary instruction
		inst_list = map(int, list(inst))
		non_zero = np.count_nonzero(inst_list)
		died = False
		#print (' inst to rbt ', inst_list[-2:])
		if inst_list[-2:] == [0,0]:
			if self.in_bounds(self.row - 1):
				self.row -= 1
			else:
				died = True
			self.path.append('U')
				
		if inst_list[-2:] == [0,1]:
			if self.in_bounds(self.row + 1):
				self.row += 1
			else:
				died = True
			self.path.append('D')
				
		if inst_list[-2:] == [1,0]:
			if self.in_bounds(self.col - 1):
				self.col -= 1
			else:
				died = True
			self.path.append('L')
				
		if inst_list[-2:] == [1,1]:
			if self.in_bounds(self.col + 1):
				self.col += 1
			else:
				died = True
			self.path.append('R')
				
		if 0 <= self.row < self.boundaries and 0 <= self.col < self.boundaries:
			discovered = self.wmap[self.row, self.col]
			self.onway.append(discovered)
			if discovered == 'P':
				self.treasures += 1
				self.wmap[self.row, self.col] = 0
		else:
			died = True
		return died
		
	def execute_memory_inst(self, index):
		inst = self.instructions[index]
		bin_inst = self.translate_one(inst)[2:4]
		if bin_inst == '00':
			#inkrement
			new_inst = int(inst) + 1
			if new_inst > 255:
				new_inst = 0
			self.instructions[index] = new_inst		# added modulo here
			self.executed_inst += 1
			return True
		
		if bin_inst == '01':
			#dekrement
			new_inst = int(inst) - 1
			self.instructions[index] = new_inst
			self.executed_inst += 1
			return True
		
		if bin_inst == '10':
			#jump to
			self.executed_inst += 1
			return int(bin(inst)[4:],2)
			
		if bin_inst == '11':
			#printout = move robot
			self.executed_inst += 1
			new_inst = inst
			self.complete_path += self.path
			bin_inst_to_robot = self.translate_one(self.instructions[index])[2:]
			died = self.execute_robot_inst(bin_inst_to_robot)
			self.steps += 1
			if died == True:
				return False	# goto index as False represents dead robot
		self.executed_inst += 1
		return None
	
	def program_stop(self):
		if self.steps > 500 or self.executed_inst > 500:
			return False
		return True
	
	def execute_instructions(self):		# inst = all instructions
		'''
		runs robot through memory and robot instructions
		return ('P's found, steps done on map)
		'''
		self.instructions = copy.deepcopy(self.__instructions2)
		main_index = 0
		moved = False
		self.steps = 0
		self.executed_inst = 0
		while (self.program_stop()):
			if main_index > 63:		# end of memory
				break
			goto_index = self.execute_memory_inst(main_index)
			
			if goto_index == False:
				break		#robot died
			if type(goto_index) == int:
				main_index = goto_index
			else:
				main_index += 1
		return (self.treasures, self.steps)
		
	def compute_fitness(self):
		pass
	
	
#inst_modul = Instructions()
#walleeee = Wallee(inst_modul.values)
#walleeee.execute_instructions()