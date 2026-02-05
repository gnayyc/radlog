# 🍋 RadLog - Lemon Squeezy 產品設定指南

## 產品資訊

### 基本設定
- **產品名稱：** RadLog - 放射科病人快速追蹤工具
- **價格：** $19.99 USD (一次買斷)
- **產品類型：** Digital Download
- **分類：** Healthcare / Medical Software

### 產品描述 (中文)

```
🏥 RadLog - 專為放射科醫師設計的病人記錄神器

⚡ 全局快捷鍵 (Ctrl+Shift+R)，秒速記錄
📝 智能解析：病歷號, 分類, 備註一行搞定
📊 自動同步 Google Sheet，永不遺失
🔐 Google 授權綁定，安全可靠

完美整合你的工作流程，提升效率 10 倍！

✨ 功能亮點
- 病歷號快速輸入與分類
- 自動時間戳記
- Google Sheets 雲端同步
- 自訂分類標籤
- Windows 原生應用

🎯 適用對象
- 放射科醫師
- 臨床醫師  
- 醫學影像分析師

💻 系統需求
- Windows 10/11
- Google 帳號
- 網際網路連線

🚀 立即購買，永久使用！
```

### 產品描述 (English)

```
🏥 RadLog - Patient Tracking Tool for Radiologists

⚡ Global hotkey (Ctrl+Shift+R) for instant access
📝 Smart parsing: Patient ID, category, notes in one line
📊 Auto-sync to Google Sheets, never lose data
🔐 Google OAuth secure binding

10x faster workflow for busy radiologists!

✨ Key Features
- Quick patient ID input with smart categorization
- Automatic timestamps
- Real-time Google Sheets sync
- Custom category tags
- Native Windows app

🎯 Perfect for
- Radiologists
- Clinical physicians
- Medical imaging analysts

💻 Requirements
- Windows 10/11
- Google account
- Internet connection

🚀 Buy once, use forever!
```

## Webhook 設定

### Webhook URL
```
https://radlog-license.cyyang.workers.dev/webhook/lemonsqueezy
```

### 觸發事件
- ✅ `order_created` - 訂單建立時自動發送授權
- ✅ `order_refunded` - 退款時撤銷授權 (可選)

### 測試 Webhook
```bash
curl -X POST https://radlog-license.cyyang.workers.dev/webhook/lemonsqueezy \
  -H "Content-Type: application/json" \
  -d '{
    "meta": {
      "event_name": "order_created"
    },
    "data": {
      "attributes": {
        "user_email": "test@example.com",
        "status": "paid"
      }
    }
  }'
```

## 下載文件準備

### 主要下載檔案
1. **RadLog.exe** (Windows 執行檔)
2. **安裝指南.pdf** (中文)
3. **Installation Guide.pdf** (English)
4. **Google Sheet 範本** (連結)

### 檔案結構
```
radlog-package/
├── RadLog.exe                 # 主程式
├── README.txt                # 快速開始指南
├── 安裝指南.pdf               # 詳細中文指南
├── Installation_Guide.pdf     # 詳細英文指南
└── LICENSE.txt               # MIT License
```

## 後續步驟

### 1. Lemon Squeezy 帳號設定
- 到 lemonsqueezy.com 註冊商家帳號
- 設定收款資訊 (銀行帳戶/PayPal)
- 驗證身份 (可能需要護照/身分證)

### 2. 建立產品
- 選擇 "Digital Download"
- 上傳產品檔案 (zip 打包)
- 設定價格 $19.99
- 填入上述產品描述

### 3. 設定 Webhook
- Dashboard → Settings → Webhooks
- 新增 webhook URL
- 選擇 `order_created` 事件
- 測試 webhook 接收

### 4. 測試購買流程
```bash
# 建立測試產品
# 完成測試購買
# 確認 email 收到授權
# 測試 RadLog.exe 授權驗證
```

### 5. 正式上線
- 公開產品頁面
- 分享購買連結
- 開始賺錢！💰

## 重要檔案位置

- **API 代碼：** `~/codes/radlog/worker/index.js`
- **Windows 程式：** `~/codes/radlog/app/RadLog.exe`
- **設定檔：** `~/codes/radlog/worker/wrangler.toml`

## 銷售分析

- **成本：** $0 (運行成本極低)
- **定價：** $19.99
- **平台費：** 5% + $0.50 = $1.50
- **淨收入：** $18.49 per sale
- **目標：** 每月 10 個銷量 = $184.9

---

🎯 **目標：今天完成 Lemon Squeezy 設定，明天開始銷售！**