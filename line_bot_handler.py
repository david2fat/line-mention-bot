"""
LINE Bot 處理器
專門處理 LINE 群組中的 @ 提及功能
"""

from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    GroupSource, UserSource, MentionEvent
)
import sqlite3
import json
import re
from datetime import datetime
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LineBotMentionHandler:
    def __init__(self, channel_access_token, channel_secret):
        self.line_bot_api = LineBotApi(channel_access_token)
        self.handler = WebhookHandler(channel_secret)
        self.setup_handlers()
    
    def setup_handlers(self):
        """設定事件處理器"""
        self.handler.add(MessageEvent, message=TextMessage)(self.handle_text_message)
    
    def handle_text_message(self, event):
        """處理文字訊息事件"""
        try:
            # 檢查是否為群組訊息
            if isinstance(event.source, GroupSource):
                group_id = event.source.group_id
                user_id = event.source.user_id
                message_text = event.message.text
                
                logger.info(f"收到群組訊息: {message_text}")
                
                # 檢查是否包含 @ 提及
                if self.contains_mention(message_text):
                    mentioned_users = self.parse_mentions(message_text, group_id)
                    
                    if mentioned_users:
                        # 儲存提及記錄
                        self.save_mentions(mentioned_users, group_id, message_text, event.message.id, user_id)
                        
                        # 回覆確認訊息
                        reply_text = self.generate_reply_message(mentioned_users)
                        self.line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=reply_text)
                        )
                        
                        logger.info(f"已記錄 {len(mentioned_users)} 個提及")
                
        except Exception as e:
            logger.error(f"處理訊息時發生錯誤: {e}")
    
    def contains_mention(self, text):
        """檢查文字是否包含 @ 提及"""
        # 檢查多種 @ 提及格式
        mention_patterns = [
            r'@\w+',  # @使用者名稱
            r'@[\u4e00-\u9fff]+',  # @中文名稱
            r'@[^\s]+',  # @任何非空白字符
        ]
        
        for pattern in mention_patterns:
            if re.search(pattern, text):
                return True
        return False
    
    def parse_mentions(self, text, group_id):
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
                        'user_id': f"user_{match}_{group_id}",  # 簡化的 ID 格式
                        'group_id': group_id
                    })
        
        return mentioned_users
    
    def save_mentions(self, mentioned_users, group_id, message, message_id, sender_id):
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
            logger.error(f"儲存提及記錄時發生錯誤: {e}")
    
    def generate_reply_message(self, mentioned_users):
        """生成回覆訊息"""
        if len(mentioned_users) == 1:
            return f"✅ 已記錄 @{mentioned_users[0]['user_name']} 的提及"
        else:
            names = [f"@{user['user_name']}" for user in mentioned_users]
            return f"✅ 已記錄 {len(mentioned_users)} 位使用者的提及: {', '.join(names)}"
    
    def get_group_members(self, group_id):
        """獲取群組成員列表"""
        try:
            members = self.line_bot_api.get_group_members(group_id)
            return members
        except Exception as e:
            logger.error(f"獲取群組成員時發生錯誤: {e}")
            return []
    
    def get_user_profile(self, user_id):
        """獲取使用者資料"""
        try:
            profile = self.line_bot_api.get_profile(user_id)
            return profile
        except Exception as e:
            logger.error(f"獲取使用者資料時發生錯誤: {e}")
            return None

class DatabaseManager:
    """資料庫管理類別"""
    
    def __init__(self, db_path='line_data.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化資料庫"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 建立提及記錄表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mentioned_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                user_name TEXT,
                group_id TEXT,
                message TEXT,
                mentioned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                message_id TEXT,
                sender_id TEXT
            )
        ''')
        
        # 建立群組資訊表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                group_id TEXT PRIMARY KEY,
                group_name TEXT,
                member_count INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 建立使用者資訊表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                display_name TEXT,
                picture_url TEXT,
                status_message TEXT,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_mention_statistics(self):
        """獲取提及統計資料"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 總提及次數
        cursor.execute('SELECT COUNT(*) FROM mentioned_users')
        total_mentions = cursor.fetchone()[0]
        
        # 被提及的使用者數量
        cursor.execute('SELECT COUNT(DISTINCT user_id) FROM mentioned_users')
        unique_users = cursor.fetchone()[0]
        
        # 群組數量
        cursor.execute('SELECT COUNT(DISTINCT group_id) FROM mentioned_users')
        group_count = cursor.fetchone()[0]
        
        # 最常被提及的使用者
        cursor.execute('''
            SELECT user_name, COUNT(*) as mention_count
            FROM mentioned_users
            GROUP BY user_id, user_name
            ORDER BY mention_count DESC
            LIMIT 10
        ''')
        top_users = [{'user_name': row[0], 'count': row[1]} for row in cursor.fetchall()]
        
        # 今日提及次數
        cursor.execute('''
            SELECT COUNT(*) FROM mentioned_users 
            WHERE DATE(mentioned_at) = DATE('now')
        ''')
        today_mentions = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_mentions': total_mentions,
            'unique_users': unique_users,
            'group_count': group_count,
            'top_users': top_users,
            'today_mentions': today_mentions
        }
    
    def get_recent_mentions(self, limit=20):
        """獲取最近的提及記錄"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, user_name, group_id, message, mentioned_at, message_id
            FROM mentioned_users
            ORDER BY mentioned_at DESC
            LIMIT ?
        ''', (limit,))
        
        mentions = []
        for row in cursor.fetchall():
            mentions.append({
                'user_id': row[0],
                'user_name': row[1],
                'group_id': row[2],
                'message': row[3],
                'mentioned_at': row[4],
                'message_id': row[5]
            })
        
        conn.close()
        return mentions 