import configparser

from neo4j import GraphDatabase
from neo4j.exceptions import Neo4jError


class GraphCreator:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        db_host = config.get('Database', 'DB_HOST')
        db_user = config.get('Database', 'DB_USER')
        db_password = config.get('Database', 'DB_PASSWORD')

        self._driver = GraphDatabase.driver(db_host, auth=(db_user, db_password))

    def close(self):
        self._driver.close()

    def create_graph(self, df):
        with self._driver.session() as session:
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

    def create_virtual_graph(self):
        with self._driver.session() as session:
            self._drop_virtual(session)
            self._create_virtual(session)

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
    def _drop_existing(session):
        try:
            query = (
                "MATCH (n) DETACH DELETE n"
            )
            session.execute_write(lambda tx: tx.run(query).data())
        except Neo4jError as e:
            print(f"Neo4j Error: {e.code} - {e.message}")

    @staticmethod
    def _create_virtual(tx):
        tx.run('''
                    CALL gds.graph.project('virtual',
                      'Location',
                      {CONNECTS_TO: {orientation:'UNDIRECTED'}});
                    ''')

    @staticmethod
    def _drop_virtual(session):
        try:
            query = '''CALL gds.graph.drop('virtual');'''
            session.execute_write(lambda tx: tx.run(query).data())
        except Neo4jError as e:
            print(f"Neo4j Error: {e.code} - {e.message}")
