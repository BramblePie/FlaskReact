import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from descartes import PolygonPatch
from pandas.io.json import json_normalize
from SPARQLWrapper import SPARQLWrapper, JSON
from owslib.wfs import WebFeatureService
from requests import Request


# FUNCTIE VOOR HET GEBRUIKEN VAN EEN SPARQL QUERY
# --------------------------------------
def query_kadaster(sparql_query, sparql_service_url):
    sparql = SPARQLWrapper(sparql_service_url, agent="Sparql Wrapper on Jupyter example")  
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    return pd.json_normalize(result["results"]["bindings"])

    # VOORBEELD HOE DE FUNCTIE KAN WORDEN GEBRUIKT
    # sparql_query = """
    # PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    # PREFIX brt: <http://brt.basisregistraties.overheid.nl/def/top10nl#>
    # PREFIX geo: <http://www.opengis.net/ont/geosparql#>
    # SELECT  ?geo (?x as ?geoLabel) ?naam WHERE {
    #  ?x a brt:Ziekenhuis;
    #  	brt:naam ?naam;
    #     geo:hasGeometry/geo:asWKT ?geo.
    # }
    # """
    # sparql_service_url = "https://data.pdok.nl/sparql"

    # data = query_kadaster(sparql_query, sparql_service_url)



# FUNCTIE VOOR HET OPVRAGEN VAN WFS INFO
# --------------------------------------
def wfs_info(wfs_url):
    url = wfs_url
    wfs = WebFeatureService(url=url)
    print(wfs.identification.title)
    # Wfs versie
    print(wfs.version)
    # Beschikbare methodes
    # print([operation.name for operation in wfs.operation])
    # Beschikbare data lagen
    print(list(wfs.contents))
    # Print alle metadata van alle lagen
    for layer, meta in wfs.items():
        print(meta.__dict__)
    
        
# FUNCTIE VOOR HET OPVRAGEN VAN WFS DATA
# --------------------------------------
def wfs_data(wfs_url, type_param):
    url=wfs_url 
    wfs = WebFeatureService(url=url)
    # Laatste beschikbare versie pakken
    layer = list(wfs.contents)[-1]
    # Specificeren van de parameters van de data
    params = dict(service='WFS', version="1.0.0", request='GetFeature', typeName=type_param, outputFormat='json')
    q = Request('GET', url, params=params).prepare().url
    return gpd.read_file(q)

# FUNCTIE VOOR HET MAKEN KLASSES OP BASIS VAN KWARTIEL, BEDOELD VOOR KLASSE BIJ NORMALISATIE WAARDES
# --------------------------------------

def klasse(dataframe_kolom, dataframe_naam_nieuwe_kolom):
    # Klasse geven aan water_normalisatie
    water_25 = dataframe_kolom.quantile(q=.25)
    water_50 = dataframe_kolom.quantile(q=.5)
    water_75 = dataframe_kolom.quantile(q=.75)

    # Gebruik de aantallen die bij vg_data.describe() staan
    m1 = dataframe_kolom < water_25
    m2 = np.logical_and(dataframe_kolom >  water_25, dataframe_kolom < water_50)
    m3 = np.logical_and(dataframe_kolom >  water_50, dataframe_kolom < water_75)
    m4 = dataframe_kolom > water_75
    return dataframe_naam_nieuwe_kolom = np.select([m1,m2,m3,m4], ['Laag','Middel','Middel-Hoog','Hoog'], default='Geen')