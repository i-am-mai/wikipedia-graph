from typing import List
import requests

BASE_URL = "https://en.wikipedia.org/w/api.php?format=json&action=query"

def format_title(title: str) -> str:
    """
    @rtype: str
    @param title: A title corresponding to a Wikipedia article
    @return: The title separated by underscores
    """
    return "_".join(title.split(" "))

def get_links(title: str) -> List[str]:
    """
    @rtype: List[str]
    @param title: A title corresponding to a Wikipedia article
    @return: A list of Wikipedia links that the article contains.
    """

    title = format_title(title)
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
            return links

# Use this to test the API; change "Wikipedia" to any valid Wikipedia article title.

# links = get_links("Wikipedia")

# with open("test.txt", "wb") as file:
#     for link in links:
#         file.write((link).encode('utf-8'))
#         file.write("\n".encode('utf-8'))