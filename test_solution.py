from neo4j import GraphDatabase


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
