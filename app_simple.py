from flask import Flask, request, render_template, jsonify
import sqlite3
import json
import os
import re
from datetime import datetime
from dotenv import load_dotenv
import requests

# 載入環境變數
load_dotenv()

app = Flask(__name__)

# LINE Bot 設定
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

# 初始化資料庫
def init_db():
    conn = sqlite3.connect('line_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mentioned_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            user_name TEXT,
            group_id TEXT,
            message TEXT,
            mentioned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            message_id TEXT
        )
    ''')
    conn.commit()
    conn.close()

# 初始化資料庫
init_db()

@app.route("/")
def index():
    """前台首頁"""
    return render_template('index.html')

@app.route("/test")
def test():
    """測試頁面"""
    return render_template('test.html')

@app.route("/webhook", methods=['POST'])
def callback():
    """LINE Bot Webhook 端點"""
    try:
        # 驗證簽名（簡化版本）
        body = request.get_data(as_text=True)
        data = json.loads(body)
        
        # 處理訊息事件
        for event in data.get('events', []):
            if event['type'] == 'message' and event['message']['type'] == 'text':
                handle_message(event)
        
        return 'OK'
    except Exception as e:
        print(f"Webhook 處理錯誤: {e}")
        return 'Error', 500

def handle_message(event):
    """處理 LINE 訊息事件"""
    try:
        # 檢查是否為群組訊息
        if 'source' in event and 'groupId' in event['source']:
            group_id = event['source']['groupId']
            user_id = event['source']['userId']
            message_text = event['message']['text']
            
            print(f"收到群組訊息: {message_text}")
            
            # 檢查是否包含 @ 提及
            if '@' in message_text:
                mentioned_users = parse_mentions(message_text, group_id)
                
                if mentioned_users:
                    # 儲存提及記錄
                    save_mentions(mentioned_users, group_id, message_text, event['message']['id'])
                    
                    # 回覆確認訊息
                    reply_message(event['replyToken'], mentioned_users)
                    
                    print(f"已記錄 {len(mentioned_users)} 個提及")
    except Exception as e:
        print(f"處理訊息時發生錯誤: {e}")

def parse_mentions(text, group_id):
    """解析訊息中的 @ 提及"""
    mentioned_users = []
    
    # 多種提及格式的正則表達式
    mention_patterns = [
        r'@(\w+)',  # @英文名稱
        r'@([\u4e00-\u9fff]+)',  # @中文名稱
        r'@([^\s]+)',  # @任何非空白字符
    ]
    
    for pattern in mention_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            # 避免重複記錄
            if not any(user['user_name'] == match for user in mentioned_users):
                mentioned_users.append({
                    'user_name': match,
                    'user_id': f"user_{match}_{group_id}",
                    'group_id': group_id
                })
    
    return mentioned_users

def save_mentions(mentioned_users, group_id, message, message_id):
    """儲存提及記錄到資料庫"""
    try:
        conn = sqlite3.connect('line_data.db')
        cursor = conn.cursor()
        
        for user in mentioned_users:
            cursor.execute('''
                INSERT INTO mentioned_users 
                (user_id, user_name, group_id, message, message_id, mentioned_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                user['user_id'],
                user['user_name'],
                group_id,
                message,
                message_id,
                datetime.now().isoformat()
            ))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"儲存提及記錄時發生錯誤: {e}")

def reply_message(reply_token, mentioned_users):
    """回覆 LINE 訊息"""
    try:
        if len(mentioned_users) == 1:
            reply_text = f"✅ 已記錄 @{mentioned_users[0]['user_name']} 的提及"
        else:
            names = [f"@{user['user_name']}" for user in mentioned_users]
            reply_text = f"✅ 已記錄 {len(mentioned_users)} 位使用者的提及: {', '.join(names)}"
        
        # 使用 LINE Messaging API 回覆
        url = 'https://api.line.me/v2/bot/message/reply'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}'
        }
        data = {
            'replyToken': reply_token,
            'messages': [
                {
                    'type': 'text',
                    'text': reply_text
                }
            ]
        }
        
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            print(f"回覆訊息失敗: {response.status_code}")
            
    except Exception as e:
        print(f"回覆訊息時發生錯誤: {e}")

@app.route("/api/mentioned-users")
def get_mentioned_users():
    """API 端點：獲取所有被提及的使用者資料"""
    conn = sqlite3.connect('line_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT user_id, user_name, group_id, message, mentioned_at, message_id
        FROM mentioned_users
        ORDER BY mentioned_at DESC
        LIMIT 50
    ''')
    
    users = []
    for row in cursor.fetchall():
        # 格式化群組 ID 為更易讀的名稱
        group_id = row[2]
        if group_id:
            # 如果群組 ID 很長，取前8位並加上省略號
            if len(group_id) > 12:
                group_display = f"群組 {group_id[:8]}..."
            else:
                group_display = f"群組 {group_id}"
        else:
            group_display = "未知群組"
            
        users.append({
            'user_id': row[0],
            'user_name': row[1],
            'group_id': group_display,
            'message': row[3],
            'mentioned_at': row[4],
            'message_id': row[5]
        })
    
    conn.close()
    return jsonify(users)

@app.route("/api/statistics")
def get_statistics():
    """API 端點：獲取統計資料"""
    conn = sqlite3.connect('line_data.db')
    cursor = conn.cursor()
    
    # 總提及次數
    cursor.execute('SELECT COUNT(*) FROM mentioned_users')
    total_mentions = cursor.fetchone()[0]
    
    # 被提及的使用者數量（按 user_id 分組）
    cursor.execute('SELECT COUNT(DISTINCT user_id) FROM mentioned_users')
    unique_users = cursor.fetchone()[0]
    
    # 群組數量
    cursor.execute('SELECT COUNT(DISTINCT group_id) FROM mentioned_users')
    group_count = cursor.fetchone()[0]
    
    # 最常被提及的使用者（合併相同用戶的不同名稱）
    cursor.execute('''
        SELECT 
            user_id,
            GROUP_CONCAT(DISTINCT user_name ORDER BY mentioned_at DESC) as all_names,
            COUNT(*) as mention_count
        FROM mentioned_users
        GROUP BY user_id
        ORDER BY mention_count DESC
        LIMIT 10
    ''')
    
    top_users = []
    for row in cursor.fetchall():
        user_id, all_names, count = row
        # 取最新的名稱作為顯示名稱
        latest_name = all_names.split(',')[0] if all_names else '未知用戶'
        # 如果有多個名稱，在括號中顯示
        if ',' in all_names:
            display_name = f"{latest_name} ({len(all_names.split(','))}個名稱)"
        else:
            display_name = latest_name
            
        top_users.append({
            'user_name': display_name,
            'count': count,
            'user_id': user_id
        })
    
    # 今日提及次數
    cursor.execute('''
        SELECT COUNT(*) FROM mentioned_users 
        WHERE DATE(mentioned_at) = DATE('now')
    ''')
    today_mentions = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'total_mentions': total_mentions,
        'unique_users': unique_users,
        'group_count': group_count,
        'top_users': top_users,
        'today_mentions': today_mentions
    })

if __name__ == "__main__":
    # 雲端部署設定
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)

# 確保應用程式可以正確啟動
app.config['SERVER_NAME'] = None 