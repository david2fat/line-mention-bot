# 🎨 Render 部署指南

## 🚀 快速開始

### 步驟 1: 準備工作
```bash
# 1. 確保已初始化 Git 倉庫
git init
git add .
git commit -m "Initial commit"

# 2. 設定環境變數
cp env_example.txt .env
# 編輯 .env 檔案，填入您的 LINE Bot 設定
```

### 步驟 2: 建立 GitHub 倉庫
1. 前往 [GitHub](https://github.com)
2. 建立新的倉庫
3. 將本地倉庫推送到 GitHub：
```bash
git remote add origin https://github.com/您的用戶名/您的倉庫名.git
git branch -M main
git push -u origin main
```

### 步驟 3: 部署到 Render

#### 方法 1: 使用網頁介面 (推薦)

1. **註冊 Render 帳戶**
   - 前往 [Render.com](https://render.com)
   - 使用 GitHub 帳戶註冊

2. **建立 Web Service**
   - 點擊 "New +" 按鈕
   - 選擇 "Web Service"
   - 連接您的 GitHub 倉庫

3. **設定服務**
   - **Name**: `line-mention-bot` (或您喜歡的名稱)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn wsgi:app`

4. **設定環境變數**
   在 "Environment Variables" 區段添加：
   ```
   LINE_CHANNEL_ACCESS_TOKEN = 您的_CHANNEL_ACCESS_TOKEN
   LINE_CHANNEL_SECRET = 您的_CHANNEL_SECRET
   FLASK_ENV = production
   FLASK_DEBUG = False
   ```

5. **建立服務**
   - 點擊 "Create Web Service"
   - 等待部署完成

#### 方法 2: 使用自動化腳本

```bash
# 執行自動部署腳本
python3 deploy_render.py
```

## 🔧 部署後設定

### 1. 獲取應用程式 URL
部署完成後，您會獲得一個 URL，例如：
```
https://line-mention-bot.onrender.com
```

### 2. 設定 LINE Bot Webhook
1. 前往 [LINE Developers Console](https://developers.line.biz/)
2. 選擇您的 Channel
3. 在 "Messaging API" 設定中
4. 設定 Webhook URL：
   ```
   https://line-mention-bot.onrender.com/webhook
   ```
5. 啟用 "Use webhook"

### 3. 測試系統
訪問您的應用程式：
```
https://line-mention-bot.onrender.com
```

## 📊 監控和管理

### 查看日誌
- 在 Render 儀表板中點擊您的服務
- 前往 "Logs" 標籤
- 查看即時日誌

### 重新部署
- 推送新的程式碼到 GitHub
- Render 會自動重新部署
- 或手動點擊 "Manual Deploy"

### 環境變數管理
- 在服務設定中編輯環境變數
- 修改後會自動重新部署

## 🛠️ 故障排除

### 常見問題

1. **部署失敗**
   - 檢查 `requirements.txt` 是否正確
   - 確認 Python 版本相容性
   - 查看部署日誌

2. **應用程式無法啟動**
   - 檢查 `wsgi.py` 檔案
   - 確認 `gunicorn` 已安裝
   - 查看啟動日誌

3. **環境變數問題**
   - 確認所有必要的環境變數已設定
   - 檢查變數名稱是否正確

4. **Webhook 驗證失敗**
   - 確認 HTTPS URL 正確
   - 檢查 LINE Bot 設定
   - 確認服務正在運行

### 日誌檢查
在 Render 儀表板中：
1. 點擊您的服務
2. 前往 "Logs" 標籤
3. 查看錯誤訊息

## 💡 最佳實踐

1. **使用環境變數**
   - 不要將敏感資訊寫入程式碼
   - 使用 Render 的環境變數功能

2. **監控資源使用**
   - 定期檢查免費額度使用情況
   - 監控應用程式效能

3. **備份資料**
   - 定期備份重要資料
   - 使用版本控制管理程式碼

4. **測試部署**
   - 部署前先在本地測試
   - 使用測試頁面驗證功能

## 🔄 更新部署

### 自動更新
```bash
# 修改程式碼後
git add .
git commit -m "Update"
git push origin main
# Render 會自動重新部署
```

### 手動更新
- 在 Render 儀表板中點擊 "Manual Deploy"

## 📈 效能優化

1. **啟用快取**
   - 使用 CDN 快取靜態資源
   - 實作資料庫查詢快取

2. **資料庫優化**
   - 使用索引優化查詢
   - 定期清理舊資料

3. **程式碼優化**
   - 減少不必要的 API 呼叫
   - 優化資料庫查詢

## 🆘 支援

如果遇到問題：
1. 檢查本指南的故障排除部分
2. 查看 Render 官方文件
3. 檢查應用程式日誌
4. 確認環境變數設定

## 📞 聯絡支援

- Render 支援：https://render.com/docs/help
- LINE Developers：https://developers.line.biz/docs/ 