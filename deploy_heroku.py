#!/usr/bin/env python3
"""
Heroku 自動部署腳本
"""

import os
import subprocess
import sys

def check_heroku_cli():
    """檢查 Heroku CLI 是否安裝"""
    try:
        subprocess.run(['heroku', '--version'], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def create_heroku_app(app_name):
    """建立 Heroku 應用程式"""
    try:
        print(f"🚀 建立 Heroku 應用程式: {app_name}")
        subprocess.run(['heroku', 'create', app_name], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 建立應用程式失敗: {e}")
        return False

def set_environment_variables():
    """設定環境變數"""
    try:
        print("🔧 設定環境變數...")
        
        # 從 .env 檔案讀取變數
        if os.path.exists('.env'):
            with open('.env', 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        subprocess.run(['heroku', 'config:set', f'{key}={value}'], check=True)
        
        # 設定生產環境變數
        subprocess.run(['heroku', 'config:set', 'FLASK_ENV=production'], check=True)
        subprocess.run(['heroku', 'config:set', 'FLASK_DEBUG=False'], check=True)
        
        print("✅ 環境變數設定完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 設定環境變數失敗: {e}")
        return False

def deploy_to_heroku():
    """部署到 Heroku"""
    try:
        print("📤 部署到 Heroku...")
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Deploy to Heroku'], check=True)
        subprocess.run(['git', 'push', 'heroku', 'main'], check=True)
        print("✅ 部署完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 部署失敗: {e}")
        return False

def open_app():
    """開啟應用程式"""
    try:
        print("🌐 開啟應用程式...")
        subprocess.run(['heroku', 'open'], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 開啟應用程式失敗: {e}")
        return False

def get_app_url():
    """獲取應用程式 URL"""
    try:
        result = subprocess.run(['heroku', 'info', '-s'], capture_output=True, text=True, check=True)
        for line in result.stdout.split('\n'):
            if line.startswith('web_url='):
                return line.split('=')[1]
    except subprocess.CalledProcessError:
        pass
    return None

def main():
    """主函數"""
    print("🚀 Heroku 自動部署工具")
    print("=" * 40)
    
    # 檢查 Heroku CLI
    if not check_heroku_cli():
        print("❌ 請先安裝 Heroku CLI")
        print("安裝指令: https://devcenter.heroku.com/articles/heroku-cli")
        return
    
    # 檢查 Git 倉庫
    if not os.path.exists('.git'):
        print("❌ 請先初始化 Git 倉庫")
        print("執行: git init")
        return
    
    # 獲取應用程式名稱
    app_name = input("請輸入 Heroku 應用程式名稱 (或按 Enter 自動生成): ").strip()
    
    # 建立應用程式
    if app_name:
        if not create_heroku_app(app_name):
            return
    
    # 設定環境變數
    if not set_environment_variables():
        return
    
    # 部署
    if not deploy_to_heroku():
        return
    
    # 獲取應用程式 URL
    app_url = get_app_url()
    if app_url:
        print(f"🎉 部署成功！")
        print(f"📱 應用程式網址: {app_url}")
        print(f"🔗 Webhook URL: {app_url}/webhook")
        
        # 開啟應用程式
        open_app()
    else:
        print("✅ 部署完成，請手動檢查應用程式狀態")

if __name__ == "__main__":
    main() 