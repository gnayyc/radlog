#!/usr/bin/env python3
"""
RadLog macOS 版
使用 rumps 做 menubar app + 全局快捷鍵
"""

import rumps
import subprocess
import json
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

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
LICENSE_API = 'https://radlog-license.YOUR_SUBDOMAIN.workers.dev'


class RadLogApp(rumps.App):
    def __init__(self):
        super().__init__("🏥", quit_button=None)
        
        self.config = self.load_config()
        self.sheets_service = None
        self.user_email = None
        
        # 建立選單
        self.menu = [
            rumps.MenuItem("📝 快速記錄", callback=self.show_input),
            rumps.MenuItem("📊 開啟 Sheet", callback=self.open_sheet),
            None,  # 分隔線
            rumps.MenuItem("⚙️ 設定", callback=self.show_settings),
            rumps.MenuItem("❌ 結束", callback=self.quit_app),
        ]
        
        # 初始化
        self.init_google_sheets()
        
        # 註冊全局快捷鍵
        self.register_hotkey()
    
    def load_config(self):
        CONFIG_DIR.mkdir(exist_ok=True)
        
        default = {
            'categories': ['tumor', 'vascular', 'infection', 'trauma', 'other'],
            'spreadsheet_id': '',
            'sheet_name': 'RadLog',
        }
        
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                for k, v in default.items():
                    if k not in config:
                        config[k] = v
                return config
        return default
    
    def save_config(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_google_credentials(self):
        creds = None
        
        if TOKEN_FILE.exists():
            creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not CREDENTIALS_FILE.exists():
                    rumps.alert(
                        "錯誤",
                        f"請將 credentials.json 放到:\n{CREDENTIALS_FILE}"
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
        creds = self.get_google_credentials()
        if creds:
            self.sheets_service = build('sheets', 'v4', credentials=creds)
    
    def register_hotkey(self):
        """註冊全局快捷鍵 Cmd+Shift+R"""
        # 使用 pynput 或 系統 AppleScript
        # 這裡用簡單的 AppleScript 方式
        script = '''
        tell application "System Events"
            -- 監聽快捷鍵需要輔助功能權限
        end tell
        '''
        # 實際實現需要更複雜的處理，這裡先跳過
        pass
    
    @rumps.clicked("📝 快速記錄")
    def show_input(self, _):
        """顯示輸入對話框"""
        response = rumps.Window(
            message='輸入格式: 病歷號, 分類, 備註',
            title='RadLog 快速記錄',
            default_text='',
            ok='送出',
            cancel='取消',
            dimensions=(400, 24)
        ).run()
        
        if response.clicked:
            text = response.text.strip()
            if text:
                self.process_input(text)
    
    def process_input(self, text):
        """處理輸入"""
        parts = text.split(',', 2)
        
        mrn = parts[0].strip() if len(parts) > 0 else ''
        category = parts[1].strip() if len(parts) > 1 else ''
        note = parts[2].strip() if len(parts) > 2 else ''
        
        if not mrn:
            rumps.alert("錯誤", "請輸入病歷號")
            return
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if self.append_to_sheet([timestamp, mrn, category, note]):
            rumps.notification(
                "RadLog",
                "記錄成功",
                f"病歷號: {mrn}"
            )
            
            # 新增 category
            if category and category not in self.config['categories']:
                self.config['categories'].append(category)
                self.save_config()
        else:
            rumps.alert("錯誤", "寫入失敗")
    
    def append_to_sheet(self, row):
        if not self.sheets_service:
            return False
        
        spreadsheet_id = self.config.get('spreadsheet_id')
        if not spreadsheet_id:
            rumps.alert("錯誤", "請先設定 Spreadsheet ID")
            return False
        
        try:
            sheet_name = self.config.get('sheet_name', 'RadLog')
            self.sheets_service.spreadsheets().values().append(
                spreadsheetId=spreadsheet_id,
                range=f'{sheet_name}!A:D',
                valueInputOption='USER_ENTERED',
                body={'values': [row]}
            ).execute()
            return True
        except Exception as e:
            print(f'Error: {e}')
            return False
    
    @rumps.clicked("📊 開啟 Sheet")
    def open_sheet(self, _):
        spreadsheet_id = self.config.get('spreadsheet_id')
        if spreadsheet_id:
            webbrowser.open(f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}')
        else:
            rumps.alert("錯誤", "請先設定 Spreadsheet ID")
    
    @rumps.clicked("⚙️ 設定")
    def show_settings(self, _):
        response = rumps.Window(
            message='輸入 Google Spreadsheet ID:',
            title='RadLog 設定',
            default_text=self.config.get('spreadsheet_id', ''),
            ok='儲存',
            cancel='取消',
            dimensions=(400, 24)
        ).run()
        
        if response.clicked:
            self.config['spreadsheet_id'] = response.text.strip()
            self.save_config()
            rumps.notification("RadLog", "設定已儲存", "")
    
    @rumps.clicked("❌ 結束")
    def quit_app(self, _):
        rumps.quit_application()


if __name__ == '__main__':
    RadLogApp().run()
