from typing import List
from flask import jsonify, Response
import requests
import re

BASE_URL = "https://en.wikipedia.org/w/api.php?format=json"

def get_links(title: str) -> Response:
    """
    @rtype: List[str]
    @param title: A title corresponding to a Wikipedia article
    @return: A list of Wikipedia links that the article contains.
    """

    title = title.replace('&', '%26')
    plcontinue = ""
    links = []

    while (True):
        temp = f"&plcontinue={plcontinue}" if plcontinue != "" else ""
        r = requests.get(f"{BASE_URL}&action=query&redirects=1&titles={title}&prop=links&pllimit=max{temp}")
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
    return jsonify(links)

def get_summary(titles: str) -> Response:
    titles = titles.replace('&', '%26')
    i = 0
    r = requests.get(f"{BASE_URL}&action=query&redirects=1&titles={titles}&prop=extracts&exintro=true")
    data = r.json()
    pages = data['query']['pages']
    summaries = {}
    for page in pages:
        if "extract" in pages[page].keys():
            extract = re.sub('(?!<b>|</b>|<span>|</span>)(<[^<]+?>|;<[^<]+?>)', '', pages[page]['extract'])
            extract = re.sub('<!--[^<]+?-->', '', extract)
            if (len(extract) > 250):
                words = extract.split()
                i = 0
                extract = ""
                for x in words:
                    extract += " " + x
                    i += len(x)
                    if (i > 197):
                        break
                if extract[len(extract) - 1] == "":
                    extract = extract[:len(extract) - 1]
                extract += "..."
            summaries[pages[page]['title']] = extract
        else:
            summaries[pages[page]['title']] = f"<b>{pages[page]['title']}</b>"
    return jsonify(summaries)

def get_thumbnail(titles: str) -> Response:
    titles = titles.replace('&', '%26')
    r = requests.get(f"{BASE_URL}&action=query&redirects=1&titles={titles}&prop=pageimages&piprop=thumbnail&pilicense=any&pithumbsize=300")
    data = r.json()
    pages = data['query']['pages']
    images = {}
    for page in pages:
        if 'thumbnail' in pages[page].keys():
            images[pages[page]['title']] = pages[page]['thumbnail']['source']
        else:
            images[pages[page]['title']] = ""
    return jsonify(images)

def search(input: str) -> Response:
    r = requests.get(f"{BASE_URL}&action=opensearch&search={input}")
    data = r.json()
    if len(data) > 1:
        return jsonify(data[1])
    else:
        return jsonify(data[0])