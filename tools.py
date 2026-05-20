from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from langchain_tavily import TavilySearch
import os 
from dotenv import load_dotenv
from rich import print
load_dotenv()


tavily = TavilySearch(max_results=3)

@tool 
def web_search(query:str)->str:
    """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets"""
    results = tavily.invoke({"query":query})
    out = []
    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )
    
    print("------------------------------------"*10)
    print("Web search results for query : ",query)
    print("\n".join(out))
    print("------------------------------------"*10)


    return "\n-----\n".join(out)

def scrape_url(url: str)->str:
    """Scrape and return clean text content from a given URL for deeper reading."""

    try:
        resp = requests.get(url=url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text,"html.parser")

        for tag in soup(["script","style","nav","footer"]):
            tag.decompose()

        return soup.get_text(separator=" ",strip=True)[:3000]  
    except Exception as e:
        return f"Could not scrape URL : {str(e)}"
    
# print(scrape_url("https://www.scrapethissite.com/pages/frames/"))