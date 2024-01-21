from neo4j import GraphDatabase


class VRPGraphCreator:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    @staticmethod
    def _create_charging_station(tx, station_name):
        tx.run("MERGE (:ChargingStation {name: $station_name})", station_name=station_name)

    def create_vrp_graph(self):
        with self.driver.session() as session:
            # Create the Hub
            session.execute_write(self._create_hub)

            # Create Locations
            locations = ['Location1', 'Location2', 'Location3', 'Location4']
            for location in locations:
                session.execute_write(self._create_location, location)

            # Create Connections
            connections = [
                ('Hub', 'Location1', 10),
                ('Hub', 'Location2', 15),
                ('Hub', 'Location3', 20),
                ('Hub', 'Location4', 25),
                ('Location1', 'Location2', 5),
                ('Location2', 'Location3', 6),
                ('Location3', 'Location4', 7),
                ('Location4', 'Location1', 8)
            ]
            for start, end, distance in connections:
                session.execute_write(self._create_connection, start, end, distance)

            # Create a Charging Station
            session.execute_write(self._create_charging_station, 'ChargingStation1')

            # Update Connections to include Charging Station
            # Assuming equal distance between locations and the charging station
            session.execute_write(self._create_connection, 'Location1', 'ChargingStation1', 4)
            session.execute_write(self._create_connection, 'ChargingStation1', 'Location4', 4)

    @staticmethod
    def _create_hub(tx):
        tx.run("MERGE (:Hub {name: 'Hub'})")

    @staticmethod
    def _create_location(tx, location_name):
        tx.run("MERGE (:Location {name: $location_name})", location_name=location_name)

    @staticmethod
    def _create_connection(tx, start, end, distance):
        query = (
            "MATCH (a {name: $start}), (b {name: $end}) "
            "MERGE (a)-[:CONNECTS_TO {distance: $distance}]-(b) "
            "MERGE (b)-[:CONNECTS_TO {distance: $distance}]->(a)"
        )
        tx.run(query, start=start, end=end, distance=distance)


# Usage
uri = "neo4j://localhost:7687"  # Replace with your URI
user = "neo4j"  # Replace with your username
password = "testanddevelopment"  # Replace with your password

vrp_graph = VRPGraphCreator(uri, user, password)
vrp_graph.create_vrp_graph()
vrp_graph.close()
