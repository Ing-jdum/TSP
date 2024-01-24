import random

from interfaces import Problem


class TSP(Problem):
    """
       A class to represent the Traveling Salesman Problem (TSP).
       Attributes:
           start_node (str): The starting node name for the TSP.
           graph_data (list): A list of dictionaries where each dictionary represents a connection
                              between two nodes with a specified distance.
           distance_dict (dict): A dictionary mapping pairs of nodes to the distance between them.
           initial_state (list): The initial state of the TSP, a list of nodes representing the tour.
           state (list): The current state or tour of the TSP.
    """

    def __init__(self, graph_data, start_node):
        self.start_node = start_node
        self.graph_data = graph_data
        self.distance_dict = self.get_distance_dict()
        self.initial_state = self.get_nodes()
        self.state = self.initial_state

    def get_nodes(self):
        """
        Extracts nodes from the graph data, ensuring the start node is first in the list.

        Returns:
            list: A list of nodes starting with the start node.
        """

        locations = set()
        for start, end in self.distance_dict.keys():
            locations.add(start)
            locations.add(end)
        locations = list(locations - {self.start_node})
        return [self.start_node] + locations

    def get_distance_dict(self):
        """
        Take the initial list of dicts and create a dictionary containing as key pair of nodes.
        Returns:
            dict: A dictionary with pair of nodes as key.
        """
        data = self.graph_data
        distance_dict = {(d['start'], d['end']): d['distance'] for d in data}
        for d in data:  # Add reverse directions
            distance_dict[(d['end'], d['start'])] = d['distance']
        return distance_dict

    def get_random_future_state(self):
        """
        Returns a new state performing some sort of transformation to the current state.
        The transformation is selected randomly, and it's described in generate_random_future_state
        Returns:
            list: A tour.
        """
        state = self.generate_random_future_state()

        while not self.validate_state(state):
            state = self.generate_random_future_state()
        return state

    def generate_random_future_state(self):
        """Perform a transformation to the current state
        to create a new one"""
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
        """
        change the order of the list randomly excluding first element
        :return: shuffled route
        """
        new_route = self.state[1:].copy()
        random.shuffle(new_route)
        return [self.state[0]] + new_route

    def inverse(self):
        """
        Inverse the order of the route between two indexes excluding first one
        :return: list containing a new route
        """
        new_route = self.state.copy()
        i, j = sorted(random.sample(range(1, len(new_route)), 2))
        new_route[i:j + 1] = reversed(new_route[i:j + 1])
        return new_route

    def swap(self):
        """
        Swap to elements in the list excluding first one
        :return:   new route
        """
        new_route = self.state.copy()
        i, j = random.sample(range(1, len(new_route)), 2)
        new_route[i], new_route[j] = new_route[j], new_route[i]
        return new_route

    def insert(self):
        """
        insert an element randomly in the route
        :return: new route
        """
        new_route = self.state.copy()
        random_node = random.choice(self.get_nodes())
        insert_position = random.randint(1, len(new_route))
        new_route.insert(insert_position, random_node)
        return new_route

    def swap_routes(self):
        """
        Swap two sub list from the list, excludes first element
        :return: new route
        """
        new_route = self.state.copy()
        n = len(new_route)
        i, j, k, l = sorted(random.sample(range(1, n), 4))
        new_route = new_route[:i] + new_route[k:l + 1] + new_route[j + 1:k] + new_route[i:j + 1] + new_route[l + 1:]
        return new_route

    def validate_state(self, sequence):
        """
        :param sequence: a tour
        :return: boolean
        """
        if not set(self.initial_state).issubset(set(sequence)):
            return False  # Check if all locations are visited at least once

        for i in range(len(sequence) - 1):
            if (sequence[i], sequence[i + 1]) not in self.distance_dict and (
                    sequence[i + 1], sequence[i]) not in self.distance_dict:
                return False  # Check if consecutive locations are connected

        return True

    def heuristic(self, state):
        pass

    def get_cost(self, state):
        """
        :param state: A tour
        :return: the fitness
        """
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
        """
        :return: A tour
        """
        return self.initial_state

    def get_current_state(self):
        """
        :return:  The current tour
        """
        return self.state

    def update_current_state(self, state):
        """
        Change the current state to the new state.
        :param state: A tour
        :return: None
        """
        self.state = state
