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

    def __init__(self, graph_data, start_node, centrality_df):
        self.start_node = start_node
        self.graph_data = graph_data
        self.distance_dict = self.get_distance_dict()
        self.nodes = self.get_nodes()
        self.initial_state = self.start()
        self.state = self.initial_state
        self.centrality_df = centrality_df
        self.memory = set()

    def start(self):
        """
        Extracts nodes from the graph data, ensuring the start node is first in the list.

        Returns:
            list: A list that is valid of nodes starting with the start node.
        """

        # Extract all unique nodes
        nodes = self.get_nodes()

        # Choose a start node
        current_node = self.start_node
        path = []
        visited = {current_node}

        while True:
            # Filter connections that start from the current node and lead to unvisited nodes
            possible_moves = [conn for conn in self.graph_data if
                              conn['start'] == current_node and conn['end'] not in visited]

            if len(path) > 0.5 * len(self.get_nodes()):
                break  # Break if there are no unvisited nodes to move to

            # Choose a random connection from the possible moves
            next_move = random.choice(possible_moves)

            # Update the current node, path, and visited nodes
            current_node = next_move['end']
            visited.add(current_node)
        return path

    def get_nodes(self):
        """
        Extracts nodes from the graph data, ensuring the start node is first in the list.

        Returns:
            list: A list of nodes starting with the start node.
        """
        locations = set([conn['start'] for conn in self.graph_data] + [conn['end'] for conn in self.graph_data])
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

    def get_available_moves(self):
        """
        Returns the nodes that the last node in the tour is connected to, based on the connections' dictionary.
        :return: A list of node names that are directly connected to the last node in the tour.
        """

        tour = self.state.copy()
        if not tour:  # If the tour is empty, return an empty list
            return []

        last_node = tour[-1]  # Get the last node in the tour

        # Find all nodes that are connected to the last node
        # This includes checking both directions since the graph may be undirected or have bidirectional edges
        available_moves = []

        for (start_node, end_node), _ in self.distance_dict.items():
            if start_node == last_node and end_node and end_node not in available_moves:
                available_moves.append(end_node)
            elif end_node == last_node and start_node and start_node not in available_moves:
                available_moves.append(start_node)
        print(f"tour : {tour[-1]}, memory {self.memory}, moves: {available_moves}")

        return available_moves

    def get_random_future_state(self):
        """
        Returns a new state performing some sort of transformation to the current state.
        The transformation is selected randomly, and it's described in generate_random_future_state
        Returns:
            list: A tour.
        """
        available_moves = self.get_available_moves()
        state = self.generate_random_future_state(available_moves)

        while not self.validate_state(state):
            state = self.generate_random_future_state(available_moves)
        return state

    def generate_random_future_state(self, available_moves):
        """Perform a transformation to the current state
        to create a new one"""
        func = random.choice([0, 1])
        if func == 0:
            state = self.transition_to_highest_centrality(available_moves, 'pagerank')
        else:
            state = self.transition_to_highest_centrality(available_moves, 'degree')
        return state

    def find_highest_centrality_node(self, available_nodes, centrality_key):
        """
        Find the node with the highest centrality from a list of available nodes.

        :param available_nodes: A list of node names to consider.
        :param centrality_key: The centrality score to use (e.g., 'pagerank', 'degree').
        :return: The name of the node with the highest centrality score.
        """

        # Filter the DataFrame to only include available nodes and not in memory
        filtered_df = self.centrality_df[self.centrality_df['name']
                                         .isin(available_nodes) & ~self.centrality_df['name'].isin(self.memory)]

        if filtered_df.empty:
            return None

        # Find the row with the maximum centrality score for the given key
        highest_centrality_row = filtered_df.loc[filtered_df[centrality_key].idxmax()]

        # Return the name of the node with the highest centrality score
        return highest_centrality_row['name']

    def update_memory(self, node, memory_size=2):
        """
        Update the short-term memory with the newly visited node, ensuring it does not exceed the specified memory size.

        :param node: The newly visited node to add to the memory.
        :param memory_size: The maximum size of the memory.
        """
        self.memory.add(node)
        # Ensure the memory does not exceed the specified size by removing the oldest entry
        if len(self.memory) > memory_size:
            self.memory.pop()

    def transition_to_highest_centrality(self, available_moves, key):
        """
        Transition to the highest centrality node from available moves, avoiding immediate loops by using memory,
        and appending it to the route.

        :param key: the centrality measure to use
        :param available_moves: A list of available nodes to move to.
        :return new_state: a tour with a new node in it
        """
        current_state = self.state.copy()
        if not available_moves or len(current_state) == 0:
            return current_state

        current_node = current_state[-1]  # The current node is the last one in the route

        # Filter out the current node from available moves
        available_moves = [node for node in available_moves if node != current_node]

        if not available_moves:
            return current_state

        # Find the available node with the highest centrality, excluding the current node and those in memory
        highest_centrality_node = self.find_highest_centrality_node(available_moves, centrality_key=key)
        if highest_centrality_node:
            # Update memory with the newly visited node
            self.update_memory(highest_centrality_node)
            # Append the highest centrality node to the route
            current_state.append(highest_centrality_node)
            return current_state
        return current_state

    def validate_state(self, sequence):
        """
        :param sequence: a tour
        :return: boolean
        """
        for i in range(len(sequence) - 1):
            if ((sequence[i], sequence[i + 1]) not in self.distance_dict
                    and (sequence[i + 1], sequence[i]) not in self.distance_dict):
                return False  # Check if consecutive locations are connected

        return True

    def is_solution(self, sequence):
        if not set(self.nodes).issubset(set(sequence)):
            return False  # Check if all locations are visited at least once
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
                total_distance = float('inf')
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
