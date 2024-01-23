from neo4j import GraphDatabase

from SimulatedAnnealing import SimulatedAnnealing
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

tsp = TSP(graph_data, 'l4')
simulated_annealing = SimulatedAnnealing(tsp)
print(simulated_annealing.find_solution(initial_temperature=3000, n=20,
                                        cooling_factor=0.1, minimum_temperature=0.9))
