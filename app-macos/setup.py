"""
py2app build script for RadLog macOS
Usage: python setup.py py2app
"""

from setuptools import setup

APP = ['radlog_mac.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'icon.icns',
    'plist': {
        'CFBundleName': 'RadLog',
        'CFBundleDisplayName': 'RadLog',
        'CFBundleIdentifier': 'com.radlog.app',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSUIElement': True,  # 不顯示在 Dock
    },
    'packages': [
        'rumps',
        'google',
        'googleapiclient',
        'google_auth_oauthlib',
    ],
}

setup(
    app=APP,
    name='RadLog',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
