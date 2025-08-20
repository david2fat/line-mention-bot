#!/usr/bin/env python3
"""
Render 自動部署腳本
"""

import os
import subprocess
import sys
import json

def create_render_yaml():
    """建立 render.yaml 設定檔案"""
    render_config = {
        "services": [
            {
                "type": "web",
                "name": "line-mention-bot",
                "env": "python",
                "plan": "free",
                "buildCommand": "pip install -r requirements.txt",
                "startCommand": "gunicorn wsgi:app",
                "envVars": [
                    {
                        "key": "FLASK_ENV",
                        "value": "production"
                    },
                    {
                        "key": "FLASK_DEBUG",
                        "value": "False"
                    }
                ]
            }
        ]
    }
    
    try:
        with open('render.yaml', 'w') as f:
            json.dump(render_config, f, indent=2)
        print("✅ render.yaml 檔案已建立")
        return True
    except Exception as e:
        print(f"❌ 建立 render.yaml 失敗: {e}")
        return False

def check_git_repo():
    """檢查 Git 倉庫"""
    if not os.path.exists('.git'):
        print("❌ 請先初始化 Git 倉庫")
        print("執行: git init")
        return False
    return True

def setup_github_repo():
    """設定 GitHub 倉庫"""
    try:
        print("🔧 設定 Git 倉庫...")
        
        # 檢查是否已有遠端倉庫
        result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
        if 'origin' not in result.stdout:
            repo_url = input("請輸入 GitHub 倉庫 URL: ").strip()
            if repo_url:
                subprocess.run(['git', 'remote', 'add', 'origin', repo_url], check=True)
        
        # 提交所有變更
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Deploy to Render'], check=True)
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Git 倉庫設定完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 設定失敗: {e}")
        return False

def main():
    """主函數"""
    print("🚀 Render 自動部署工具")
    print("=" * 40)
    
    # 建立 render.yaml
    if not create_render_yaml():
        return
    
    # 檢查 Git 倉庫
    if not check_git_repo():
        return
    
    # 設定 GitHub 倉庫
    if not setup_github_repo():
        return
    
    print("\n🎉 設定完成！")
    print("\n📋 後續步驟：")
    print("1. 前往 https://render.com")
    print("2. 登入並建立新帳戶")
    print("3. 點擊 'New +' 選擇 'Web Service'")
    print("4. 連接您的 GitHub 倉庫")
    print("5. 設定以下環境變數：")
    print("   - LINE_CHANNEL_ACCESS_TOKEN")
    print("   - LINE_CHANNEL_SECRET")
    print("6. 點擊 'Create Web Service'")
    print("\n🔗 部署完成後，您將獲得一個 HTTPS URL")
    print("📱 將該 URL + /webhook 設定為 LINE Bot 的 Webhook URL")

if __name__ == "__main__":
    main() 