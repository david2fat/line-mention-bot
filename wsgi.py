from app_simple import app

# 確保應用程式可以正確啟動
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 