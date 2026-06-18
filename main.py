from datetime import datetime, timedelta
from fetch import fetch_arxiv_data
from fetch_semantic import fetch_semantic_papers
from filerTrans import filter_papers, translate_text
from slack_notify import send_slack_notification
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    # --- 検索設定 ---
    categories = ["cs.LG", "cs.NI", "cs.AI"] 
    # Semantic Scholar用の検索クエリ（スペース区切り）
    semantic_query = "federated learning sensing communication"
    
    keywords = ["federated learning", "sensing", "communication", "edge computing"]
    target_date = datetime.now() - timedelta(days=1)
    target_year = target_date.strftime('%Y')
    
    SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

    print(f"【{target_date.strftime('%Y-%m-%d')}】付近の論文を取得中やで...")

    # 1. 欲張りセット：arXivとSemantic Scholarの両方から取得！
    arxiv_papers = fetch_arxiv_data(categories, max_results=100)
    semantic_papers = fetch_semantic_papers(semantic_query, target_year, limit=50)
    
    # 2. 2つのリストを合体
    all_papers = arxiv_papers + semantic_papers
    
    # 3. キーワードと日付でフィルタリング
    filtered_papers = filter_papers(all_papers, keywords, target_date)
    
    # 4. 重複チェック（arXivとIEEE両方に同じ論文が出た場合に1つにまとめるで）
    unique_papers = []
    seen_titles = set()
    for p in filtered_papers:
        # タイトルの小文字化＆スペース削除＆[学会名]の除去で簡易的に重複判定するンゴ
        clean_title = p['title'].lower().replace(" ", "")
        check_title = clean_title.split("]")[-1] if "]" in clean_title else clean_title
        
        if check_title not in seen_titles:
            unique_papers.append(p)
            seen_titles.add(check_title)

    if not unique_papers:
        message = f"【お知らせ】{target_date.strftime('%Y-%m-%d')}付近の連合学習・通信系の新着論文は無かったンゴ..."
        send_slack_notification(SLACK_WEBHOOK_URL, message)
        return

    # 5. Slackに飛ばすメッセージを組み立てる
    slack_message = f"🎉 *最新の論文が {len(unique_papers)} 件見つかったで！(arXiv & IEEE/ACM等)*\n\n"

    for i, paper in enumerate(unique_papers, 1):
        translated_title = translate_text(paper['title'])
        translated_summary = translate_text(paper['summary'])
        
        slack_message += f"*{i}. {translated_title}*\n"
        slack_message += f"📝 原題: {paper['title']}\n"
        slack_message += f"🔗 URL: {paper['link']}\n"
        slack_message += f"💡 要約:\n> {translated_summary[:200]}... (続く)\n"
        slack_message += "-" * 40 + "\n"

    send_slack_notification(SLACK_WEBHOOK_URL, slack_message)

if __name__ == "__main__":
    main()