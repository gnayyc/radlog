/**
 * RadLog License Verification API
 * Cloudflare Worker
 * 
 * Endpoints:
 * - GET /verify?email=xxx → 驗證 license
 * - POST /webhook/lemonsqueezy → 接收購買通知
 */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, X-Signature',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    try {
      // GET /verify?email=xxx
      if (path === '/verify' && request.method === 'GET') {
        const email = url.searchParams.get('email')?.toLowerCase().trim();
        
        if (!email) {
          return jsonResponse({ error: 'Missing email parameter' }, 400, corsHeaders);
        }

        // 檢查 KV 中是否有這個 email
        const license = await env.LICENSES.get(email);
        
        if (license) {
          const data = JSON.parse(license);
          return jsonResponse({
            valid: true,
            email: email,
            purchasedAt: data.purchasedAt,
          }, 200, corsHeaders);
        } else {
          return jsonResponse({
            valid: false,
            email: email,
          }, 200, corsHeaders);
        }
      }

      // POST /webhook/lemonsqueezy
      if (path === '/webhook/lemonsqueezy' && request.method === 'POST') {
        // 驗證 webhook 簽名
        const signature = request.headers.get('X-Signature');
        const rawBody = await request.text();
        
        // 可選：驗證簽名（生產環境建議啟用）
        if (env.WEBHOOK_SECRET && signature) {
          const encoder = new TextEncoder();
          const key = await crypto.subtle.importKey(
            'raw',
            encoder.encode(env.WEBHOOK_SECRET),
            { name: 'HMAC', hash: 'SHA-256' },
            false,
            ['sign']
          );
          const sig = await crypto.subtle.sign('HMAC', key, encoder.encode(rawBody));
          const expectedSig = Array.from(new Uint8Array(sig))
            .map(b => b.toString(16).padStart(2, '0'))
            .join('');
          
          if (signature !== expectedSig) {
            console.log('Invalid webhook signature');
            return jsonResponse({ error: 'Invalid signature' }, 401, corsHeaders);
          }
        }
        
        const body = JSON.parse(rawBody);
        
        // Lemon Squeezy order_created 事件
        // 支援 paid 狀態的訂單
        if (body.meta?.event_name === 'order_created') {
          const attrs = body.data?.attributes;
          const email = attrs?.user_email?.toLowerCase().trim();
          const orderId = body.data?.id;
          const orderNumber = attrs?.order_number;
          const status = attrs?.status;
          
          // 只處理已付款的訂單
          if (email && status === 'paid') {
            // 存入 KV
            await env.LICENSES.put(email, JSON.stringify({
              orderId: orderId,
              orderNumber: orderNumber,
              purchasedAt: new Date().toISOString(),
              source: 'lemonsqueezy',
              userName: attrs?.user_name || '',
            }));
            
            console.log(`License added for: ${email} (order #${orderNumber})`);
            return jsonResponse({ success: true, email, orderNumber }, 200, corsHeaders);
          }
        }
        
        return jsonResponse({ success: true, message: 'Event received' }, 200, corsHeaders);
      }

      // POST /admin/add — 手動新增 license（開發/測試用）
      if (path === '/admin/add' && request.method === 'POST') {
        const authHeader = request.headers.get('Authorization');
        if (authHeader !== `Bearer ${env.ADMIN_SECRET}`) {
          return jsonResponse({ error: 'Unauthorized' }, 401, corsHeaders);
        }

        const { email } = await request.json();
        if (!email) {
          return jsonResponse({ error: 'Missing email' }, 400, corsHeaders);
        }

        await env.LICENSES.put(email.toLowerCase().trim(), JSON.stringify({
          purchasedAt: new Date().toISOString(),
          source: 'manual',
        }));

        return jsonResponse({ success: true, email }, 200, corsHeaders);
      }

      // POST /admin/remove — 移除 license
      if (path === '/admin/remove' && request.method === 'POST') {
        const authHeader = request.headers.get('Authorization');
        if (authHeader !== `Bearer ${env.ADMIN_SECRET}`) {
          return jsonResponse({ error: 'Unauthorized' }, 401, corsHeaders);
        }

        const { email } = await request.json();
        if (!email) {
          return jsonResponse({ error: 'Missing email' }, 400, corsHeaders);
        }

        await env.LICENSES.delete(email.toLowerCase().trim());
        return jsonResponse({ success: true, email }, 200, corsHeaders);
      }

      // GET /admin/list — 列出所有 licenses
      if (path === '/admin/list' && request.method === 'GET') {
        const authHeader = request.headers.get('Authorization');
        if (authHeader !== `Bearer ${env.ADMIN_SECRET}`) {
          return jsonResponse({ error: 'Unauthorized' }, 401, corsHeaders);
        }

        const list = await env.LICENSES.list();
        const licenses = [];
        
        for (const key of list.keys) {
          const value = await env.LICENSES.get(key.name);
          licenses.push({
            email: key.name,
            ...JSON.parse(value),
          });
        }

        return jsonResponse({ licenses, count: licenses.length }, 200, corsHeaders);
      }

      return jsonResponse({ error: 'Not found' }, 404, corsHeaders);

    } catch (error) {
      console.error(error);
      return jsonResponse({ error: 'Internal server error' }, 500, corsHeaders);
    }
  },
};

function jsonResponse(data, status = 200, headers = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...headers,
    },
  });
}
