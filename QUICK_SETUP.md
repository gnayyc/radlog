# 🚀 RadLog 快速上線指南

**目標：今天讓 RadLog 開始賺錢！**

## ⚠️ 前置條件：建置 Windows .exe

**目前只有原始碼，還需要建置執行檔！**

```bash
# 1. 推送到 GitHub
cd ~/codes/radlog
gh repo create radlog --private --source=. --push

# 2. 建立 tag 觸發自動建置
git tag v1.0.0
git push origin v1.0.0

# 3. 等 3 分鐘，下載建置好的 .exe
gh run download --name RadLog-Windows
mv RadLog.exe radlog-package/
```

詳見：`BUILD_WINDOWS.md`

---

## ⚡ Step 1: Lemon Squeezy 註冊 (5分鐘)

1. 前往：https://lemonsqueezy.com
2. 點 **Sign up** → 輸入 Email/密碼
3. 驗證 Email
4. 選擇 **Individual** 帳號類型

## ⚡ Step 2: 建立商店 (2分鐘)

1. Dashboard → **Create Store**
2. 商店名稱：`CY Medical Tools`
3. URL：`cy-medical-tools` 
4. 其他設定保持預設

## ⚡ Step 3: 建立 RadLog 產品 (5分鐘)

**基本設定：**
- Product Type: **Digital Download**
- Name: `RadLog - Patient Tracker for Radiologists`
- Price: `$19.99`
- Category: `Software`

**描述（直接貼上）：**
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

💻 Requirements: Windows 10/11, Google account

🚀 Buy once, use forever!
```

**上傳檔案：**
```bash
cd ~/codes/radlog
zip -r radlog-v1.0.zip radlog-package/
```
上傳 `radlog-v1.0.zip`

## ⚡ Step 4: 設定 Webhook (2分鐘)

1. Settings → **Webhooks**
2. 新增 Webhook：
   - URL: `https://radlog-license.cyyang.workers.dev/webhook/lemonsqueezy`
   - Events: `order_created` ✅
   - Secret: （保留空白）

## ⚡ Step 5: 測試 & 上線 (1分鐘)

1. **Test Mode 購買：**
   - 產品頁面 → **Buy in test mode**
   - 完成測試購買
   - 確認收到授權 Email

2. **正式上線：**
   - Product → **Settings** → 關閉 Test mode
   - 點 **Publish** 

3. **取得購買連結：**
   - 複製產品 URL
   - **開始賺錢！** 🎉

---

## 📧 預期收到的授權 Email 格式

```
Subject: RadLog License Key

您好，

感謝購買 RadLog！以下是您的授權資訊：

授權 Email: [購買者email]
產品: RadLog - Patient Tracker for Radiologists
授權狀態: 有效

請下載附件並執行 RadLog.exe 開始使用。

首次啟動時請輸入您的購買 Email 進行授權驗證。

技術支援: cyyang@example.com
```

---

## 🎯 完成後下一步

1. **分享購買連結**（Discord、醫師社群）
2. **收集使用者回饋**
3. **規劃 v2 功能**（語音輸入？iPad 版？）

**預估首月收入：10 個銷量 × $18.49 = $184.9** 💰