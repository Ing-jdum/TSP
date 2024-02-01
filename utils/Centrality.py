from constants import constants
from utils import SessionManager
import pandas as pd


def get_centrality_data():
    driver = SessionManager()
    queries = constants.queries_dict

    pagerank = driver.bring_data(queries['page_rank'])
    degree = driver.bring_data(queries['degree'])
    closeness = driver.bring_data(queries['closeness'])
    clustering = driver.bring_data(queries['clustering'])
    data = pd.merge(pagerank, degree, on='name')
    data = pd.merge(data, closeness, on='name')
    data = pd.merge(data, clustering, on='name')
    return data


def get_data():
    driver = SessionManager()
    queries = constants.queries_dict
    return driver.execute(queries['get_data'])
