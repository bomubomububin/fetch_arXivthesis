import requests
import json

def send_slack_notification(webhook_url: str, message: str):
    payload = {
        "text": message
    }
    headers = {'Content-Type': 'application/json'}
    
    response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
    
    if response.status_code == 200:
        print("Slackへの通知に成功したンゴ！")
    else:
        print(f"Slack通知失敗や... エラーコード: {response.status_code}, 理由: {response.text}")