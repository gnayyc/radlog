# 🍋 RadLog Lemon Squeezy 設定完整指南

## 📋 準備資料

### 商店資訊
- **商店名稱:** CY Software
- **商店 URL:** cyyang
- **支援 Email:** cyyang@gmail.com (或你的信箱)
- **Logo:** 可選

### 產品資訊
- **名稱:** RadLog - Patient Tracker for Radiologists
- **價格:** $19.99
- **類型:** 軟體 / 一次買斷
- **描述:** 見下方完整文案

### 技術資訊
- **Webhook URL:** `https://radlog-license.cyyang.workers.dev/webhook/lemonsqueezy`
- **下載連結:** (待 GitHub Release 或其他托管)

---

## 🚀 執行步驟

### Step 1: 註冊 Lemon Squeezy (10分鐘)
1. 前往 https://lemonsqueezy.com
2. 點 "Get Started Free"
3. 用 Google 註冊 (建議用 cyyang@gmail.com)
4. 驗證 Email

### Step 2: 設定商店 (15分鐘)
1. Dashboard → Settings → Store
2. 填寫：
   - Store name: **CY Software**
   - Store URL: **cyyang** (會變成 cyyang.lemonsqueezy.com)
   - Support email: **你的信箱**
   - Currency: **USD**
   - Country: **Taiwan**

### Step 3: 連接付款 (15分鐘)
1. Settings → Payments
2. 選擇 **Stripe Express** (最簡單)
3. 填寫台灣稅務資訊
4. 設定提款到你的銀行帳戶

### Step 4: 建立 RadLog 產品 (20分鐘)
1. Products → **New Product**
2. 填寫：

**基本資訊:**
```
Name: RadLog - Patient Tracker for Radiologists
Slug: radlog
Description: (見下方完整文案)
```

**定價:**
```
Price: $19.99
Type: One-time
Currency: USD
```

**設定:**
```
Product type: Software
Download limit: 5 (允許重新下載)
License keys: 不勾選 (我們用 email 驗證)
```

3. **發布產品**

### Step 5: 設定 Webhook (15分鐘)
1. Settings → Webhooks → **Add webhook**
2. 填寫：
   - **Endpoint URL:** `https://radlog-license.cyyang.workers.dev/webhook/lemonsqueezy`
   - **Events:** 只勾選 `order_created`
   - **Signing secret:** 複製備用
3. **儲存**

4. 設定 Worker secret:
```bash
cd ~/codes/radlog/worker
echo "你的_signing_secret" | bunx wrangler secret put WEBHOOK_SECRET
```

### Step 6: 測試購買 (30分鐘)
1. 啟用 **Test Mode** (右上角開關)
2. 用測試卡號購買：
   - 卡號：`4242 4242 4242 4242`
   - 到期：未來任何日期
   - CVC：任何 3 位數
3. 確認：
   - [ ] Webhook 收到訂單
   - [ ] Cloudflare KV 寫入 license
   - [ ] 收到「購買成功」Email

### Step 7: 上線！(5分鐘)
1. 關閉 **Test Mode**
2. 產品設為 **Published**
3. 複製產品購買連結
4. 開始銷售！🎉

---

## 📝 產品文案 (複製貼上用)

### 產品描述
```
放射科醫師的快速病人記錄工具

⚡ 一個快捷鍵解決記錄問題
按 Ctrl+Shift+R 叫出小視窗，輸入「病歷號, 分類, 備註」，瞬間完成。

📊 自動同步到 Google Sheet
不用開 Excel、不用找檔案。資料直接存到你的 Google Sheet，手機也能看。

🔐 安全可靠
資料存在你自己的 Google 帳號，我們無法存取你的病歷資料。

💰 一次買斷 $19.99
永久使用，免費更新，無訂閱費，無廣告。

支援 Windows 10/11，離線可用，多台電腦同步。
14 天內不滿意無條件退款。
```

### 購買後 Email
```
🎉 感謝購買 RadLog！

下載連結：[待提供]

使用步驟：
1. 下載並安裝 RadLog.exe
2. 用購買時的 Google 帳號登入
3. 按 Ctrl+Shift+R 開始使用！

有問題請回信，我們會盡快處理。

祝工作順利！
CY Software
```

---

## 💰 收益計算

**每筆 $19.99 訂單:**
- Lemon Squeezy 費用: 5% + $0.50 = $1.50
- 實際收入: $19.99 - $1.50 = **$18.49**

**目標:**
- 第一週：1-2 筆訂單 ($18-37)
- 第一個月：10 筆訂單 ($185)
- 後續：口碑推薦 + 同事轉介

---

## ⏰ 預估時間表

- **13:00-14:00** 註冊 + 商店設定
- **14:00-14:30** 建立產品 + 文案
- **14:30-15:00** Webhook + 技術整合
- **15:00-15:30** 測試購買流程
- **15:30-16:00** 上線 + 第一筆銷售準備

**目標：下午 4 點第一個付費產品上線！** 🚀