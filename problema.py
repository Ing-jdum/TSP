from neo4j import GraphDatabase
import random
import math

from TSP import TSP


def get_graph_data(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))

    with driver.session() as session:
        query = """
            MATCH (a)-[r:CONNECTS_TO]->(b)
            WHERE a.name < b.name
            RETURN a.name AS start, b.name AS end, r.distance AS distance
        """
        result = session.execute_read(lambda tx: tx.run(query).data())
    return result


# Example usage
uri = "neo4j://localhost:7687"
user = "neo4j"
password = "testanddevelopment"
graph_data = get_graph_data(uri, user, password)
print(type(graph_data))
print(graph_data)

import random
import math


# Function to calculate the total distance of the route
def calculate_total_distance(route, distance_dict):
    total_distance = 0
    for i in range(len(route)):
        start = route[i]
        end = route[(i + 1) % len(route)]
        # Check if the connection exists
        if (start, end) in distance_dict:
            total_distance += distance_dict[(start, end)]
        else:
            return float('inf')  # Return a very high distance if the connection doesn't exist
    return total_distance


# Function to generate a new route by swapping two locations
def generate_new_route(current_route):
    new_route = current_route.copy()
    i, j = random.sample(range(len(new_route)), 2)
    new_route[i], new_route[j] = new_route[j], new_route[i]
    return new_route


# Simulated Annealing algorithm
def simulated_annealing(nodes, distance_dict, initial_temp, cooling_rate, min_temp):
    current_route = nodes.copy()
    current_distance = calculate_total_distance(current_route, distance_dict)
    temperature = initial_temp
    print(current_route)

    while temperature > min_temp:
        new_route = generate_new_route(current_route)
        new_distance = calculate_total_distance(new_route, distance_dict)
        print(new_route)

        if new_distance < current_distance or random.uniform(0, 1) < math.exp(
                (current_distance - new_distance) / temperature):
            current_route = new_route
            current_distance = new_distance

        temperature *= cooling_rate

    return current_route, current_distance


# Main function
def main():
    # Your input data
    data = graph_data
    # Convert data to a dictionary for easy distance lookup
    distance_dict = {(d['start'], d['end']): d['distance'] for d in data}
    for d in data:  # Add reverse directions
        distance_dict[(d['end'], d['start'])] = d['distance']

    print(distance_dict)
    # List of nodes (locations)
    nodes = ['Hub', 'Location1', 'Location2', 'Location3', 'Location4']
    print(nodes)

    # Parameters for the simulated annealing algorithm
    initial_temp = 10000
    cooling_rate = 0.995
    min_temp = 1

    # Run the algorithm
    best_route, best_distance = simulated_annealing(nodes, distance_dict, initial_temp, cooling_rate, min_temp)

    print(f"Best route: {best_route}\nTotal distance: {best_distance}")


main()
