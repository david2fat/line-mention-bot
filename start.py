#!/usr/bin/env python3
"""
LINE @ 提醒系統快速啟動腳本
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """檢查 Python 版本"""
    if sys.version_info < (3, 7):
        print("❌ 需要 Python 3.7 或更高版本")
        return False
    print(f"✅ Python 版本: {sys.version}")
    return True

def check_dependencies():
    """檢查依賴套件"""
    required_packages = [
        'flask',
        'line-bot-sdk',
        'python-dotenv'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少依賴套件: {', '.join(missing_packages)}")
        print("正在安裝...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ 依賴套件安裝完成")
        except subprocess.CalledProcessError:
            print("❌ 依賴套件安裝失敗")
            return False
    else:
        print("✅ 所有依賴套件已安裝")
    return True

def check_env_file():
    """檢查環境變數檔案"""
    env_file = Path('.env')
    if not env_file.exists():
        print("⚠️  .env 檔案不存在")
        print("正在建立 .env 檔案...")
        try:
            with open('env_example.txt', 'r', encoding='utf-8') as f:
                content = f.read()
            
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ .env 檔案已建立")
            print("⚠️  請記得編輯 .env 檔案並填入您的 LINE Bot 設定")
            return False
        except Exception as e:
            print(f"❌ 建立 .env 檔案失敗: {e}")
            return False
    else:
        print("✅ .env 檔案存在")
        return True

def check_line_bot_config():
    """檢查 LINE Bot 設定"""
    from dotenv import load_dotenv
    load_dotenv()
    
    access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    channel_secret = os.getenv('LINE_CHANNEL_SECRET')
    
    if not access_token or access_token == 'your_line_channel_access_token_here':
        print("❌ 請在 .env 檔案中設定 LINE_CHANNEL_ACCESS_TOKEN")
        return False
    
    if not channel_secret or channel_secret == 'your_line_channel_secret_here':
        print("❌ 請在 .env 檔案中設定 LINE_CHANNEL_SECRET")
        return False
    
    print("✅ LINE Bot 設定已配置")
    return True

def start_application():
    """啟動應用程式"""
    print("\n🚀 啟動 LINE @ 提醒系統...")
    print("=" * 50)
    print("📱 前台介面: http://localhost:5000")
    print("🔗 Webhook URL: http://localhost:5000/webhook")
    print("=" * 50)
    print("按 Ctrl+C 停止服務")
    print("=" * 50)
    
    try:
        from app import app
        app.run(debug=True, host='127.0.0.1', port=5000)
    except KeyboardInterrupt:
        print("\n👋 服務已停止")
    except Exception as e:
        print(f"❌ 啟動失敗: {e}")

def main():
    """主函數"""
    print("🔍 檢查系統環境...")
    print("=" * 30)
    
    # 檢查 Python 版本
    if not check_python_version():
        return
    
    # 檢查依賴套件
    if not check_dependencies():
        return
    
    # 檢查環境變數檔案
    if not check_env_file():
        print("\n📋 請完成以下步驟後重新執行:")
        print("1. 編輯 .env 檔案")
        print("2. 填入您的 LINE Bot 設定")
        print("3. 重新執行 python start.py")
        return
    
    # 檢查 LINE Bot 設定
    if not check_line_bot_config():
        print("\n📋 請完成以下步驟後重新執行:")
        print("1. 前往 LINE Developers Console")
        print("2. 建立新的 Channel (Messaging API)")
        print("3. 取得 Channel Access Token 和 Channel Secret")
        print("4. 更新 .env 檔案")
        print("5. 重新執行 python start.py")
        return
    
    # 啟動應用程式
    start_application()

if __name__ == "__main__":
    main() 