#!/bin/bash
# Render 建置腳本

# 安裝系統依賴
apt-get update && apt-get install -y gcc python3-dev

# 安裝 Python 套件
pip install -r requirements.txt 