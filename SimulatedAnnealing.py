import configparser
import itertools
import math
import random

from TSP import TSP
from interfaces import Problem
from collections import defaultdict
import statistics
import time
import matplotlib.pyplot as plt

from test_solution import get_graph_data


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

    # helper functions

    def find_solution(self, minimum_temperature: float, initial_temperature: float, cooling_factor: float, n: int):
        """
        A method to run a modification of simulated annealing
        :param initial_temperature: temperature to start
        :param n: number of iterations in the for loop
        :param cooling_factor:
        :param minimum_temperature: temperature before breaking the loop
        :return: best tour found
        """

        problem = self.problem

        def simulated_annealing():
            problem.update_current_state(problem.get_initial_state())
            best_solution = problem.get_current_state()
            best_score = problem.get_cost(best_solution)
            stagnation_counter = 0
            temperature = initial_temperature
            while temperature > minimum_temperature:
                for _ in range(n):
                    if stagnation_counter >= 1500:
                        break

                    future_state = problem.get_random_future_state()
                    current_cost = problem.get_cost(problem.get_current_state())
                    future_cost = problem.get_cost(future_state)
                    energy_change = future_cost - current_cost
                    if energy_change > 0 or (
                            energy_change <= 0 and random.uniform(0, 1) < probability(energy_change, temperature)):
                        problem.update_current_state(future_state)
                        current_cost = future_cost  # Update current cost since state has changed
                        stagnation_counter = 0  # Reset stagnation counter
                    else:
                        stagnation_counter += 1  # Increment stagnation counter

                    if current_cost > best_score:
                        best_solution = problem.get_current_state()
                        best_score = current_cost

                temperature *= cooling_factor  # Cool down
            problem.update_current_state(best_solution)

        while not (problem.is_solution(problem.get_current_state())):
            problem.update_current_state(problem.get_initial_state())
            simulated_annealing()

        return problem.get_current_state(), 1/problem.get_cost(problem.get_current_state())

    def best_of_x(self, x: int, minimum_temperature: float, initial_temperature: float,
                  cooling_factor: float, n: int):
        """
        Run find_solution x times see parameters on find_solution method
        """

        best_solution, best_distance = [], float('inf')
        for _ in range(x):
            solution, distance = self.find_solution(minimum_temperature, initial_temperature, cooling_factor, n)
            if distance < best_distance:
                best_solution, best_distance = solution, distance
        return best_solution, best_distance

    def get_best_parameters(self, parameters, minimum_temperature=10, executions_per_combination=10):
        """
        :param parameters: dictionary containing the parameters and a list of values to test
        :param minimum_temperature: fixed parameter
        :param executions_per_combination: int
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
                    minimum_temperature=minimum_temperature)
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

    def plot_n_results(self, num_runs, minimum_temperature, initial_temperature, cooling_factor, n):
        """
        Runs the simulated annealing solution method multiple times and plots a histogram of the distances found.

        Parameters:
            num_runs: Number of times to run the simulation.
            initial_temperature: Initial temperature for simulated annealing.
            n: Number of iterations per single temperature in simulated annealing.
            cooling_factor: Factor by which the temperature is decreased in each iteration.
            minimum_temperature: Minimum temperature to stop the annealing process.
        """

        distances = []

        for _ in range(num_runs):
            solution, distance = self.find_solution(
                initial_temperature=initial_temperature,
                n=n,
                cooling_factor=cooling_factor,
                minimum_temperature=minimum_temperature)
            if distance == float('inf'):
                distance = -1
            distances.append(distance)

        # Plotting the histogram of distances
        plt.hist(distances, bins='auto')
        plt.title('Histograma de distancias')
        plt.xlabel('Distancia')
        plt.ylabel('Frecuencia')
        plt.show()


# Testing purposes
# config = configparser.ConfigParser()
# config.read('config.ini')
# db_host = config.get('Database', 'DB_HOST')
# db_user = config.get('Database', 'DB_USER')
# db_password = config.get('Database', 'DB_PASSWORD')
#
# graph_data = get_graph_data(db_host,
#                             db_user, db_password)
#
# tsp = TSP(graph_data, 'Hub')
# simulated_annealing = SimulatedAnnealing(tsp)
# print(simulated_annealing.best_of_x(x=40, initial_temperature=2000, n=15,
#                                     cooling_factor=0.1, minimum_temperature=0.99))
