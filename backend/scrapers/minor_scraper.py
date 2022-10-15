from typing import Dict, List, Tuple
import requests
from lxml import html
import json

# The api key is public so it does not need to be hidden in a .env file
BASE_URL = "http://rpi.apis.acalog.com/v1/"
# It is ok to publish this key because I found it online already public
DEFAULT_QUERY_PARAMS = "?key=3eef8a28f26fb2bcc514e6f1938929a1f9317628&format=xml"
CHUNK_SIZE = 500

# returns the list of catalogs with the newest one being first
# each catalog is a tuple (year, catalog_id) ex: ('2020-2021', 21)
def get_catalogs() -> List[Tuple[str, int]]:
    catalogs_xml = html.fromstring(
        requests.get(
            f"{BASE_URL}content{DEFAULT_QUERY_PARAMS}&method=getCatalogs"
        ).text.encode("utf8")
    )
    catalogs = catalogs_xml.xpath("//catalogs/catalog")

    ret: List[Tuple[str, int]] = []
    # For each catalog get its year and id and add that as as tuples to ret
    for catalog in catalogs:
        catalog_id: int = catalog.xpath("@id")[0].split("acalog-catalog-")[1]
        catalog_year: str = catalog.xpath(".//title/text()")[0].split(
            "Rensselaer Catalog "
        )[1]
        ret.append((catalog_year, catalog_id))

    # sort so that the newest catalog is always first
    ret.sort(key=lambda tup: tup[0], reverse=True)
    return ret

# Returns a list of course ids for a given catalog
def get_minor_ids(catalog_id: str) -> List[str]:
    programs_xml = html.fromstring(
        requests.get(
            f"{BASE_URL}search/programs{DEFAULT_QUERY_PARAMS}&method=listing&options[limit]=0&catalog={catalog_id}"
        ).text.encode("utf8")
    )
    return programs_xml.xpath('//result[type="Minor"]/id/text()')


