import re
from datetime import datetime, timedelta
import requests
import os
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

def filter_papers(papers, keywords, target_date):
    target_date_str = target_date.strftime('%Y-%m-%d')
    keyword_pattern = re.compile('|'.join(keywords), re.IGNORECASE)
    return [paper for paper in papers if paper['published_date'] == target_date_str and 
            (keyword_pattern.search(paper['title']) or keyword_pattern.search(paper['summary']))]

def translate_text(text, target_language='ja'):
    # ベタ書きをやめて、環境変数から取得するンゴ！
    API_KEY = os.environ.get("GOOGLE_API_KEY")
    
    url = f"https://translation.googleapis.com/language/translate/v2?key={API_KEY}"
    data = {
        'q': text,
        'target': target_language
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        return response.json()['data']['translations'][0]['translatedText']
    else:
        print(f"翻訳エラーや...: {response.text}")
        return text