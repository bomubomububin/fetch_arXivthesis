import requests

def fetch_semantic_papers(query: str, target_year: str, limit: int = 50):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    
    params = {
        "query": query,
        "fields": "title,abstract,url,publicationDate,venue",
        "limit": limit,
        "year": target_year
    }
    
    print(f"Semantic Scholarで [{query}] を検索中や...")
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Semantic ScholarのAPIエラーンゴ...: {response.status_code}")
        return []
        
    data = response.json()
    papers = []
    
    for item in data.get('data', []):
        if item.get('abstract'): # 要約がない論文は弾く
            # 学会名(IEEE, ACMなど)が取れたらタイトルに付ける工夫や
            venue = item.get('venue') or "学会不明/プレプリント"
            paper_url = item.get('url') or f"https://www.semanticscholar.org/paper/{item.get('paperId')}"
            pub_date = item.get('publicationDate') or "1970-01-01"
            
            papers.append({
                "title": f"[{venue}] {item.get('title')}",
                "summary": item.get('abstract'),
                "link": paper_url,
                "published_date": pub_date
            })
    return papers