import re
from datetime import datetime, timedelta
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def filter_papers(papers, keywords, target_date):
    # 過去3日分の日付リストを作って、API登録のラグを許容するセーフティネットや！
    allowed_dates = [(target_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(4)]
    keyword_pattern = re.compile('|'.join(keywords), re.IGNORECASE)
    
    filtered = []
    for paper in papers:
        # arXivはタイムゾーンの関係で未来の日付になることも稀にあるから、それも一応拾うようにしとるで
        if paper['published_date'] in allowed_dates or paper['published_date'] == (target_date + timedelta(days=1)).strftime('%Y-%m-%d'):
            if keyword_pattern.search(paper['title']) or keyword_pattern.search(paper['summary']):
                filtered.append(paper)
    return filtered

def translate_text(text, target_language='ja'):
    API_KEY = os.environ.get("GOOGLE_API_KEY")
    url = f"https://translation.googleapis.com/language/translate/v2?key={API_KEY}"
    data = {'q': text, 'target': target_language}
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()['data']['translations'][0]['translatedText']
    else:
        print(f"翻訳エラーや...: {response.text}")
        return text