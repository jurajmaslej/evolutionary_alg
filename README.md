Evolution algorithm

versions:
runs on python 2.7, also 3.x
libraries: numpy, matplotlib

generation = gen
population = pop
probabilty = prob

Basics:
1 generation run:
	1. compute fitness of every robot
	2. get top 5% robots
	3. pass top 5% to next gen
	4. do crossovers and mutation to with top robots 
		to create additional 15%
	5. randomly create remaining 80%
	... run next generation with new pop

Population initialization:
	Robots are initialized with random memory filled up to 50th instruction

Mutation:
	with given probability to one robot,
	if probability of mutation won, we iterate over memory
	of given robot.
	with given prob. we choose to mutate it's memory instruction
		with different probabilities:
			shift right by 1 bit
			shift right by 2 bits
			create completly new value in memory cell

Crossover:
	create new robot with half memory from one parent, second half from another one
	one parent is given, second one is choosen from top 5%
	we randomize order of parents with probability

Calculation of fitness:
	idea: treasure is much more important than number of steps
	    : if same number of treasures found, it's better to take solution with less steps
	if treasures == 0:
		return int(steps/2)   ## if none of treasures were found, it's better to make more steps, so robot did not die too soon
	return treasures*100 - int(steps*1.5)	## it's much more important to find treasure

Graphs:
	filename: population size, generations, prob of mutation,
	y-axis: fitness reached
	x-axis: generations

What is being printed out?
	('gen ', 48) 	we are at generation 48, implemented functions, so that only 1/10 of gen's are printed out for readability
	('fitness ', (352, 4))	best fitness so far was 352 with 4 found treasures
	('crossovers in one previous gen ', 675)	crossovers done
	('mutated robots in one previous gen ', 3447)	crossovers + mutations
	('random new robots in one previous gen ', 3600)	randomly generated new robots

Variables:
	fitness_history: list(tuple(best fitness from every generation,
				max treasures found))
			fitness_history (352, 4) means best fitness in given generation was 352, while robot found 4 treasures

Notes to code:
	class Wallee, file worm_factory : represents virtual machine, executes memory
	class Darwin, file evolution_main : runs evolution algorithm
	robots are called wallee's in class Darwin

Style of code:
	how robots are carried into new generation:
		self.population = old generation
		self.next_gen_parents = top 5% are coppied there with fitness, than 15% of mutated and c-o are added, finally random 80% are added
		than, all next_gen_parents are mutated, except robots which has non-zero fitness there (top 5%)
		later, in run_all() self.next_gen_parents are loaded into self.population
	run_all() : most important, runs through all generations
	execution goes to mutation() (crossover()) and then is passed to execute_mutations() (execute_crossovers())

BEST RESULTS:
	we achieved best result while running population of 4000+ robots on ~100 generations, 0.8 prob of mutation,
	algorithm found 4 treasures in every run we tried so far

	with ~100 robots and ~1000 generations we found 3 treasuers reliably
	


