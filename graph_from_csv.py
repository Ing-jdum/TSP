from neo4j import GraphDatabase


class GraphCreator:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_graph(self, df):
        with self.driver.session() as session:
            self._drop_existing(session)
            # Create nodes
            for location in df.columns[1:]:
                session.execute_write(self._create_node, location)

            # Create relationships with distances, skip diagonal entries
            for i, row in df.iterrows():
                for j, value in enumerate(row[1:]):
                    # Skip diagonal and -1 values
                    if i != j and value != -1:
                        session.execute_write(self._create_relationship, row[0], df.columns[j + 1], value)

    @staticmethod
    def _create_node(tx, location):
        query = (
            "MERGE (l:Location {name: $location}) "
            "RETURN l"
        )
        tx.run(query, location=location)

    @staticmethod
    def _create_relationship(tx, from_location, to_location, distance):
        query = (
            "MATCH (l1:Location {name: $from_location}), "
            "(l2:Location {name: $to_location}) "
            "MERGE (l1)-[r:CONNECTS_TO {distance: $distance}]->(l2) "
            "RETURN r"
        )
        tx.run(query, from_location=from_location, to_location=to_location, distance=distance)

    @staticmethod
    def _drop_existing(tx):
        query = (
            "MATCH (n) DETACH DELETE n"
        )
        tx.run(query)

