import random

from interfaces import Problem


class TSP(Problem):
    def __init__(self, graph_data, start_node):
        self.start_node = start_node
        self.graph_data = graph_data
        self.distance_dict = self.get_distance_dict()
        self.initial_state = self.get_nodes()
        self.state = self.initial_state

    def get_nodes(self):
        locations = set()
        for start, end in self.distance_dict.keys():
            locations.add(start)
            locations.add(end)
        locations = list(locations - {self.start_node})
        return [self.start_node] + locations

    def get_distance_dict(self):
        data = self.graph_data
        distance_dict = {(d['start'], d['end']): d['distance'] for d in data}
        for d in data:  # Add reverse directions
            distance_dict[(d['end'], d['start'])] = d['distance']
        return distance_dict

    def get_random_future_state(self):
        state = self.generate_random_future_state()
        is_valid_state = self.validate_state(state)
        while not is_valid_state:
            state = self.generate_random_future_state()
            is_valid_state = self.validate_state(state)
        return state

    def generate_random_future_state(self):
        """Returns neighbor of  your solution."""
        func = random.choice([0, 1, 2, 3, 4])
        if func == 0:
            state = self.inverse()

        elif func == 1:
            state = self.insert()

        elif func == 2:
            state = self.swap()

        elif func == 3:
            state = self.shuffle()

        else:
            state = self.swap_routes()
        return state

    def shuffle(self):
        new_route = self.state[1:].copy()  # Exclude the first element
        random.shuffle(new_route)
        return [self.state[0]] + new_route  # Reinsert the first element

    def inverse(self):
        new_route = self.state.copy()
        i, j = sorted(random.sample(range(1, len(new_route)), 2))  # Start from second element
        new_route[i:j + 1] = reversed(new_route[i:j + 1])
        return new_route

    def swap(self):
        new_route = self.state.copy()
        i, j = random.sample(range(1, len(new_route)), 2)  # Start from second element
        new_route[i], new_route[j] = new_route[j], new_route[i]
        return new_route

    def insert(self):
        new_route = self.state.copy()
        random_node = random.choice(self.get_nodes())
        insert_position = random.randint(1, len(new_route))  # Start from second position
        new_route.insert(insert_position, random_node)
        return new_route

    def swap_routes(self):
        new_route = self.state.copy()
        n = len(new_route)
        i, j = sorted(random.sample(range(1, n), 2))  # Start from second element
        k, l = sorted(random.sample(range(1, n), 2))  # Start from second element

        if j < k:
            new_route = new_route[:i] + new_route[k:l + 1] + new_route[j + 1:k] + new_route[i:j + 1] + new_route[l + 1:]
        return new_route

    def validate_state(self, sequence):
        if not set(self.initial_state).issubset(set(sequence)):
            return False  # Check if all locations are visited at least once

        for i in range(len(sequence) - 1):
            if (sequence[i], sequence[i + 1]) not in self.distance_dict and (
                    sequence[i + 1], sequence[i]) not in self.distance_dict:
                return False  # Check if consecutive locations are connected

        return True

    def heuristic(self, state):
        return self.get_cost(state)

    def get_cost(self, state):
        total_distance = 0
        for i in range(len(state)):
            start = state[i]
            end = state[(i + 1) % len(state)]
            # Check if the connection exists
            if (start, end) in self.distance_dict:
                total_distance += self.distance_dict[(start, end)]
            elif (end, start) in self.distance_dict:
                total_distance += self.distance_dict[(start, end)]
            else:
                total_distance = float('inf')  # Return a very high distance if the connection doesn't exist
                break
        return 1 / total_distance

    def get_initial_state(self):
        return self.initial_state

    def get_current_state(self):
        return self.state

    def update_current_state(self, state):
        self.state = state
