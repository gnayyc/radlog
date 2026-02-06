# 🔨 RadLog Windows 建置指南

## ⚠️ 現況
目前只有 Python 原始碼，還沒有 Windows .exe 執行檔。

## 🚀 最簡單的方法：GitHub Actions

已設定好自動建置，只需要：

### Step 1: 推送到 GitHub (5分鐘)
```bash
cd ~/codes/radlog

# 建立 GitHub repo（如果還沒有）
gh repo create radlog --private --source=. --push

# 或者手動
git remote add origin git@github.com:cyyang/radlog.git
git push -u origin main
```

### Step 2: 觸發建置
```bash
# 方法 A: 建立 tag（推薦）
git tag v1.0.0
git push origin v1.0.0

# 方法 B: 手動觸發
gh workflow run "Build Windows Executable"
```

### Step 3: 下載 .exe
```bash
# 等 2-3 分鐘後
gh run download --name RadLog-Windows

# 或從 GitHub Actions 頁面下載 artifact
```

### Step 4: 加入 Lemon Squeezy 包
```bash
cp RadLog.exe radlog-package/
cd radlog-package
zip -r ../radlog-v1.0.zip .
```

## 📋 Checklist
- [ ] 推送到 GitHub
- [ ] 建立 v1.0.0 tag
- [ ] 確認 Actions 成功
- [ ] 下載 RadLog.exe
- [ ] 打包上傳到 Lemon Squeezy

---

**預估時間：10 分鐘（首次需推送到 GitHub）**
