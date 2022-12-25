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

def get_summary(titles: str) -> str:
    i = 0
    r = requests.get(f"{BASE_URL}&titles={titles}&prop=extracts&exintro=true&exchars=300")
    data = r.json()
    pages = data['query']['pages']
    summaries = {}
    for page in pages:
        try:
            extract = pages[page]['extract']
            summaries[pages[page]['title']] = re.sub('<[^<b]+?>', '', extract)
        except Exception as e:
            summaries[pages[page]['title']] = pages[page]['title']
    return jsonify(summaries)

def get_thumbnail(title: str) -> str:
    r = requests.get(f"{BASE_URL}&titles={title}&prop=pageimages&piprop=thumbnail")