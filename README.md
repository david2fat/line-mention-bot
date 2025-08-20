# LINE @ 提醒系統

這是一個用於整合 LINE 群組中被 @ 提及人員資料的前台系統。

## 功能特色

- 🔔 自動偵測 LINE 群組中的 @ 提及
- 📊 即時統計資料顯示
- 👥 被提及人員資料整合
- 📈 最常被提及使用者排行
- 🎨 現代化響應式前端介面
- 🔄 自動資料更新

## 系統架構

```
LINE 群組 → LINE Bot → Webhook → Flask 後端 → SQLite 資料庫
                                    ↓
                              前端介面顯示
```

## 安裝步驟

### 1. 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 2. 設定 LINE Bot

1. 前往 [LINE Developers Console](https://developers.line.biz/)
2. 建立新的 Channel (Messaging API)
3. 取得 Channel Access Token 和 Channel Secret
4. 複製 `env_example.txt` 為 `.env` 並填入您的設定：

```bash
cp env_example.txt .env
```

編輯 `.env` 檔案：
```
LINE_CHANNEL_ACCESS_TOKEN=您的_CHANNEL_ACCESS_TOKEN
LINE_CHANNEL_SECRET=您的_CHANNEL_SECRET
```

### 3. 設定 Webhook URL

在 LINE Developers Console 中設定 Webhook URL：
```
https://您的網域/webhook
```

### 4. 啟動應用程式

```bash
python app.py
```

應用程式將在 `http://localhost:5000` 啟動。

## 使用方式

### 在 LINE 群組中使用

1. 將您的 LINE Bot 加入群組
2. 當有人在群組中使用 @ 提及其他人時，Bot 會自動記錄
3. Bot 會回覆確認訊息

### 查看資料

1. 開啟瀏覽器前往 `http://localhost:5000`
2. 查看統計資料和最近提及記錄
3. 資料會每 30 秒自動更新

## API 端點

- `GET /` - 前台首頁
- `POST /webhook` - LINE Bot Webhook
- `GET /api/mentioned-users` - 獲取所有提及記錄
- `GET /api/statistics` - 獲取統計資料

## 資料庫結構

```sql
CREATE TABLE mentioned_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    user_name TEXT,
    group_id TEXT,
    message TEXT,
    mentioned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    message_id TEXT
);
```

## 部署建議

### 本地開發
```bash
python app.py
```

### 生產環境部署
建議使用以下工具進行部署：
- **Heroku**: 支援 Python 應用程式
- **AWS EC2**: 自架伺服器
- **Google Cloud Platform**: 雲端服務
- **Docker**: 容器化部署

### 使用 ngrok 進行本地測試
```bash
# 安裝 ngrok
brew install ngrok  # macOS
# 或下載 ngrok 並設定

# 啟動隧道
ngrok http 5000

# 使用提供的 HTTPS URL 作為 Webhook URL
```

## 注意事項

1. **LINE Bot 權限**: 確保 Bot 有權限讀取群組訊息
2. **Webhook 安全性**: 生產環境請使用 HTTPS
3. **資料庫備份**: 定期備份 SQLite 資料庫
4. **速率限制**: 注意 LINE API 的呼叫限制

## 故障排除

### 常見問題

1. **Webhook 驗證失敗**
   - 檢查 Channel Secret 是否正確
   - 確認 Webhook URL 格式

2. **Bot 無法接收訊息**
   - 確認 Bot 已加入群組
   - 檢查群組設定是否允許 Bot 讀取訊息

3. **前端無法載入資料**
   - 檢查後端服務是否正常運行
   - 確認 API 端點是否可存取

## 技術棧

- **後端**: Python Flask
- **前端**: HTML5, CSS3, JavaScript, Bootstrap 5
- **資料庫**: SQLite
- **LINE Bot**: LINE Messaging API
- **部署**: 支援多種雲端平台

## 授權

MIT License

## 支援

如有問題或建議，請提交 Issue 或 Pull Request。 