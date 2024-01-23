import configparser

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


config = configparser.ConfigParser()
config.read('config.ini')
db_host = config.get('Database', 'DB_HOST')
db_user = config.get('Database', 'DB_USER')
db_password = config.get('Database', 'DB_PASSWORD')
graph_data = get_graph_data(db_host, db_user, db_password)

# Remember to change the name of the start node i forgot multiple times hahahaha
tsp = TSP(graph_data, 'l1')
simulated_annealing = SimulatedAnnealing(tsp)
print(simulated_annealing.best_of_x(x=40, initial_temperature=2000, n=15,
                                    cooling_factor=0.1, minimum_temperature=0.99))
