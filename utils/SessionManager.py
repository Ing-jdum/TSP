import configparser

from neo4j import GraphDatabase
import pandas as pd


class SessionManager:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        db_host = config.get('Database', 'DB_HOST')
        db_user = config.get('Database', 'DB_USER')
        db_password = config.get('Database', 'DB_PASSWORD')

        self._driver = GraphDatabase.driver(db_host, auth=(db_user, db_password))

    def _close(self):
        self._driver.close()

    def execute(self, query):
        with self._driver.session(database="neo4j") as session:
            results = session.execute_read(
                lambda tx: tx.run(query).data())
            self._close()
        return results

    def bring_data(self, query):
        results = self.execute(query)
        return pd.DataFrame(results)
