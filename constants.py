queries_dict = {
    'create_virtual': '''
       CALL gds.graph.project('virtual',
          'Location',
          {CONNECTS_TO: {orientation:'UNDIRECTED'}});
   ''',

    'page_rank': '''
        CALL gds.pageRank.stream('virtual')
        YIELD nodeId, score AS pagerank
        WITH gds.util.asNode(nodeId) AS node, pagerank
        RETURN node.name AS name, toFloat(pagerank) AS pagerank
        ORDER BY pagerank DESC;
    ''',

    'degree': '''
        CALL gds.degree.stream('virtual')
        YIELD nodeId, score as degree
        WITH gds.util.asNode(nodeId) AS node, degree
        RETURN node.name AS name, degree
        ORDER BY degree DESC;
    '''

}