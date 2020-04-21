#export data uit wfs van pdok/kadaster

import geopandas as gpd
from requests import Request
from owslib.wfs import WebFeatureService
def wfs_kadaster(url,type_param):
 wfs = WebFeatureService(url=url)
 layer = list(wfs.contents)[-1]
 params = dict(service='WFS', request='GetFeature',typeName=type_param ,StartIndex='0', outputFormat='json')
 q = Request('GET', url, params=params).prepare().url
 return gpd.read_file(q)


#!!!!!---v00rbeeld----!!!!
#voor url voor wfs dataprovider in en het type van de data die je wil kijk hier onder
# data = wfs_kadaster("https://geodata.nationaalgeoregister.nl/asbestscholenkaart/wfs","asbestscholenkaart:asbestscholenkaart")