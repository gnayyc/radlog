# RadLog 上架檢查清單

## 🔧 技術準備

### Cloudflare Workers
- [ ] `wrangler login` 完成
- [ ] KV Namespace 建立，ID 填入 `wrangler.toml`
- [ ] `wrangler secret put ADMIN_SECRET` 設定
- [ ] `wrangler deploy` 成功
- [ ] 測試 `/verify` 端點

### Google Cloud
- [ ] 建立專案「RadLog」
- [ ] 啟用 Sheets API
- [ ] OAuth consent screen 設定完成
- [ ] Desktop OAuth credentials 下載
- [ ] `credentials.json` 測試可用

### 打包
- [ ] 更新 `radlog.py` 中的 `LICENSE_API` URL
- [ ] Windows: `git tag v1.0.0 && git push origin v1.0.0`
- [ ] GitHub Actions 打包成功
- [ ] 下載 `RadLog.exe` 測試可用

---

## 💰 金流準備

### Lemon Squeezy
- [ ] 註冊帳號
- [ ] 連結 PayPal
- [ ] 建立產品
  - Name: `RadLog - Patient Tracker for Radiologists`
  - Price: `$19.99`
  - 描述: 複製 `LANDING.md` 內容
- [ ] 設定 Webhook
  - URL: `https://你的worker/webhook/lemonsqueezy`
  - Events: `order_created`
- [ ] 取得購買連結

---

## 📦 上架準備

### 下載頁面
- [ ] 上傳 `RadLog.exe` 到某處（GitHub Releases 或 Google Drive）
- [ ] 準備下載連結

### 產品頁面
- [ ] 標題、描述填好
- [ ] 價格設定正確
- [ ] 購買後自動寄送下載連結

---

## 🧪 測試

### 購買流程
- [ ] 用測試帳號購買（Lemon Squeezy test mode）
- [ ] 確認 Webhook 收到
- [ ] 確認 License 加入 KV
- [ ] 確認收到下載連結

### 使用流程
- [ ] 下載 exe
- [ ] Google 登入成功
- [ ] License 驗證通過
- [ ] 記錄成功寫入 Sheet
- [ ] 快捷鍵正常

---

## 🚀 上線

- [ ] 關閉 test mode
- [ ] 產品設為公開
- [ ] 發布到社群（Reddit、Twitter）
- [ ] 通知主人的放射科同事

---

## 上線後

- [ ] 監控第一筆訂單
- [ ] 回覆客戶問題
- [ ] 收集反饋
- [ ] 規劃 v1.1 功能
