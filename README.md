# 🏥 RadLog

快速病人記錄工具 for 放射科醫師

## 功能

- ⌨️ 全局快捷鍵快速叫出（Ctrl+Shift+R）
- 📝 快速輸入：`病歷號, 分類, 備註` 一行搞定
- 📊 自動同步 Google Sheet
- 🔐 Google 帳號授權（購買後綁定）

## 安裝

### Windows

1. 下載 `RadLog.exe`
2. 執行，用 Google 帳號登入
3. 設定你的 Google Sheet ID
4. 開始使用！

### 首次設定

1. **建立 Google Sheet**
   - 開新 Sheet，第一行標題：`時間 | 病歷號 | 分類 | 備註`
   - 複製 URL 中的 Spreadsheet ID

2. **設定 RadLog**
   - 點「設定」
   - 貼上 Spreadsheet ID
   - 設定你的分類（預設：tumor, vascular, infection, trauma, other）

3. **設定 Google OAuth**（開發者）
   - 到 Google Cloud Console 建立 OAuth 2.0 credentials
   - 下載 `credentials.json` 放到 `~/.radlog/`

## 使用

### 快速輸入

```
1234567, tumor, liver mass suspect HCC
```

自動解析為：
- 病歷號: 1234567
- 分類: tumor
- 備註: liver mass suspect HCC
- 時間: (自動)

### 快捷鍵

- `Ctrl+Shift+R` — 叫出 RadLog
- `Enter` — 送出快速輸入

## 專案結構

```
radlog/
├── app/                 # Windows 應用程式
│   ├── radlog.py       # 主程式
│   ├── requirements.txt
│   └── build.bat       # 打包腳本
├── worker/             # Cloudflare Workers（授權 API）
│   ├── index.js
│   ├── wrangler.toml
│   └── README.md
└── README.md
```

## 授權

購買後，用購買時的 Google 帳號登入即可使用。

購買連結：[Lemon Squeezy](https://YOUR_URL)

## 定價

**$19.99** 一次買斷，永久使用。

## License

MIT
