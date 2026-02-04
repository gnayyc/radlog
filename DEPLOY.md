# RadLog 部署指南

## 總覽

```
1. Cloudflare Workers（授權 API）     ~15 分鐘
2. Google Cloud（OAuth）             ~20 分鐘
3. Lemon Squeezy（收款）             ~10 分鐘
4. Windows 打包測試                   ~10 分鐘
```

---

## Step 1: Cloudflare Workers

### 1.1 註冊/登入 Cloudflare

1. 到 https://dash.cloudflare.com
2. 註冊或登入

### 1.2 安裝 Wrangler CLI

```bash
npm install -g wrangler
wrangler login
```

### 1.3 建立 KV Namespace

```bash
cd ~/codes/radlog/worker
wrangler kv:namespace create LICENSES
```

輸出類似：
```
{ binding = "LICENSES", id = "abc123..." }
```

**複製這個 id**，貼到 `wrangler.toml`：

```toml
[[kv_namespaces]]
binding = "LICENSES"
id = "abc123..."  # ← 貼這裡
```

### 1.4 設定 Admin Secret

```bash
wrangler secret put ADMIN_SECRET
```

輸入一個隨機密碼（記下來，之後管理用）

### 1.5 部署

```bash
wrangler deploy
```

成功後會顯示 URL，類似：
```
https://radlog-license.YOUR_SUBDOMAIN.workers.dev
```

**記下這個 URL**，之後要用。

### 1.6 測試

```bash
# 手動新增測試 license
curl -X POST https://radlog-license.xxx.workers.dev/admin/add \
  -H "Authorization: Bearer YOUR_ADMIN_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"email": "your@gmail.com"}'

# 驗證
curl "https://radlog-license.xxx.workers.dev/verify?email=your@gmail.com"
# 應該回傳 {"valid": true, ...}
```

---

## Step 2: Google Cloud OAuth

### 2.1 建立專案

1. 到 https://console.cloud.google.com
2. 建立新專案：`RadLog`

### 2.2 啟用 API

1. 到 APIs & Services → Library
2. 搜尋並啟用：
   - **Google Sheets API**
   - **Google OAuth2 API**（可能叫 People API 或 OAuth2）

### 2.3 設定 OAuth 同意畫面

1. APIs & Services → OAuth consent screen
2. 選擇 **External**
3. 填寫：
   - App name: `RadLog`
   - User support email: 你的 email
   - Developer contact: 你的 email
4. Scopes：新增 `https://www.googleapis.com/auth/spreadsheets`
5. Test users：新增你的 email（測試階段）

### 2.4 建立 OAuth Credentials

1. APIs & Services → Credentials
2. Create Credentials → **OAuth client ID**
3. Application type: **Desktop app**
4. Name: `RadLog Desktop`
5. 下載 JSON

### 2.5 放置 credentials

把下載的 JSON 重新命名為 `credentials.json`，放到：
- Windows: `C:\Users\你的用戶名\.radlog\credentials.json`
- Mac: `~/.radlog/credentials.json`

---

## Step 3: Lemon Squeezy

### 3.1 註冊

1. 到 https://lemonsqueezy.com
2. 註冊帳號

### 3.2 建立 Store

1. 建立 Store（商店）
2. 設定名稱、描述

### 3.3 建立產品

1. Products → New Product
2. 設定：
   - Name: `RadLog - Patient Tracker for Radiologists`
   - Price: `$19.99`（一次買斷）
   - 描述：簡短介紹功能

### 3.4 設定 Webhook

1. Settings → Webhooks
2. New Webhook：
   - URL: `https://radlog-license.xxx.workers.dev/webhook/lemonsqueezy`
   - Events: 勾選 `order_created`
3. 儲存

### 3.5 取得購買連結

產品頁會有一個購買連結，類似：
```
https://your-store.lemonsqueezy.com/checkout/buy/xxx
```

**更新到 `radlog.py`** 中的購買按鈕 URL。

---

## Step 4: Windows 打包

### 4.1 在 Windows 電腦上

```cmd
cd radlog\app
pip install -r requirements.txt
```

### 4.2 更新設定

編輯 `radlog.py`，更新：

```python
LICENSE_API = 'https://radlog-license.YOUR_SUBDOMAIN.workers.dev'
```

以及購買連結。

### 4.3 打包

```cmd
build.bat
```

或手動：
```cmd
pyinstaller --onefile --windowed --name RadLog radlog.py
```

### 4.4 測試

1. 執行 `dist\RadLog.exe`
2. 用 Google 帳號登入
3. 設定 Spreadsheet ID
4. 測試記錄功能

---

## Step 5: 發布

### 5.1 準備

- [ ] Worker 部署完成
- [ ] OAuth 設定完成
- [ ] Lemon Squeezy 產品上架
- [ ] Windows .exe 打包完成
- [ ] 測試購買流程

### 5.2 上架

1. 把 `RadLog.exe` 上傳到某處（GitHub Releases、Google Drive）
2. 在 Lemon Squeezy 產品頁加上下載連結
3. 發布！

---

## 常見問題

### Q: OAuth 說「App not verified」？

這是正常的（測試階段）。點 Advanced → Go to RadLog (unsafe)。

正式發布前可以申請 Google 驗證，但需要隱私政策等文件。

### Q: 打包後 .exe 很大？

PyInstaller 會包含整個 Python runtime，約 30-50MB 是正常的。

可以用 `--exclude-module` 排除不需要的模組來縮小。

### Q: 如何手動新增 license？

```bash
curl -X POST https://radlog-license.xxx.workers.dev/admin/add \
  -H "Authorization: Bearer YOUR_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@gmail.com"}'
```

---

## 檢查清單

```
[ ] Cloudflare Worker 部署
[ ] KV Namespace 建立
[ ] Admin Secret 設定
[ ] Google Cloud 專案建立
[ ] Sheets API 啟用
[ ] OAuth credentials 下載
[ ] Lemon Squeezy 產品建立
[ ] Webhook 設定
[ ] radlog.py 更新 URL
[ ] Windows 打包測試
[ ] 購買流程測試
```
