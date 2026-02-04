# RadLog 上線步驟

## ✅ 已完成
1. [x] Cloudflare Worker 部署完成
2. [x] KV namespace 建立完成
3. [x] API 測試通過

## 🔗 API 資訊
- **URL:** `https://radlog-license.cyyang.workers.dev`
- **ADMIN_SECRET:** `360797e7e5791d9ae917fc45ef749e02`

## 📋 待完成：Lemon Squeezy 設定

### 1. 建立產品
1. 登入 https://app.lemonsqueezy.com
2. Products → Create Product
3. 填入：
   - **Name:** RadLog - Patient Tracker for Radiologists
   - **Price:** $19.99 (One-time)
   - **Description:** (見 LANDING.md)

### 2. 設定 Webhook
1. Settings → Webhooks → Add Webhook
2. **URL:** `https://radlog-license.cyyang.workers.dev/webhook/lemonsqueezy`
3. **Events:** 勾選 `order_created`
4. **Signing Secret:** 複製下來

### 3. 設定 Worker 的 Webhook Secret（可選但建議）
```bash
cd ~/codes/radlog/worker
echo "YOUR_SIGNING_SECRET" | bunx wrangler secret put WEBHOOK_SECRET
```

### 4. 測試流程
1. 建立測試訂單（Lemon Squeezy 有 test mode）
2. 確認 webhook 收到
3. 確認 KV 有寫入 license
4. 用 Windows RadLog 驗證 license

## 🖥️ Windows 端設定
RadLog Windows app 需要改成連到：
`https://radlog-license.cyyang.workers.dev/verify?email=EMAIL`
