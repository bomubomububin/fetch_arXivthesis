from datetime import datetime, timedelta
from fetch import fetch_arxiv_data
from filerTrans import filter_papers, translate_text
from slack_notify import send_slack_notification
import os
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

def main():
    categories = ["cs.LG", "cs.NI", "cs.AI"] 
    keywords = ["federated learning", "sensing", "communication", "edge computing"]
    target_date = datetime.now() - timedelta(days=1)
    
    # ベタ書きをやめて、環境変数から取得するンゴ！
    SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

    print(f"【{target_date.strftime('%Y-%m-%d')}】の論文を取得中やで...")

    papers = fetch_arxiv_data(categories, max_results=200)
    filtered_papers = filter_papers(papers, keywords, target_date)
    
    if not filtered_papers:
        message = f"【お知らせ】{target_date.strftime('%Y-%m-%d')}の条件に合う新着論文は無かったンゴ..."
        send_slack_notification(SLACK_WEBHOOK_URL, message)
        return

    slack_message = f"🎉 *{target_date.strftime('%Y-%m-%d')}の新着論文が {len(filtered_papers)} 件見つかったで！*\n\n"

    for i, paper in enumerate(filtered_papers, 1):
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