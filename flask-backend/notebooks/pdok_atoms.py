import requests
from lxml import etree, html

# RSS feed voor alle atom beschikbare datasets
res = requests.get("http://geodata.nationaalgeoregister.nl/atom/index.xml")
root = html.fromstring(res.content)

q = "Wijken en Buurten"
# Zoeken op datasets met 'q' in de titel
entries = root.xpath(f"./entry/link[contains(@title,'{q}')]/@href")

zp = []

for entry in entries:
    res = requests.get(entry)
    root = html.fromstring(res.content)
    # Request RSS feed voor specifieke dataset en zoek de download link
    zp.append(root.xpath("entry/link/@href")[0])

print(zp)
