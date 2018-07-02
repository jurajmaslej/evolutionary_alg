from __future__ import division
from data_loader import Loader
from worm_instructs import Instructions
from worm_factory import Wallee
import numpy as np
import random
import copy
import matplotlib.pyplot as plt

class Darwin:
	
	def __init__(self, pop_size, gen_count, prob_mutation):
		''' 
		wallee = robot
		Population as dict walee:fitness of Wallee
		use top 5% as elit robots, do not mutate them
		15 % crossovers and mutation of top 5%
		80 % random new robots
		'''
		self.population = dict()
		for i in range(0, pop_size):
			inst_modul = Instructions()		#random init of first Instructions for every robot
			self.population[Wallee(inst_modul.values)] = 0	# init fitness is zero
		self.prob_mutation = prob_mutation
		self.top5percent = int((pop_size / 100) * 5)
		self.fitness_history = [(0,0)]
		self.mutated = 0
		self.num_crossovers = 0
		self.num_random = 0
		#self.run_one_generation()
		self.run_all(gen_count)		
		
	def run_all(self, gen_count):
		'''
		runs for gen_count generations
		prints fitness, gen number, population stats
		'''
		for gen in range(0, gen_count):
			if gen % (gen_count / 10) == 0:
				print ('gen ', gen)
				print('fitness ', self.fitness_history[-1])
				print('crossovers in one previous gen ', self.num_crossovers) 
				print('mutated robots in one previous gen ', self.mutated)
				print('random new robots in one previous gen ', self.num_random)
			self.mutated = 0
			self.num_crossovers = 0
			self.num_random = 0
			self.next_gen_parents = dict()
			self.next_gen_population = dict()	#mutations and c-o here
			self.run_one_generation()
			self.selection_parents()
			self.crossovers()
			self.mutations()
			self.population = copy.deepcopy(self.next_gen_population)	#new becomes old
		#self.printout_fness()
		return self.fitness_history[-1]
	
	def printout_fness(self):
		for i in range(0, len(self.fitness_history)):
			if i % (len(self.fitness_history) /10)  == 0:
				print (self.fitness_history[i])
		print('last fitness ', self.fitness_history[-1])
	
	def compute_fitness(self, treasures, steps):
		'''
		finding treasure is much more important then lot of steps, even so, 
		less steps => better solution
		
		if no treasure found, do opposite aproach, more steps are better, 
		robot does not kill himself so fast, so he has chance to mutate into something better
		'''
		if treasures == 0:
			return int(steps/2)		# if none of treasures were found, it's better to make more steps
		return treasures*100 - int(steps*1.5)
	
	def run_one_generation(self):
		'''
		runs one generation
		compute_fitness for whole population
		append best value to fitness_history to store
		'''
		for key, value in self.population.iteritems():
			treasures, steps = key.execute_instructions()
			fitness = self.compute_fitness(treasures, steps)
			self.population[key] = fitness

		best_wallee = max(self.population, key=self.population.get)
		fitnesses = max(list(self.population.values()))
		self.fitness_history.append((fitnesses, best_wallee.treasures))
		
	def selection_parents(self, elitarism = True):
		'''
		5% of population stays
		15% mutation, c-o's of best from old population
		80% new random robots
		'''
		sorted_old_pop = sorted(self.population.items(), key=lambda x:x[1], reverse = True)
		added = 0
		if elitarism:
			while added <= self.top5percent:		#treasure was found, goto next gen, 1/4 should be defined as class variable
				if sorted_old_pop[added][0].name is None:
					sorted_old_pop[added][0].name = random.random()		#add name to robot for debug reasons
				self.next_gen_parents[sorted_old_pop[added][0]] = sorted_old_pop[added][1]
				added += 1
	
	def execute_mutation(self, wallee):
		for i in range(0,64):
			random_prob = random.random()
			if random_prob < self.prob_mutation:
				random_prob = random.random()
				if random_prob <= 0.5:
					wallee.instructions[i] = wallee.instructions[i] >> 1		#shift right by 1 bits, returns int
				elif 0.5 < random_prob < 0.9:
					wallee.instructions[i] = wallee.instructions[i] >> 3
				else:
					wallee.instructions[i] = np.random.randint(0,255)
			# else: instruction not mutated
		return wallee
	
	def mutations(self):	#self.prob = probability of mutation
		'''
		do mutation with given probability
		does not mutate top 5%
		'''
		for wallee, fness in self.next_gen_parents.iteritems():
			new_wallee = copy.deepcopy(wallee)
			new_wallee.path = []
			new_wallee.onway = []
			new_wallee.steps = 0
			new_wallee.treasures = 0
			new_wallee.restore_robot()
			if fness != 0: # do not mutate best ones from old pop
				self.next_gen_population[new_wallee] = 0
			else:
				random_prob = random.random()
				if random_prob < self.prob_mutation:
					self.mutated += 1
					mutated_wallee = self.execute_mutation(new_wallee)
					self.next_gen_population[mutated_wallee] = 0
				else:
					self.next_gen_population[new_wallee] = 0
	
	def execute_co(self, index, wallees_parents):	#randomly choose mating partner, create new wallee
		he = wallees_parents[int(index/3)]
		she = wallees_parents[np.random.randint(0,len(wallees_parents))]
		
		#do actual c-o's with wallees memories
		inst_len = len(he.instructions)
		
		# instructions are np arrays
		rand_prob = random.random()
		if rand_prob > 0.5:
			# first half and last half
			new_walle_instructions = np.hstack((he.instructions[:int(inst_len / 2)],she.instructions[int(inst_len / 2):]))
		else:
			# first half and first half
			new_walle_instructions = np.hstack((he.instructions[:int(inst_len / 2)],she.instructions[:int(inst_len / 2)]))
		
		return Wallee(new_walle_instructions)
	
	def crossovers(self):
		'''
		5% best ones from previous
		15% best ones with crossovers and mutation
		80% random
		+ another random if numbers not right
		
		# update 
		# elitarism only for top 5 %
		'''
		
		wallees_parents = sorted(self.next_gen_parents, key=self.next_gen_parents.get)
		for i in range(0, self.top5percent*3):		#do another 15%
			new_wallee = self.execute_co(i, wallees_parents)
			self.next_gen_parents[new_wallee] = 0
			self.num_crossovers += 1
			
		for i in range(0, self.top5percent * 16):	#do rest 80%, 16 + 3 + 1 = 20, 20*5=100%
			add_inst = Instructions()	#randomly generated
			additional_wallee = Wallee(add_inst.values)
			self.next_gen_parents[additional_wallee] = 0
			self.num_random += 1
				
		if len(self.next_gen_parents) != len(self.population):
			add_inst = Instructions()	#randomly generated
			additional_wallee = Wallee(add_inst.values)
			self.next_gen_parents[additional_wallee] = 0
			
			
def run_multiple_times(pop_size, generations, prob_mutation, runtimes):
	'''
	pop_size = int, size of population
	generations = int, num of generations
	prob_mutation = 0 < float < 1, probability of mutation
	runtimes = to get stable results, we run algorithm multiple times, 
	later, mean and average of results is produced
	'''
	fnes = []
	treasures = []
	filename = 'outputs_final_pop' + str(pop_size) + '_gen' + str(generations) + '_mutprob' + str(prob_mutation) + '.txt'
	output_file= open(filename, 'w')
	output_file.write('Model robots:' + str(pop_size) + ' generations:' + str(generations) +  ' mut prob:' + str(prob_mutation))
	for i in range(0,runtimes):
		robot_kind = Darwin(pop_size, generations, prob_mutation)
		fnes.append(robot_kind.fitness_history[-1][0])
		treasures.append(robot_kind.fitness_history[-1][1])
		print('new run of model ', i, ' best fitness ', fnes[-1])
		output_file.write('run ' + str(i) + ' best fitness: ' + str(fnes[-1]) + ' treasures: ' + str(treasures[-1]) +  '\n')
	
	output_file.write('median of treasures ' + str(np.median(treasures)) +'\n')
	output_file.write('median of fitness ' + str(np.median(fnes)) +'\n')
	output_file.write('mean of treasures ' + str(np.mean(treasures)) +'\n')
	output_file.write('mean of fitness ' + str(np.mean(fnes)) +'\n')
	output_file.close()

	print('median of treasures ', np.median(treasures))
	print('median of fnes ', np.median(fnes))

def run_one_time(pop_size, generations, prob_mutation, plot_graph):
	robot_kind = Darwin(pop_size, generations, prob_mutation)
	if plot_graph:
		fness = [a[0] for a in robot_kind.fitness_history]
		a =  [i for i in range(0, len(robot_kind.fitness_history))]
		plt.plot(a, fness, '-')
		plt.xlabel('generation')
		plt.ylabel('fitness')
		graph_name = 'fitness__pop' + str(pop_size) + '_gen' + str(generations) + '_mutprob' + str(prob_mutation) + '.png'
		plt.savefig(graph_name)
		plt.close()

def run_choosen_models():
	run_one_time(10, 100, 0.8, True)
	run_one_time(40, 1000, 0.8, True)
	run_one_time(4500, 80, 0.8, True)
	
run_choosen_models()
#run_multiple_times(100, 800, 0.2)		# takes a ....lot of time, like 1.5 hours, would suggest to have a look in already produced files
