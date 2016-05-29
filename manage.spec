# -*- mode: python -*-

block_cipher = None


a = Analysis(['manage.py'],
             pathex=['/Users/lee/Desktop/product'],
             binaries=None,
             datas=None,
             hiddenimports=['django', 'django-bootstrap', 'openpyxl', 'hierarchy.migrations'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='manage',
          debug=False,
          strip=False,
          upx=True,
          console=True )
