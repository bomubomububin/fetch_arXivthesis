import requests
import xml.etree.ElementTree as ET

def fetch_arxiv_data(categories: list, max_results: int = 200):
    # リストを ['cat:cs.LG', 'cat:cs.NI'] の形にして、'+OR+' で合体させるンゴ
    query_parts = [f"cat:{cat}" for cat in categories]
    search_query = "+OR+".join(query_parts)
    
    api_url = f'http://export.arxiv.org/api/query?search_query={search_query}&start=0&max_results={max_results}&sortBy=submittedDate'
    response = requests.get(api_url)
    root = ET.fromstring(response.text)

    ns = {'ns': 'http://www.w3.org/2005/Atom'}
    papers = []

    for entry in root.findall('ns:entry', ns):
        papers.append({
            "title": entry.find('ns:title', ns).text.strip(),
            "summary": entry.find('ns:summary', ns).text.strip(),
            "link": entry.find('ns:id', ns).text.strip(),
            "published_date": entry.find('ns:published', ns).text.split('T')[0],
        })
    return papers