# 🍋 Lemon Squeezy 完整設定指南

## Step 1: 註冊帳號
1. 前往 https://lemonsqueezy.com
2. 點擊 "Get Started Free"
3. 用 Google 或 Email 註冊
4. 驗證 Email

## Step 2: 設定商店
1. Dashboard → Settings → Store
2. 填寫商店資訊：
   - **Store name:** CY Software (或你喜歡的名稱)
   - **Store URL:** cyyang (會變成 cyyang.lemonsqueezy.com)
   - **Support email:** 你的 email
3. 上傳 Logo（可選）

## Step 3: 設定付款
1. Settings → Payments
2. 連接 Stripe 帳號（Lemon Squeezy 用 Stripe 處理付款）
3. 填寫稅務資訊（台灣選 Taiwan）
4. 設定提款帳戶（銀行帳號或 PayPal）

## Step 4: 建立 RadLog 產品
1. Products → Create Product
2. 填寫：

**基本資訊：**
- **Name:** RadLog - Patient Tracker for Radiologists
- **Description:** 
```
放射科醫師的快速病人記錄工具。
按 Ctrl+Shift+R 叫出小視窗，輸入「病歷號, 分類, 備註」，自動同步到你的 Google Sheet。
不再需要切換視窗、開 Excel。一次買斷，永久使用。
```

**定價：**
- **Price:** $19.99
- **Payment type:** One-time (一次買斷)

**交付：**
- **Product type:** Software
- **Files:** 上傳 RadLog 安裝程式（或提供下載連結）
- **License keys:** 不需要（我們用 email 驗證）

3. 點擊 "Publish"

## Step 5: 設定 Webhook
1. Settings → Webhooks → Add Webhook
2. 填寫：
   - **URL:** `https://radlog-license.cyyang.workers.dev/webhook/lemonsqueezy`
   - **Events:** 勾選 `order_created`
3. 複製 **Signing Secret**
4. 回到終端機執行：
```bash
cd ~/codes/radlog/worker
echo "你的_signing_secret" | bunx wrangler secret put WEBHOOK_SECRET
```

## Step 6: 測試購買流程
1. Lemon Squeezy 有 Test Mode
2. Settings → Test Mode → Enable
3. 用測試卡號購買：`4242 4242 4242 4242`
4. 確認：
   - [ ] Webhook 有收到
   - [ ] KV 有寫入 license
   - [ ] RadLog app 可以驗證

## Step 7: 上線！
1. 關閉 Test Mode
2. 分享產品連結
3. 等收錢 💰

---

## 📊 費用計算

| 項目 | 費率 |
|------|------|
| Lemon Squeezy | 5% + $0.50 |
| Stripe 處理費 | 包含在上面 |

**$19.99 產品實收：**
- 費用: $19.99 × 5% + $0.50 = $1.50
- 實收: $19.99 - $1.50 = **$18.49**

## 🔗 有用連結
- Lemon Squeezy Dashboard: https://app.lemonsqueezy.com
- Webhook 文件: https://docs.lemonsqueezy.com/api/webhooks
- API 文件: https://docs.lemonsqueezy.com/api
