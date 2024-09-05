#Import pywake and relevant modules
import py_wake
from py_wake.site import UniformWeibullSite, UniformSite
from py_wake.examples.data.iea37 import IEA37_WindTurbines
from py_wake import NOJ

#Import numpy
import numpy

#Import algorithms for optimisation
import pygad

def setup_site():
    """ Place parameters here for site specifics """
    wind_turbines = IEA37_WindTurbines()
    site = UniformWeibullSite(p_wd = [1], a = [9.8], k = [2], ti = 0.1)
    #Noj is our deficit model. We load it with the site and turbine type
    noj = NOJ(site,wind_turbines)
    return noj
    
def setup_constant_ws_site():
    wind_turbines = IEA37_WindTurbines()
    site = UniformSite(ws = 9.8)
    noj = NOJ(site,wind_turbines)
    return noj
    
def divide_range(start, end, precision):
    point_list = []
    step = (end - start)/precision
    for i in range(precision):
        point_list.append(start + (step * i))
    return point_list
  
def create_grid_ranges(x_start, x_end, y_start, y_end, precision):
    grid_ranges = []
    x_list = divide_range(x_start, x_end, precision)
    y_list = divide_range(y_start, y_end, precision)
    for y_val in y_list:
        for x_val in x_list:
            grid_ranges.append([y_val, x_val])
    return grid_ranges
   
def get_turbine_locations(input_list, grid):
    x_positions = []
    y_positions = []
    for index in input_list:
        y_positions.append(grid[index][0])
        x_positions.append(grid[index][1])
    return x_positions, y_positions
                      
def run_test(seed = None, generations = 50, population = 50, turbines = 16, x_start = 0, x_end = 1000, y_start = 0, y_end = 1000, precision = 1000, mutation_ratio = 0.1, keep_parents_ratio = 0.9, crossover_type = "two_points", constant_ws = False):
    fitness_dict = {} #Create a dictionary for the storing of fitness values
    for i in range(1, generations+1):
        fitness_dict[i] = [] #Create an empty list for each generation
    
    if constant_ws:
        SITE_CONFIG = setup_constant_ws_site()
    else:
        SITE_CONFIG = setup_site()
    SITE_POSITIONS = create_grid_ranges(x_start, x_end, y_start, y_end, precision)
    
    def ga_function(solution, index_in_pop):
        position_lists = get_turbine_locations(solution, SITE_POSITIONS)
        result = SITE_CONFIG(position_lists[0], position_lists[1])
        return float(result.aep().sum())
        
    def generation_fitness(ga_instance): #For each run of a generation
        fitness_dict[ga_instance.generations_completed].append(ga_instance.best_solution()[1]) #Add the fitness of the generation to the dictionary
    
    ga_instance = pygad.GA(num_generations=generations, #Number of generations to run for
                           num_parents_mating=int(population*keep_parents_ratio),
                           fitness_func=ga_function,
                           on_generation=generation_fitness,
                           sol_per_pop=population, #The number of solutions within the population
                           num_genes=turbines, #Number of turbines, for pygad, this is the num_genes parameter
                           init_range_low=0, #The start of the list of positions
                           init_range_high=(len(SITE_POSITIONS) - 1), #The end of the list of positions
                           parent_selection_type="sss", #Steady state selection
                           keep_parents=int(population*keep_parents_ratio), #Number of parents to keep.
                           crossover_type=crossover_type, #Two points are crossed over, as particular layouts of turbines may be beneficial
                           mutation_type="random", #Mutation type
                           mutation_probability=mutation_ratio, #Mutation percentage
                           gene_type=int,
                           allow_duplicate_genes=False, #Prevent duplicates as this would mean turbines in the same position
                           random_seed=seed)
    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    return (solution, solution_fitness, fitness_dict)