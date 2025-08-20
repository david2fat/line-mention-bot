from flask import Flask, request, render_template, jsonify
from linebot.exceptions import InvalidSignatureError
import os
from dotenv import load_dotenv
from line_bot_handler import LineBotMentionHandler, DatabaseManager

# 載入環境變數
load_dotenv()

app = Flask(__name__)

# 初始化 LINE Bot 處理器和資料庫管理器
line_bot_handler = LineBotMentionHandler(
    os.getenv('LINE_CHANNEL_ACCESS_TOKEN'),
    os.getenv('LINE_CHANNEL_SECRET')
)
db_manager = DatabaseManager()

# 資料庫已由 DatabaseManager 初始化

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
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        line_bot_handler.handler.handle(body, signature)
    except InvalidSignatureError:
        return 'Invalid signature', 400
    
    return 'OK'

# 訊息處理已移至 LineBotMentionHandler 類別中

@app.route("/api/mentioned-users")
def get_mentioned_users():
    """API 端點：獲取所有被提及的使用者資料"""
    return jsonify(db_manager.get_recent_mentions(50))

@app.route("/api/statistics")
def get_statistics():
    """API 端點：獲取統計資料"""
    return jsonify(db_manager.get_mention_statistics())

if __name__ == "__main__":
    # 雲端部署設定
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port) 