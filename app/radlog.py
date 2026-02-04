#!/usr/bin/env python3
"""
RadLog - 快速病人記錄工具
Windows App with Global Hotkey
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import webbrowser
from datetime import datetime
from pathlib import Path
import threading

# Google API
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import requests

# 設定
CONFIG_DIR = Path.home() / '.radlog'
CONFIG_FILE = CONFIG_DIR / 'config.json'
TOKEN_FILE = CONFIG_DIR / 'token.json'
CREDENTIALS_FILE = CONFIG_DIR / 'credentials.json'

# Google Sheets API scope
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# License API
LICENSE_API = 'https://radlog-license.YOUR_SUBDOMAIN.workers.dev'  # 部署後替換


class RadLogApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('RadLog')
        self.root.geometry('500x300')
        self.root.resizable(False, False)
        
        # 載入設定
        self.config = self.load_config()
        self.sheets_service = None
        self.user_email = None
        
        # 檢查授權狀態
        if not self.check_license():
            self.show_license_required()
            return
        
        # 初始化 Google Sheets
        self.init_google_sheets()
        
        # 建立 UI
        self.create_ui()
        
        # 全局快捷鍵（Windows）
        self.setup_hotkey()
    
    def load_config(self):
        """載入設定"""
        CONFIG_DIR.mkdir(exist_ok=True)
        
        default_config = {
            'categories': ['tumor', 'vascular', 'infection', 'trauma', 'other'],
            'spreadsheet_id': '',
            'sheet_name': 'RadLog',
            'hotkey': 'ctrl+shift+r',
        }
        
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 合併預設值
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
        
        return default_config
    
    def save_config(self):
        """儲存設定"""
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def check_license(self):
        """檢查 license（透過 Google 帳號）"""
        if not self.user_email:
            # 先嘗試取得 Google 帳號
            creds = self.get_google_credentials()
            if creds:
                # 取得用戶 email
                try:
                    service = build('oauth2', 'v2', credentials=creds)
                    user_info = service.userinfo().get().execute()
                    self.user_email = user_info.get('email', '').lower()
                except:
                    pass
        
        if not self.user_email:
            return False
        
        # 驗證 license
        try:
            response = requests.get(
                f'{LICENSE_API}/verify',
                params={'email': self.user_email},
                timeout=10
            )
            data = response.json()
            return data.get('valid', False)
        except Exception as e:
            print(f'License check failed: {e}')
            # 離線時允許使用（已經驗證過一次）
            return self.config.get('license_verified', False)
    
    def get_google_credentials(self):
        """取得 Google OAuth credentials"""
        creds = None
        
        if TOKEN_FILE.exists():
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not CREDENTIALS_FILE.exists():
                    messagebox.showerror(
                        'Error',
                        f'請將 Google OAuth credentials.json 放到:\n{CREDENTIALS_FILE}'
                    )
                    return None
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(CREDENTIALS_FILE), SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        
        return creds
    
    def init_google_sheets(self):
        """初始化 Google Sheets API"""
        creds = self.get_google_credentials()
        if creds:
            self.sheets_service = build('sheets', 'v4', credentials=creds)
            
            # 記錄已驗證（離線用）
            self.config['license_verified'] = True
            self.save_config()
    
    def show_license_required(self):
        """顯示需要購買 license"""
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill='both', expand=True)
        
        ttk.Label(
            frame,
            text='RadLog 需要授權',
            font=('Arial', 16, 'bold')
        ).pack(pady=10)
        
        ttk.Label(
            frame,
            text='請先購買授權，然後使用購買時的 Google 帳號登入。',
            wraplength=400
        ).pack(pady=10)
        
        ttk.Button(
            frame,
            text='購買授權 ($19.99)',
            command=lambda: webbrowser.open('https://YOUR_LEMONSQUEEZY_URL')
        ).pack(pady=5)
        
        ttk.Button(
            frame,
            text='我已購買，重新登入',
            command=self.retry_login
        ).pack(pady=5)
    
    def retry_login(self):
        """重新登入"""
        # 刪除舊 token
        if TOKEN_FILE.exists():
            TOKEN_FILE.unlink()
        
        # 重新啟動
        self.root.destroy()
        app = RadLogApp()
        app.run()
    
    def create_ui(self):
        """建立主 UI"""
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill='both', expand=True)
        
        # 標題
        ttk.Label(
            main_frame,
            text='🏥 RadLog',
            font=('Arial', 18, 'bold')
        ).pack(pady=(0, 10))
        
        # 快速輸入框
        ttk.Label(main_frame, text='快速輸入 (MRN, category, note):').pack(anchor='w')
        
        self.quick_entry = ttk.Entry(main_frame, width=60, font=('Consolas', 11))
        self.quick_entry.pack(fill='x', pady=5)
        self.quick_entry.bind('<Return>', self.on_quick_submit)
        self.quick_entry.focus()
        
        # 或分開輸入
        ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=10)
        
        # MRN
        mrn_frame = ttk.Frame(main_frame)
        mrn_frame.pack(fill='x', pady=2)
        ttk.Label(mrn_frame, text='病歷號:', width=10).pack(side='left')
        self.mrn_entry = ttk.Entry(mrn_frame, width=20)
        self.mrn_entry.pack(side='left')
        
        # Category
        cat_frame = ttk.Frame(main_frame)
        cat_frame.pack(fill='x', pady=2)
        ttk.Label(cat_frame, text='分類:', width=10).pack(side='left')
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(
            cat_frame,
            textvariable=self.category_var,
            values=self.config['categories'],
            width=17
        )
        self.category_combo.pack(side='left')
        
        # Note
        note_frame = ttk.Frame(main_frame)
        note_frame.pack(fill='x', pady=2)
        ttk.Label(note_frame, text='備註:', width=10).pack(side='left')
        self.note_entry = ttk.Entry(note_frame, width=50)
        self.note_entry.pack(side='left', fill='x', expand=True)
        
        # 按鈕
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=15)
        
        ttk.Button(btn_frame, text='送出', command=self.on_submit).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='開啟 Sheet', command=self.open_sheet).pack(side='left', padx=5)
        ttk.Button(btn_frame, text='設定', command=self.show_settings).pack(side='right', padx=5)
        
        # 狀態列
        self.status_var = tk.StringVar(value='Ready')
        ttk.Label(main_frame, textvariable=self.status_var, foreground='gray').pack(anchor='w')
    
    def parse_quick_input(self, text):
        """解析快速輸入: MRN, category, note..."""
        parts = text.split(',', 2)
        
        if len(parts) >= 1:
            mrn = parts[0].strip()
        else:
            mrn = ''
        
        if len(parts) >= 2:
            category = parts[1].strip()
        else:
            category = ''
        
        if len(parts) >= 3:
            note = parts[2].strip()
        else:
            note = ''
        
        return mrn, category, note
    
    def on_quick_submit(self, event=None):
        """處理快速輸入提交"""
        text = self.quick_entry.get().strip()
        if not text:
            return
        
        mrn, category, note = self.parse_quick_input(text)
        
        # 填入分開的欄位
        self.mrn_entry.delete(0, tk.END)
        self.mrn_entry.insert(0, mrn)
        self.category_var.set(category)
        self.note_entry.delete(0, tk.END)
        self.note_entry.insert(0, note)
        
        # 直接提交
        self.on_submit()
        
        # 清空快速輸入
        self.quick_entry.delete(0, tk.END)
    
    def on_submit(self):
        """提交記錄到 Google Sheet"""
        mrn = self.mrn_entry.get().strip()
        category = self.category_var.get().strip()
        note = self.note_entry.get().strip()
        
        if not mrn:
            messagebox.showwarning('Warning', '請輸入病歷號')
            return
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 新增到 Sheet
        if self.append_to_sheet([timestamp, mrn, category, note]):
            self.status_var.set(f'✓ 已記錄: {mrn}')
            
            # 清空輸入
            self.mrn_entry.delete(0, tk.END)
            self.category_var.set('')
            self.note_entry.delete(0, tk.END)
            self.quick_entry.focus()
            
            # 新增 category 到列表（如果是新的）
            if category and category not in self.config['categories']:
                self.config['categories'].append(category)
                self.category_combo['values'] = self.config['categories']
                self.save_config()
        else:
            self.status_var.set('✗ 記錄失敗')
    
    def append_to_sheet(self, row):
        """新增一行到 Google Sheet"""
        if not self.sheets_service:
            messagebox.showerror('Error', 'Google Sheets 未連接')
            return False
        
        spreadsheet_id = self.config.get('spreadsheet_id')
        if not spreadsheet_id:
            messagebox.showerror('Error', '請先在設定中指定 Spreadsheet ID')
            return False
        
        try:
            sheet_name = self.config.get('sheet_name', 'RadLog')
            range_name = f'{sheet_name}!A:D'
            
            body = {'values': [row]}
            
            self.sheets_service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='USER_ENTERED',
                body=body
            ).execute()
            
            return True
        except Exception as e:
            print(f'Append failed: {e}')
            messagebox.showerror('Error', f'寫入失敗: {e}')
            return False
    
    def open_sheet(self):
        """開啟 Google Sheet"""
        spreadsheet_id = self.config.get('spreadsheet_id')
        if spreadsheet_id:
            webbrowser.open(f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}')
        else:
            messagebox.showwarning('Warning', '請先在設定中指定 Spreadsheet ID')
    
    def show_settings(self):
        """顯示設定視窗"""
        settings_win = tk.Toplevel(self.root)
        settings_win.title('設定')
        settings_win.geometry('450x300')
        settings_win.transient(self.root)
        
        frame = ttk.Frame(settings_win, padding=15)
        frame.pack(fill='both', expand=True)
        
        # Spreadsheet ID
        ttk.Label(frame, text='Google Spreadsheet ID:').pack(anchor='w')
        sheet_id_entry = ttk.Entry(frame, width=50)
        sheet_id_entry.insert(0, self.config.get('spreadsheet_id', ''))
        sheet_id_entry.pack(fill='x', pady=5)
        
        ttk.Label(
            frame,
            text='(從 Sheet URL 複製: https://docs.google.com/spreadsheets/d/[這段]/edit)',
            foreground='gray',
            wraplength=400
        ).pack(anchor='w')
        
        # Sheet Name
        ttk.Label(frame, text='Sheet 名稱:').pack(anchor='w', pady=(10, 0))
        sheet_name_entry = ttk.Entry(frame, width=30)
        sheet_name_entry.insert(0, self.config.get('sheet_name', 'RadLog'))
        sheet_name_entry.pack(anchor='w', pady=5)
        
        # Categories
        ttk.Label(frame, text='分類 (逗號分隔):').pack(anchor='w', pady=(10, 0))
        categories_entry = ttk.Entry(frame, width=50)
        categories_entry.insert(0, ', '.join(self.config.get('categories', [])))
        categories_entry.pack(fill='x', pady=5)
        
        def save_settings():
            self.config['spreadsheet_id'] = sheet_id_entry.get().strip()
            self.config['sheet_name'] = sheet_name_entry.get().strip() or 'RadLog'
            self.config['categories'] = [
                c.strip() for c in categories_entry.get().split(',') if c.strip()
            ]
            self.category_combo['values'] = self.config['categories']
            self.save_config()
            settings_win.destroy()
        
        ttk.Button(frame, text='儲存', command=save_settings).pack(pady=15)
    
    def setup_hotkey(self):
        """設定全局快捷鍵（僅 Windows）"""
        try:
            import keyboard
            hotkey = self.config.get('hotkey', 'ctrl+shift+r')
            keyboard.add_hotkey(hotkey, self.show_window)
            print(f'Hotkey registered: {hotkey}')
        except ImportError:
            print('Warning: keyboard module not found, hotkey disabled')
        except Exception as e:
            print(f'Hotkey setup failed: {e}')
    
    def show_window(self):
        """顯示視窗（從系統匣或快捷鍵）"""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        self.quick_entry.focus()
    
    def run(self):
        """啟動應用"""
        self.root.mainloop()


if __name__ == '__main__':
    app = RadLogApp()
    app.run()
