FROM python:3.9-slim

# 設定工作目錄
WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴檔案
COPY requirements.txt .

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式檔案
COPY . .

# 建立必要的目錄
RUN mkdir -p templates

# 暴露端口
EXPOSE 5000

# 設定環境變數
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# 啟動命令
CMD ["python", "app.py"] 