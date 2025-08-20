#!/usr/bin/env python3
"""
LINE @ 提醒系統安全啟動腳本
"""

import os
import sys
import socket
import threading
import time
from pathlib import Path

def check_port_available(port):
    """檢查端口是否可用"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', port))
            return True
    except OSError:
        return False

def find_available_port(start_port=5000):
    """尋找可用的端口"""
    port = start_port
    while port < start_port + 100:
        if check_port_available(port):
            return port
        port += 1
    return None

def check_file_permissions():
    """檢查檔案權限"""
    files_to_check = [
        'app.py',
        'line_bot_handler.py',
        'templates/index.html'
    ]
    
    for file_path in files_to_check:
        if not os.path.exists(file_path):
            print(f"❌ 檔案不存在: {file_path}")
            return False
        
        if not os.access(file_path, os.R_OK):
            print(f"❌ 無法讀取檔案: {file_path}")
            return False
    
    return True

def create_test_data():
    """建立測試資料"""
    try:
        import sqlite3
        conn = sqlite3.connect('line_data.db')
        cursor = conn.cursor()
        
        # 檢查是否有資料
        cursor.execute('SELECT COUNT(*) FROM mentioned_users')
        count = cursor.fetchone()[0]
        
        if count == 0:
            # 插入測試資料
            test_data = [
                ('user_test1', '測試用戶1', 'group_test', '這是一個測試訊息 @測試用戶1', '2024-01-01 10:00:00', 'msg_001'),
                ('user_test2', '測試用戶2', 'group_test', '另一個測試 @測試用戶2', '2024-01-01 11:00:00', 'msg_002'),
                ('user_test1', '測試用戶1', 'group_test', '再次提及 @測試用戶1', '2024-01-01 12:00:00', 'msg_003'),
            ]
            
            cursor.executemany('''
                INSERT INTO mentioned_users (user_id, user_name, group_id, message, mentioned_at, message_id)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', test_data)
            
            conn.commit()
            print("✅ 已建立測試資料")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ 建立測試資料失敗: {e}")
        return False

def start_flask_app(port):
    """啟動 Flask 應用程式"""
    try:
        from app import app
        
        print(f"🌐 啟動 Flask 應用程式於端口 {port}...")
        print(f"📱 前台介面: http://127.0.0.1:{port}")
        print(f"🔗 Webhook URL: http://127.0.0.1:{port}/webhook")
        print("=" * 50)
        print("按 Ctrl+C 停止服務")
        print("=" * 50)
        
        app.run(
            debug=True,
            host='127.0.0.1',
            port=port,
            use_reloader=False  # 避免重複啟動
        )
        
    except ImportError as e:
        print(f"❌ 導入錯誤: {e}")
        print("請確認已安裝所有依賴套件: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ 啟動失敗: {e}")

def main():
    """主函數"""
    print("🔍 檢查系統環境...")
    print("=" * 30)
    
    # 檢查檔案權限
    if not check_file_permissions():
        print("❌ 檔案權限檢查失敗")
        return
    
    # 檢查環境變數檔案
    if not os.path.exists('.env'):
        print("⚠️  .env 檔案不存在，正在建立...")
        try:
            with open('env_example.txt', 'r', encoding='utf-8') as f:
                content = f.read()
            
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ .env 檔案已建立")
            print("⚠️  請記得編輯 .env 檔案並填入您的 LINE Bot 設定")
        except Exception as e:
            print(f"❌ 建立 .env 檔案失敗: {e}")
            return
    
    # 尋找可用端口
    port = find_available_port()
    if port is None:
        print("❌ 無法找到可用端口")
        return
    
    print(f"✅ 找到可用端口: {port}")
    
    # 建立測試資料
    create_test_data()
    
    # 啟動應用程式
    try:
        start_flask_app(port)
    except KeyboardInterrupt:
        print("\n👋 服務已停止")
    except Exception as e:
        print(f"❌ 啟動失敗: {e}")

if __name__ == "__main__":
    main() 