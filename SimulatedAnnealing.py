import math
import random
from interfaces import Problem


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
       Attributes:
           general_functions (Problem): a class with  the implementation of the methods in the interface Problem
    """
    def __init__(self, general_functions: Problem):
        self.problem = general_functions

    # helper functions

    def find_solution(self, initial_temperature: float, n: int, cooling_factor: float, minimum_temperature: float):
        """
        A method to run a modification of simulated annealing
        :param initial_temperature: temperature to start
        :param n: number of iterations in the for loop
        :param cooling_factor:
        :param minimum_temperature: temperature before breaking the loop
        :return: best tour found
        """

        problem = self.problem
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

        try:
            distance = 1/best_score
        except ZeroDivisionError:
            distance = float('inf')

        return best_solution, distance

    def best_of_x(self, x: int, initial_temperature: float, n: int, cooling_factor: float,
                  minimum_temperature: float):
        """
        Run find_solution x times see paramaters on find_solution method
        """

        best_solution, best_distance = [], float('inf')
        for _ in range(x):
            solution, distance = self.find_solution(initial_temperature, n, cooling_factor, minimum_temperature)
            if distance < best_distance:
                best_solution, best_distance = solution, distance
        return best_solution, best_distance
