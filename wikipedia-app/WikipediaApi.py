from typing import List
from flask import jsonify, Response
import requests
import re

BASE_URL = "https://en.wikipedia.org/w/api.php?format=json&action=query"

def get_links(title: str) -> List[str]:
    """
    @rtype: List[str]
    @param title: A title corresponding to a Wikipedia article
    @return: A list of Wikipedia links that the article contains.
    """

    # title = format_title(title)
    plcontinue = ""
    links = []

    while (True):
        temp = f"&plcontinue={plcontinue}" if plcontinue != "" else ""
        r = requests.get(f"{BASE_URL}&titles={title}&prop=links&pllimit=max{temp}")
        try:
            data = r.json()
            id = next(iter(data['query']['pages']))
            temp_links = data['query']['pages'][id]['links']
            for link in temp_links:
                links.append(link['title'])
            plcontinue = data['continue']['plcontinue']
        except Exception as e:
            break
    for i in range(len(links)):
        if re.search("^[A-Za-z\s]+:[A-Za-z]+", links[i]):
            links = links[:i]
            break
    links.insert(0, title)
    return jsonify(links)

def get_summary(title: str) -> str:
    i = 0
    r = requests.get(f"{BASE_URL}&titles={title}&prop=extracts&explaintext&exchars=100")
    data = r.json()
    pages = data['query']['pages']
    page = next(iter(pages.items()))[0]
    return pages[page]['extract']

# def get_graph(title: str) -> Response:
#     links = get_links(title)
#     links.insert(0, title)
#     nodes = [{"id": links[i], "name": links[i], "val": 1, "color": "rgba(0, 0, 0, 1)"} for i in [random.randrange(0, len(links)) for x in range(10)]]
#     nodes.insert(0, {"id": title, "name": title, "val": 1, "color": "rgba(0, 0, 0, 1)"})
#     edges = [{"source": title, "target": node["id"]} for node in nodes]
#     data = {}
#     data['nodes'] = nodes
#     data['links'] = edges
#     j = jsonify(data)
#     return j