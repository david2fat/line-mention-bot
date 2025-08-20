#!/usr/bin/env python3
"""
Vercel 自動部署腳本
"""

import os
import subprocess
import sys

def check_vercel_cli():
    """檢查 Vercel CLI 是否安裝"""
    try:
        subprocess.run(['vercel', '--version'], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def create_vercel_json():
    """建立 vercel.json 設定檔案"""
    vercel_config = {
        "version": 2,
        "builds": [
            {
                "src": "wsgi.py",
                "use": "@vercel/python"
            }
        ],
        "routes": [
            {
                "src": "/(.*)",
                "dest": "wsgi.py"
            }
        ],
        "env": {
            "FLASK_ENV": "production",
            "FLASK_DEBUG": "False"
        }
    }
    
    try:
        import json
        with open('vercel.json', 'w') as f:
            json.dump(vercel_config, f, indent=2)
        print("✅ vercel.json 檔案已建立")
        return True
    except Exception as e:
        print(f"❌ 建立 vercel.json 失敗: {e}")
        return False

def deploy_to_vercel():
    """部署到 Vercel"""
    try:
        print("📤 部署到 Vercel...")
        subprocess.run(['vercel', '--prod'], check=True)
        print("✅ 部署完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 部署失敗: {e}")
        return False

def main():
    """主函數"""
    print("🚀 Vercel 自動部署工具")
    print("=" * 40)
    
    # 檢查 Vercel CLI
    if not check_vercel_cli():
        print("❌ 請先安裝 Vercel CLI")
        print("安裝指令: npm install -g vercel")
        return
    
    # 建立 vercel.json
    if not create_vercel_json():
        return
    
    # 部署
    if not deploy_to_vercel():
        return
    
    print("\n🎉 部署成功！")
    print("📱 請檢查 Vercel 儀表板獲取您的應用程式 URL")
    print("🔗 將 URL + /webhook 設定為 LINE Bot 的 Webhook URL")

if __name__ == "__main__":
    main() 