# RadLog License API

Cloudflare Worker 驗證 RadLog license。

## 部署步驟

### 1. 安裝 Wrangler CLI
```bash
npm install -g wrangler
wrangler login
```

### 2. 建立 KV Namespace
```bash
wrangler kv:namespace create LICENSES
# 複製輸出的 id 到 wrangler.toml
```

### 3. 設定 Admin Secret
```bash
wrangler secret put ADMIN_SECRET
# 輸入一個隨機字串作為 admin API 密碼
```

### 4. 部署
```bash
wrangler deploy
```

## API 端點

### 驗證 License
```
GET /verify?email=user@example.com

Response (有效):
{
  "valid": true,
  "email": "user@example.com",
  "purchasedAt": "2026-02-04T06:00:00.000Z"
}

Response (無效):
{
  "valid": false,
  "email": "user@example.com"
}
```

### Lemon Squeezy Webhook
```
POST /webhook/lemonsqueezy
Content-Type: application/json

(Lemon Squeezy 會自動發送 order_created 事件)
```

### Admin: 手動新增 License
```
POST /admin/add
Authorization: Bearer YOUR_ADMIN_SECRET
Content-Type: application/json

{"email": "user@example.com"}
```

### Admin: 列出所有 Licenses
```
GET /admin/list
Authorization: Bearer YOUR_ADMIN_SECRET
```

## Lemon Squeezy 設定

1. 到 Lemon Squeezy Dashboard → Settings → Webhooks
2. 新增 Webhook URL: `https://radlog-license.YOUR_SUBDOMAIN.workers.dev/webhook/lemonsqueezy`
3. 選擇事件: `order_created`
4. 儲存

## 測試

```bash
# 手動新增測試 license
curl -X POST https://radlog-license.xxx.workers.dev/admin/add \
  -H "Authorization: Bearer YOUR_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'

# 驗證
curl "https://radlog-license.xxx.workers.dev/verify?email=test@example.com"
```
