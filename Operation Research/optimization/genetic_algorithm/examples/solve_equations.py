import random
import math
import numpy as np

def fittness_equations(params, variables):
    '''
    the fitness value from the linear equation
    '''
    actual_sum = 0
    for i in range(len(variables)):
        actual_sum += params[i] * variables[i]

    error   = abs(params[-1] - actual_sum)
    fittness= error
    return fittness

def selection(population,  generation, chromosome_weights, n_survive):
    '''
    Selection criteria
    '''
    fit_chromosomes= []
    fitnessscore   = []
    for chromosome in population:
        individual_fitness = fittness_equations(params=chromosome_weights, variables=chromosome)
        fitnessscore.append(individual_fitness)

    total_fitness=sum(fitnessscore)
    print('fitness loss: ', total_fitness)

    score_card = list(zip(fitnessscore,population))
    score_card.sort()

    for individual in score_card:
        if individual[0]==0:
            if individual[1] not in fit_chromosomes:
                # Check that chromosome is unique
                fit_chromosomes.append(individual[1])

    score_card = score_card[:n_survive]
    score, population=zip(*score_card)

    return list(population), fit_chromosomes

def crossover(population, n_bits):
    '''
    Crossover between chromosomes
    '''
    n_pop       = len(population)
    n_crossover = n_pop//2        # Number of pair to crossover

    random.shuffle(population)    
    fatherchromosome = population[:n_crossover]
    motherchromosome = population[n_crossover:]

    children=[]
    for i in range(len(fatherchromosome)):
        crossoversite   = random.randint(0,n_bits)
        fatherfragments = [fatherchromosome[i][:crossoversite], fatherchromosome[i][crossoversite:]]
        motherfragments = [motherchromosome[i][:crossoversite], motherchromosome[i][crossoversite:]]

        firstchild      = fatherfragments[0]+motherfragments[1]
        secondchild     = motherfragments[0]+fatherfragments[1]
        children.append(firstchild)
        children.append(secondchild)

    return children

def mutation(population, n_bits, p_mutation, min_val, max_val):
    '''
    Mutation through chromos
    '''
    mutatedchromosomes=[]
    for chromosome in population:
        if random.random() > p_mutation:
            mutation_site=random.randint(0,n_bits-1)
            chromosome[mutation_site]=random.randint(min_val, max_val )
            mutatedchromosomes.append(chromosome)

    return mutatedchromosomes

def get_fit_chromosomes(chromosome_weights, generations, n_bits, n_pop, n_survive, p_mutation, min_val=1, max_val=9):

    # Initialize population
    population=[[random.randint(min_val, max_val) for i in range(n_bits)] for j in range(n_pop)]

    fitted_chromosomes=[]
    for generation in range(generations):
        generation+=1
        print(f'(gen:{generation:3})', end=' ')

        # select fittest chromosomes
        population, fit_chromosomes = selection(population,  generation, chromosome_weights, n_survive=n_survive)
        for chromo in fit_chromosomes:
            if chromo not in fitted_chromosomes:
                # Check that chromo is unique through all generation
                fitted_chromosomes.append(chromo.copy())
                #use copy for change id of chromo (beacuse it will change by garbage collection through mutation)


        # Crossover through parents
        crossover_children = crossover(population, n_bits)
        population=population+crossover_children

        # Mutation through parents
        mutated_population=mutation(population, n_bits,  p_mutation, min_val=1, max_val=9)
        population=population+mutated_population



    return fitted_chromosomes


def genetic_equation_solver(generation, params, n_survive, p_mutation=0.1, min_num=1, max_num=9):
    params      = params
    n_coeff     = len(params)-1
    n_soln      = len(params)-1
    n_survive   = n_survive
    p_mutation  = p_mutation
    solution    = get_fit_chromosomes(params, generations, n_coeff, n_soln, n_survive, p_mutation, min_val=min_num, max_val=max_num)
    return solution

def display_outputs(params, solutions):
    n_soln = len(solutions)
    print('\n-----------Solution-----------')
    print(f'Number of solutions: {n_soln}')
    print(f'Fitted  Solutions  :')
    for soln in solutions:
        experssion = '\t'
        for i in range(len(soln)):
            if i != 0:
                experssion+=' + ' 
            experssion += f'{params[i]} * ({soln[i]})'
        experssion += f' = {params[-1]}'
        print(experssion)
    


# params is coefficients of equation (c0,c1,c2,...,cn): c0 * x0 + c1 * x1 + c2 * x2 + ... + cn-1 * xn-1 = cn
params      = [10,2,1,2,0,21,100]               
min_num     = 0      # min value of (xi)
max_num     = 29     # max value of (xi)

# Genetic Algorithm parameterss
generations = 50       # Maximum number of generations
n_survive   = 4        # Number of survive from selection step
p_mutation  = 0.1      # Probability of mutation happen

solution = genetic_equation_solver(generation=generations, params=params, n_survive=n_survive, p_mutation=p_mutation, min_num=min_num, max_num=max_num)
display_outputs(params=params, solutions=solution)
