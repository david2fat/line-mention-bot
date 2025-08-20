# ☁️ 雲端部署指南

## 🚀 快速部署選項

### 1. Heroku (推薦 - 免費)
```bash
python deploy_heroku.py
```

### 2. Railway (推薦 - 免費)
```bash
python deploy_railway.py
```

### 3. Render (推薦 - 免費)
```bash
python deploy_render.py
```

### 4. Vercel (推薦 - 免費)
```bash
python deploy_vercel.py
```

## 📋 部署前準備

### 1. 設定 LINE Bot
1. 前往 [LINE Developers Console](https://developers.line.biz/)
2. 建立新的 Channel (Messaging API)
3. 取得 Channel Access Token 和 Channel Secret
4. 編輯 `.env` 檔案：

```bash
cp env_example.txt .env
```

編輯 `.env` 檔案：
```
LINE_CHANNEL_ACCESS_TOKEN=您的_CHANNEL_ACCESS_TOKEN
LINE_CHANNEL_SECRET=您的_CHANNEL_SECRET
```

### 2. 初始化 Git 倉庫
```bash
git init
git add .
git commit -m "Initial commit"
```

## 🌟 Heroku 部署 (最簡單)

### 自動部署
```bash
# 1. 安裝 Heroku CLI
# macOS: brew install heroku/brew/heroku
# Windows: 下載安裝程式

# 2. 登入 Heroku
heroku login

# 3. 執行自動部署腳本
python deploy_heroku.py
```

### 手動部署
```bash
# 1. 建立 Heroku 應用程式
heroku create your-app-name

# 2. 設定環境變數
heroku config:set LINE_CHANNEL_ACCESS_TOKEN=您的_TOKEN
heroku config:set LINE_CHANNEL_SECRET=您的_SECRET
heroku config:set FLASK_ENV=production

# 3. 部署
git push heroku main

# 4. 開啟應用程式
heroku open
```

## 🚄 Railway 部署

### 自動部署
```bash
# 1. 安裝 Railway CLI
npm install -g @railway/cli

# 2. 執行自動部署腳本
python deploy_railway.py
```

### 手動部署
```bash
# 1. 登入 Railway
railway login

# 2. 初始化專案
railway init

# 3. 設定環境變數
railway variables set LINE_CHANNEL_ACCESS_TOKEN=您的_TOKEN
railway variables set LINE_CHANNEL_SECRET=您的_SECRET

# 4. 部署
railway deploy
```

## 🎨 Render 部署

### 自動部署
```bash
# 1. 執行自動部署腳本
python deploy_render.py

# 2. 按照腳本指示完成設定
```

### 手動部署
1. 前往 [Render.com](https://render.com)
2. 註冊並登入
3. 點擊 "New +" → "Web Service"
4. 連接 GitHub 倉庫
5. 設定環境變數
6. 點擊 "Create Web Service"

## ⚡ Vercel 部署

### 自動部署
```bash
# 1. 安裝 Vercel CLI
npm install -g vercel

# 2. 執行自動部署腳本
python deploy_vercel.py
```

### 手動部署
```bash
# 1. 登入 Vercel
vercel login

# 2. 部署
vercel --prod
```

## 🔧 部署後設定

### 1. 設定 LINE Bot Webhook
部署完成後，您會獲得一個 HTTPS URL，例如：
```
https://your-app-name.herokuapp.com
```

在 LINE Developers Console 中設定 Webhook URL：
```
https://your-app-name.herokuapp.com/webhook
```

### 2. 測試系統
訪問您的應用程式：
```
https://your-app-name.herokuapp.com
```

### 3. 檢查日誌
```bash
# Heroku
heroku logs --tail

# Railway
railway logs

# Render
# 在 Render 儀表板查看日誌
```

## 📊 各平台比較

| 平台 | 免費額度 | 部署難度 | 穩定性 | 推薦度 |
|------|----------|----------|--------|--------|
| Heroku | 有限 | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Railway | 充足 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Render | 充足 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Vercel | 充足 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## 🛠️ 故障排除

### 常見問題

1. **環境變數未設定**
   - 檢查 `.env` 檔案是否正確
   - 確認雲端平台的環境變數設定

2. **部署失敗**
   - 檢查 `requirements.txt` 是否正確
   - 確認 Python 版本相容性

3. **Webhook 驗證失敗**
   - 確認 HTTPS URL 正確
   - 檢查 LINE Bot 設定

4. **應用程式無法啟動**
   - 檢查日誌檔案
   - 確認端口設定正確

### 日誌檢查
```bash
# Heroku
heroku logs --tail

# Railway
railway logs

# Render
# 在儀表板查看

# Vercel
vercel logs
```

## 🔄 更新部署

### 自動更新
```bash
# 修改程式碼後
git add .
git commit -m "Update"
git push origin main

# 各平台會自動重新部署
```

### 手動更新
```bash
# Heroku
git push heroku main

# Railway
railway deploy

# Render
# 自動更新

# Vercel
vercel --prod
```

## 💡 最佳實踐

1. **使用環境變數**：不要將敏感資訊寫入程式碼
2. **定期備份**：重要資料要定期備份
3. **監控日誌**：定期檢查應用程式日誌
4. **測試部署**：部署前先在本地測試
5. **版本控制**：使用 Git 管理程式碼版本

## 🆘 支援

如果遇到問題：
1. 檢查本指南的故障排除部分
2. 查看各平台的官方文件
3. 檢查應用程式日誌
4. 確認環境變數設定 