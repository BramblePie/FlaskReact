from owslib.wfs import WebFeatureService


def wfsinfo(url):
 wfs = WebFeatureService(url=url) 
 print(wfs.identification.title)
 print(wfs.version)
 print([operation.name for operation in wfs.operations])
 print(list(wfs.contents))
 for layer, meta in wfs.items():
     print(meta.__dict__)

# !!!!!----v00rbeeld----!!!!!!!    
# krijg info over de wfs database door deze functie uit te voeren
# info = wfsinfo("https://geodata.nationaalgeoregister.nl/asbestscholenkaart/wfs?service=WFS")
