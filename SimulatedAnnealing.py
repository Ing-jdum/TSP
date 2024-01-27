import configparser
import itertools
import math
import random
import pandas as pd

import constants
from TSP import TSP
from interfaces import Problem
from collections import defaultdict
import statistics
import time
import matplotlib.pyplot as plt

from test_solution import get_graph_data
from utils import SessionManager


def probability(energy_change, temperature):
    """
    :param energy_change: difference between current state cost and probable future state
    :param temperature: current temperature
    :return: a value between 1 and 0 from e^(-energy_change/temperature)
    """
    return math.exp(-energy_change / temperature)


class SimulatedAnnealing:
    """
       A class to represent the SimulatedAnnealing algorithm.
    """

    def __init__(self, general_functions: Problem):
        self.problem = general_functions

    def find_solution(self, minimum_temperature: float, initial_temperature: float,
                      cooling_factor: float, n: int, multipl: float = 2, max_stagnation: int = 500):
        """
        A method to run a modification of simulated annealing
        :param max_stagnation: the limit of stagnatino to exit
        :param multipl: a multiplier to indicate how long a solution can be.
        :param initial_temperature: temperature to start
        :param n: number of iterations in the for loop
        :param cooling_factor:
        :param minimum_temperature: temperature before breaking the loop
        :return: best tour found if none is found it call's itself recursively
        """

        # This method has a potential flaw that if not solution exists due to unconnected nodes or something like that
        # It will never stop calling itself until a Max Recursive Limit exception is thrown but i don't have much time
        # Because I'm on final exams. It's an easy fix, changing the while for a for loop with a max_retry value.

        problem = self.problem
        restart_threshold = multipl * len(problem.get_nodes())

        def simulated_annealing():
            problem.update_current_state(problem.start())

            best_solution = problem.get_current_state() # at this point this might not be a solution
            best_score = problem.get_cost(best_solution)
            stagnation_counter = 0
            temperature = initial_temperature
            while temperature > minimum_temperature:
                for _ in range(n): # This to follow the algorithm discussed during  class
                    # if stagnation counter reached the limit, break the loop
                    if stagnation_counter >= max_stagnation:
                        break
                    # Calculate energy change based on possible future state
                    future_state = problem.get_random_future_state()
                    current_cost = problem.get_cost(problem.get_current_state())
                    future_cost = problem.get_cost(future_state)
                    energy_change = future_cost - current_cost
                    # execute with probability or it's a closer state to a solution based on the cost
                    if energy_change > 0 or (
                            energy_change <= 0 and random.uniform(0, 1) < probability(energy_change, temperature)):
                        problem.update_current_state(future_state)
                        current_cost = future_cost  # Update current cost since state has changed
                        stagnation_counter = 0  # Reset stagnation counter
                    else:
                        stagnation_counter += 1  # Increment stagnation counter

                    # first variation, don't let the list of the tour grow infinitely,
                    # it will grow until restart_threshold
                    if len(problem.get_current_state()) > restart_threshold:
                        problem.update_current_state(problem.start())
                    # if a solution if found, go and see if it's better than the current you have stored
                    # Even tho we are looking for a solution and not necessarily optimizing, we want a good solution.
                    if problem.is_solution(problem.get_current_state()) and current_cost > best_score:
                        best_solution = problem.get_current_state()
                        best_score = current_cost
                temperature *= cooling_factor  # Cool down
            problem.update_current_state(best_solution)

            while not (problem.is_solution(problem.get_current_state())):
                simulated_annealing()

        simulated_annealing()

        return problem.get_current_state(), 1 / problem.get_cost(problem.get_current_state())

    def best_of_x(self, x: int, minimum_temperature: float, initial_temperature: float,
                  cooling_factor: float, n: int, multipl: float = 2):
        """
        Run find_solution x times see parameters on find_solution method
        """

        best_solution, best_distance = [], float('inf')
        for _ in range(x):
            solution, distance = self.find_solution(minimum_temperature, initial_temperature, cooling_factor, n, multipl=multipl)
            if distance < best_distance:
                best_solution, best_distance = solution, distance
        return best_solution, best_distance

    def get_best_parameters(self, parameters, minimum_temperature=10, executions_per_combination=10, multipl: int = 2):
        """
        A function to search between different values of parameters of the simulated annealing algorithm,
        All other parameters explained on find_solution.
        :param multipl:
        :param executions_per_combination:
        :param minimum_temperature:
        :param parameters: dictionary containing the parameters and a list of values to test
        :return: dictionary with the results sorted by distance and then time
        """
        # Dictionary to hold aggregated results for each parameter combination
        aggregated_results = defaultdict(list)

        for initial_temperature, cooling_factor, n in itertools.product(
                parameters['initial_temperature'], parameters['cooling_factor'], parameters['n']):

            # Execute each parameter combination multiple times
            for _ in range(executions_per_combination):
                start_time = time.time()
                solution, distance = self.find_solution(
                    initial_temperature=initial_temperature,
                    n=n,
                    cooling_factor=cooling_factor,
                    minimum_temperature=minimum_temperature,
                    multipl=multipl)
                end_time = time.time()
                time_elapsed = end_time - start_time

                # Aggregate results
                aggregated_results[(initial_temperature, cooling_factor, n)].append((distance, time_elapsed))

        # Process the results to find the mode of distance and minimum time for each parameter set
        best_results = []
        for params, results in aggregated_results.items():
            distances = [result[0] for result in results]
            mode_distance = statistics.mode(distances)
            min_time = min([elapsed_time for dist, elapsed_time in results if dist == mode_distance])

            best_results.append((params, mode_distance, min_time))

        # Sort the results by distance first and then by time
        best_results.sort(key=lambda x: (x[1], x[2]))

        return best_results

    def plot_n_results(self, num_runs, minimum_temperature, initial_temperature, cooling_factor, n, multipl: float = 2):
        """
        Runs the simulated annealing solution method multiple times and plots a histogram of the distances found.
        Parameters:
            Explained on find_solution
        """

        distances = []

        for _ in range(num_runs):
            solution, distance = self.find_solution(
                initial_temperature=initial_temperature,
                n=n,
                cooling_factor=cooling_factor,
                minimum_temperature=minimum_temperature,
                multipl=multipl)
            if distance == float('inf'):
                distance = -1
            distances.append(distance)

        # Plotting the histogram of distances
        plt.hist(distances, bins='auto')
        plt.title('Histograma de distancias')
        plt.xlabel('Distancia')
        plt.ylabel('Frecuencia')
        plt.show()



# # Testing purposes
# config = configparser.ConfigParser()
# config.read('config.ini')
# db_host = config.get('Database', 'DB_HOST')
# db_user = config.get('Database', 'DB_USER')
# db_password = config.get('Database', 'DB_PASSWORD')
#
# graph_data = get_graph_data(db_host,
#                             db_user, db_password)
#
# driver = SessionManager()
# queries = constants.queries_dict
# try:
#     driver.execute(queries['drop_virtual'])
#     driver.execute(queries['create_virtual'])
# except:
#     print("Subgrafo ya existe")
#

#
# print(data)
# tsp = TSP(graph_data, 'l1', data)
#
# simulated_annealing = SimulatedAnnealing(tsp)
# print(simulated_annealing.best_of_x(x=10, initial_temperature=500, n=15,
#                                     cooling_factor=0.5, minimum_temperature=5, multipl=1.5))
