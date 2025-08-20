# 🔧 故障排除指南

## HTTP 403 錯誤解決方案

### 問題描述
存取 localhost 時出現 "HTTP ERROR 403" 錯誤。

### 解決方案

#### 1. 使用新的啟動腳本
```bash
python run.py
```

#### 2. 檢查端口是否被佔用
```bash
# macOS/Linux
lsof -i :5000

# Windows
netstat -ano | findstr :5000
```

#### 3. 手動指定端口
如果 5000 端口被佔用，可以修改 `app.py`：
```python
if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8080)  # 改用 8080 端口
```

#### 4. 檢查防火牆設定
確保防火牆沒有阻擋本地連接。

#### 5. 使用測試頁面
啟動後先訪問測試頁面：
```
http://127.0.0.1:5000/test
```

## 常見問題解決

### 1. 模組導入錯誤
```bash
# 重新安裝依賴套件
pip install -r requirements.txt
```

### 2. 資料庫錯誤
```bash
# 刪除舊的資料庫檔案
rm line_data.db

# 重新啟動應用程式
python run.py
```

### 3. 權限問題
```bash
# 檢查檔案權限
ls -la *.py
ls -la templates/

# 修改權限（如果需要）
chmod +x *.py
```

### 4. 環境變數問題
確保 `.env` 檔案存在且包含正確的設定：
```bash
# 檢查 .env 檔案
cat .env

# 如果不存在，複製範例檔案
cp env_example.txt .env
```

## 啟動步驟

### 方法 1：使用安全啟動腳本（推薦）
```bash
python run.py
```

### 方法 2：手動啟動
```bash
# 1. 安裝依賴
pip install -r requirements.txt

# 2. 設定環境變數
cp env_example.txt .env
# 編輯 .env 檔案

# 3. 啟動應用程式
python app.py
```

### 方法 3：使用 Docker
```bash
# 建立並啟動容器
docker-compose up -d

# 查看日誌
docker-compose logs -f
```

## 測試步驟

1. **啟動應用程式**
   ```bash
   python run.py
   ```

2. **訪問測試頁面**
   ```
   http://127.0.0.1:5000/test
   ```

3. **檢查 API 端點**
   ```
   http://127.0.0.1:5000/api/statistics
   http://127.0.0.1:5000/api/mentioned-users
   ```

4. **訪問主頁面**
   ```
   http://127.0.0.1:5000/
   ```

## 日誌檢查

如果仍有問題，檢查應用程式日誌：
```bash
# 查看 Python 錯誤訊息
python run.py 2>&1 | tee app.log

# 檢查系統日誌
tail -f app.log
```

## 聯絡支援

如果以上方法都無法解決問題，請提供以下資訊：
1. 作業系統版本
2. Python 版本
3. 錯誤訊息截圖
4. 應用程式日誌 