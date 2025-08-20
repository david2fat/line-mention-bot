#!/usr/bin/env python3
"""
LINE @ 提醒系統安裝腳本
"""

import os
import sys
import subprocess
import sqlite3

def install_requirements():
    """安裝 Python 依賴套件"""
    print("正在安裝 Python 依賴套件...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依賴套件安裝完成")
    except subprocess.CalledProcessError:
        print("❌ 依賴套件安裝失敗")
        return False
    return True

def create_env_file():
    """建立環境變數檔案"""
    if not os.path.exists('.env'):
        print("正在建立 .env 檔案...")
        try:
            with open('env_example.txt', 'r', encoding='utf-8') as f:
                content = f.read()
            
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ .env 檔案已建立")
            print("⚠️  請記得編輯 .env 檔案並填入您的 LINE Bot 設定")
        except Exception as e:
            print(f"❌ 建立 .env 檔案失敗: {e}")
            return False
    else:
        print("✅ .env 檔案已存在")
    return True

def init_database():
    """初始化資料庫"""
    print("正在初始化資料庫...")
    try:
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
        print("✅ 資料庫初始化完成")
    except Exception as e:
        print(f"❌ 資料庫初始化失敗: {e}")
        return False
    return True

def create_directories():
    """建立必要的目錄"""
    print("正在建立目錄結構...")
    try:
        os.makedirs('templates', exist_ok=True)
        print("✅ 目錄結構建立完成")
    except Exception as e:
        print(f"❌ 建立目錄失敗: {e}")
        return False
    return True

def main():
    """主安裝流程"""
    print("🚀 開始安裝 LINE @ 提醒系統...")
    print("=" * 50)
    
    # 建立目錄
    if not create_directories():
        return
    
    # 安裝依賴套件
    if not install_requirements():
        return
    
    # 建立環境變數檔案
    if not create_env_file():
        return
    
    # 初始化資料庫
    if not init_database():
        return
    
    print("=" * 50)
    print("🎉 安裝完成！")
    print("\n📋 後續步驟：")
    print("1. 編輯 .env 檔案，填入您的 LINE Bot 設定")
    print("2. 在 LINE Developers Console 設定 Webhook URL")
    print("3. 執行 'python app.py' 啟動應用程式")
    print("4. 開啟瀏覽器前往 http://localhost:5000")
    print("\n📖 詳細說明請參考 README.md")

if __name__ == "__main__":
    main() 