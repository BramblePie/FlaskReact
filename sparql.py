import pandas as pd
# from pandas.io.json import json_normalize
from SPARQLWrapper import SPARQLWrapper, JSON

def query_kadaster(sparql_query, sparql_service_url):
    sparql = SPARQLWrapper(sparql_service_url, agent="Sparql Wrapper on Jupyter example")  
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    return pd.json_normalize(result["results"]["bindings"])

sparql_query = """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX brt: <http://brt.basisregistraties.overheid.nl/def/top10nl#>
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
SELECT  ?geo (?x as ?geoLabel) ?naam WHERE {
 ?x a brt:Ziekenhuis;
 	brt:naam ?naam;
    geo:hasGeometry/geo:asWKT ?geo.
}
"""
sparql_service_url = "https://data.pdok.nl/sparql"

data = query_kadaster(sparql_query, sparql_service_url)