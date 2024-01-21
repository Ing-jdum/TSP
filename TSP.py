import random

from interfaces import Problem


class TSP(Problem):
    def __init__(self, graph_data):
        self.graph_data = graph_data
        self.distance_dict = self.get_distance_dict()
        self.initial_state = self.get_nodes()
        self.state = self.initial_state

    def get_nodes(self):
        locations = set()
        for start, end in self.distance_dict.keys():
            locations.add(start)
            locations.add(end)
        return list(locations)

    def get_distance_dict(self):
        data = self.graph_data
        distance_dict = {(d['start'], d['end']): d['distance'] for d in data}
        for d in data:  # Add reverse directions
            distance_dict[(d['end'], d['start'])] = d['distance']
        return distance_dict

    def get_random_future_state(self):
        state = self.generate_random_future_state()
        is_state_valid = self.validate_state(state)
        while not is_state_valid:
            state = self.generate_random_future_state()
            is_state_valid = self.validate_state(state)
        return state

    def generate_random_future_state(self):
        new_route = self.state.copy()
        random.shuffle(new_route)
        i, j = random.sample(range(len(new_route)), 2)
        new_route[i], new_route[j] = new_route[j], new_route[i]
        return new_route

    def validate_state(self, sequence):
        for i in range(len(sequence) - 1):
            if not (sequence[i], sequence[i + 1]) in self.distance_dict and not (sequence[i + 1],
                                                                                 sequence[i]) in self.distance_dict:
                return False
        return True

    def heuristic(self, state):
        return self.get_cost(state) / 2

    def get_cost(self, state):
        total_distance = 0
        for i in range(len(state)):
            start = state[i]
            end = state[(i + 1) % len(state)]
            # Check if the connection exists
            if (start, end) in self.distance_dict:
                total_distance += self.distance_dict[(start, end)]
            else:
                return float('inf')  # Return a very high distance if the connection doesn't exist
        return total_distance

    def get_initial_state(self):
        return self.initial_state

    def get_current_state(self):
        return self.state

    def update_current_state(self, state):
        self.state = state
