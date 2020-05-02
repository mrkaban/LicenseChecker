# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['D:\\LicenseChecker\\1.2\\main.pyw'],
             pathex=['D:\\LicenseChecker\\1.2'],
             binaries=[],
             datas=[('data\\LicenseChecker.ico', 'data'), ('data\\Lpro.db', 'data'), ('data\\LicenseChecker.png', 'data'), ('data\\gpl-2.0.rtf', 'data'), ('data\\python-powered.png', 'data'), ('data\\User-DB.db', 'data'), ('data\\About.ui', 'data'), ('data\\main.ui', 'data'), ('data\\DoubleClick.ui', 'data'), ('data\\PoisZamen.ui', 'data'), ('data\\Spravka.ui', 'data'), ('data\\ViewBD.ui', 'data'), ('data\\RuchPoisk.ui', 'data'), ('data\\Media.ui', 'data'), ('data\\settings.ui', 'data'), ('data\\settings.ini', 'data')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='LicenseChecker',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='data\\LicenseChecker.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='LicenseChecker')
