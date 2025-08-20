#!/usr/bin/env python3
"""
一鍵雲端部署工具
支援多種雲端平台
"""

import os
import sys
import subprocess

def print_banner():
    """顯示歡迎橫幅"""
    print("=" * 60)
    print("☁️  LINE @ 提醒系統 - 雲端部署工具")
    print("=" * 60)
    print("支援平台：")
    print("1. 🌟 Heroku (推薦 - 最簡單)")
    print("2. 🚄 Railway (推薦 - 免費額度充足)")
    print("3. 🎨 Render (推薦 - 穩定可靠)")
    print("4. ⚡ Vercel (推薦 - 速度快)")
    print("5. 🐳 Docker (自架伺服器)")
    print("6. 📋 查看部署指南")
    print("0. ❌ 退出")
    print("=" * 60)

def check_prerequisites():
    """檢查前置需求"""
    print("🔍 檢查系統環境...")
    
    # 檢查 Python 版本
    if sys.version_info < (3, 7):
        print("❌ 需要 Python 3.7 或更高版本")
        return False
    
    # 檢查必要檔案
    required_files = [
        'app.py',
        'requirements.txt',
        'wsgi.py',
        'templates/index.html'
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ 缺少必要檔案: {file_path}")
            return False
    
    # 檢查 .env 檔案
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
            return False
    
    print("✅ 系統環境檢查完成")
    return True

def deploy_heroku():
    """部署到 Heroku"""
    print("\n🚀 開始部署到 Heroku...")
    
    # 檢查 Heroku CLI
    try:
        subprocess.run(['heroku', '--version'], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ 請先安裝 Heroku CLI")
        print("安裝指令:")
        print("  macOS: brew install heroku/brew/heroku")
        print("  Windows: 下載 https://devcenter.heroku.com/articles/heroku-cli")
        return False
    
    # 執行部署腳本
    try:
        subprocess.run([sys.executable, 'deploy_heroku.py'], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def deploy_railway():
    """部署到 Railway"""
    print("\n🚄 開始部署到 Railway...")
    
    # 檢查 Railway CLI
    try:
        subprocess.run(['railway', '--version'], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ 請先安裝 Railway CLI")
        print("安裝指令: npm install -g @railway/cli")
        return False
    
    # 執行部署腳本
    try:
        subprocess.run([sys.executable, 'deploy_railway.py'], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def deploy_render():
    """部署到 Render"""
    print("\n🎨 開始部署到 Render...")
    
    # 檢查 Git
    if not os.path.exists('.git'):
        print("❌ 請先初始化 Git 倉庫")
        print("執行: git init")
        return False
    
    # 執行部署腳本
    try:
        subprocess.run([sys.executable, 'deploy_render.py'], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def deploy_vercel():
    """部署到 Vercel"""
    print("\n⚡ 開始部署到 Vercel...")
    
    # 檢查 Vercel CLI
    try:
        subprocess.run(['vercel', '--version'], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ 請先安裝 Vercel CLI")
        print("安裝指令: npm install -g vercel")
        return False
    
    # 執行部署腳本
    try:
        subprocess.run([sys.executable, 'deploy_vercel.py'], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def deploy_docker():
    """Docker 部署"""
    print("\n🐳 開始 Docker 部署...")
    
    # 檢查 Docker
    try:
        subprocess.run(['docker', '--version'], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ 請先安裝 Docker")
        print("下載: https://www.docker.com/products/docker-desktop")
        return False
    
    # 建立並啟動容器
    try:
        print("🔨 建立 Docker 映像...")
        subprocess.run(['docker-compose', 'up', '-d', '--build'], check=True)
        print("✅ Docker 部署完成")
        print("📱 應用程式運行在: http://localhost:5000")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Docker 部署失敗: {e}")
        return False

def show_deployment_guide():
    """顯示部署指南"""
    print("\n📋 部署指南")
    print("=" * 40)
    
    if os.path.exists('CLOUD_DEPLOYMENT.md'):
        try:
            with open('CLOUD_DEPLOYMENT.md', 'r', encoding='utf-8') as f:
                content = f.read()
                print(content)
        except Exception as e:
            print(f"❌ 讀取部署指南失敗: {e}")
    else:
        print("❌ 部署指南檔案不存在")

def main():
    """主函數"""
    while True:
        print_banner()
        
        try:
            choice = input("請選擇部署平台 (0-6): ").strip()
        except KeyboardInterrupt:
            print("\n👋 再見！")
            break
        
        if choice == '0':
            print("👋 再見！")
            break
        elif choice == '1':
            if check_prerequisites():
                deploy_heroku()
        elif choice == '2':
            if check_prerequisites():
                deploy_railway()
        elif choice == '3':
            if check_prerequisites():
                deploy_render()
        elif choice == '4':
            if check_prerequisites():
                deploy_vercel()
        elif choice == '5':
            if check_prerequisites():
                deploy_docker()
        elif choice == '6':
            show_deployment_guide()
        else:
            print("❌ 無效選擇，請重新輸入")
        
        input("\n按 Enter 繼續...")

if __name__ == "__main__":
    main() 