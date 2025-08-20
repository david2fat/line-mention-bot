#!/usr/bin/env python3
"""
Railway 自動部署腳本
"""

import os
import subprocess
import sys

def check_railway_cli():
    """檢查 Railway CLI 是否安裝"""
    try:
        subprocess.run(['railway', '--version'], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def login_railway():
    """登入 Railway"""
    try:
        print("🔐 登入 Railway...")
        subprocess.run(['railway', 'login'], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 登入失敗: {e}")
        return False

def create_railway_project():
    """建立 Railway 專案"""
    try:
        print("🚀 建立 Railway 專案...")
        subprocess.run(['railway', 'init'], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 建立專案失敗: {e}")
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
                        subprocess.run(['railway', 'variables', 'set', f'{key}={value}'], check=True)
        
        # 設定生產環境變數
        subprocess.run(['railway', 'variables', 'set', 'FLASK_ENV=production'], check=True)
        subprocess.run(['railway', 'variables', 'set', 'FLASK_DEBUG=False'], check=True)
        
        print("✅ 環境變數設定完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 設定環境變數失敗: {e}")
        return False

def deploy_to_railway():
    """部署到 Railway"""
    try:
        print("📤 部署到 Railway...")
        subprocess.run(['railway', 'deploy'], check=True)
        print("✅ 部署完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 部署失敗: {e}")
        return False

def get_service_url():
    """獲取服務 URL"""
    try:
        result = subprocess.run(['railway', 'status'], capture_output=True, text=True, check=True)
        # 解析輸出找到 URL
        for line in result.stdout.split('\n'):
            if 'https://' in line:
                return line.strip()
    except subprocess.CalledProcessError:
        pass
    return None

def main():
    """主函數"""
    print("🚀 Railway 自動部署工具")
    print("=" * 40)
    
    # 檢查 Railway CLI
    if not check_railway_cli():
        print("❌ 請先安裝 Railway CLI")
        print("安裝指令: npm install -g @railway/cli")
        return
    
    # 登入 Railway
    if not login_railway():
        return
    
    # 建立專案
    if not create_railway_project():
        return
    
    # 設定環境變數
    if not set_environment_variables():
        return
    
    # 部署
    if not deploy_to_railway():
        return
    
    # 獲取服務 URL
    service_url = get_service_url()
    if service_url:
        print(f"🎉 部署成功！")
        print(f"📱 服務網址: {service_url}")
        print(f"🔗 Webhook URL: {service_url}/webhook")
    else:
        print("✅ 部署完成，請手動檢查服務狀態")

if __name__ == "__main__":
    main() 