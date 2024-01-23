import math
import random
from interfaces import Problem


class SimulatedAnnealing:

    def __init__(self, general_functions: Problem):
        self.problem = general_functions

    # helper functions
    @staticmethod
    def __execute_with_probability(state, future_state, energy_change, temperature):
        def probability_function():
            return math.exp(energy_change / temperature)

        probability = probability_function()

        if random.uniform(0, 1) < probability:
            state = future_state
        return state

    # find solution
    def find_solution(self, initial_temperature: float, n: int, cooling_factor: float, minimum_temperature: float):
        is_solution_valid = False
        while not is_solution_valid:
            problem = self.problem
            best_solution = problem.get_current_state()
            best_fitness = 0

            def probability_function():
                return math.exp(float(energy_change) / float(temperature))

            for _ in range(n):
                same_solution = 0
                same_cost_diff = 0
                temperature = initial_temperature
                problem.update_current_state(problem.get_initial_state())
                while same_solution < 500 and same_cost_diff < 1500:
                    if temperature < minimum_temperature:
                        break
                    future_state = problem.get_random_future_state()
                    energy_change = problem.get_cost(future_state) - problem.get_cost(problem.get_current_state())
                    if energy_change > 0:
                        problem.update_current_state(future_state)
                        same_solution = 0
                        same_cost_diff = 0
                    elif energy_change == 0:
                        same_solution = 0
                        same_cost_diff += 1
                    else:
                        if random.uniform(0, 1) < probability_function():
                            problem.update_current_state(future_state)
                            same_solution = 0
                            same_cost_diff = 0
                        else:
                            same_solution += 1
                            same_cost_diff += 1
                    if problem.get_cost(problem.get_current_state()) > best_fitness:
                        best_solution = problem.get_current_state()
                        best_fitness = problem.get_cost(problem.get_current_state())
                    temperature = temperature * cooling_factor

            is_solution_valid = problem.validate_state(problem.get_current_state())
            print(best_solution, best_fitness)
        return best_solution, 1/best_fitness
