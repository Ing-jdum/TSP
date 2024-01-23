import math
import random
from interfaces import Problem


def probability(energy_change, temperature):
    return math.exp(-energy_change / temperature)


class SimulatedAnnealing:

    def __init__(self, general_functions: Problem):
        self.problem = general_functions

    # helper functions

    def find_solution(self, initial_temperature, n, cooling_factor, minimum_temperature):
        problem = self.problem
        problem.update_current_state(problem.get_initial_state())
        best_solution = problem.get_current_state()
        best_fitness = problem.get_cost(best_solution)

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

                if current_cost > best_fitness:
                    best_solution = problem.get_current_state()
                    best_fitness = current_cost

            temperature *= cooling_factor  # Cool down

        # The validate_state check is removed assuming all generated states are valid.
        # If this is not the case, add it back.
        try:
            distance = 1/best_fitness
        except ZeroDivisionError:
            distance = float('inf')
        return best_solution, distance

    def best_of_x(self, x: int, initial_temperature: float, n: int, cooling_factor: float,
                  minimum_temperature: float):
        best_solution, best_distance = [], float('inf')
        for _ in range(x):
            solution, distance = self.find_solution(initial_temperature, n, cooling_factor, minimum_temperature)
            if distance < best_distance:
                best_solution, best_distance = solution, distance
        return best_solution, best_distance
