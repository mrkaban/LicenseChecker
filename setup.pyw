# coding: utf-8

from cx_Freeze import setup, Executable
import sys

excludes = ['asyncio', '', 'collections', 'concurrent', 'distutils', 'email',
'test', 'unittest', 'libcrypto-1_1']

include_files = ['data']
base = None
if sys.platform == "win32":
    base = "Win32GUI"

if 'bdist_msi' in sys.argv:
    sys.argv += ['--initial-target-dir', 'C:\\LicenseChecker']

options = {
    'build_msi': {
        'include_msvcr': True,
        'upgrade_code': '{66620F3A-DC3A-11E2-B341-002219E9B011}',
        'product_code': '{66620F3A-DC3A-11E2-B341-002219E9B011}',
        'include_files': include_files,
        "excludes": excludes,
    }
}


setup(name='LicenseChecker',
      version='1.6',
      description='LicenseChecker - Проверка легальности установленных программ',
      author = 'mrkaban (КонтинентСвободы.рф)',
      data_files=[
                  ('data', ['data/LicenseChecker.png']),
                  ('data', ['data/Lpro.db']),
                  ('data', ['data/LicenseChecker.ico']),
                  ('data', ['data/gpl-2.0.rtf']),
                  ('data', ['data/python-powered.png']),
                  ('data', ['data/User-DB.db']),
                  ('data', ['data/About.ui']),
                  ('data', ['data/main.ui']),
                  ('data', ['data/DoubleClick.ui']),
                  ('data', ['data/PoisZamen.ui']),
                  ('data', ['data/Spravka.ui']),
                  ('data', ['data/ViewBD.ui']),
                  ('data', ['data/RuchPoisk.ui']),
                  ('data', ['data/Media.ui']),
                  ('data', ['data/settings.ui']),
                  ('data', ['data/settings.ini']),
                  ('data', ['data/cat-auto.png']),
                  ('data', ['data/cat-bd.png']),
                  ('data', ['data/cat-media.png']),
                  ('data', ['data/cat-ruch.png']),
                  ('data', ['data/cat-zamena.png']),
                  ('data', ['data/donate.png']),
                  ],
      options=options,
            executables = [
        Executable(
            script = "main.pyw",
            copyright ='mrkaban (КонтинентСвободы.рф)',
            base=base,
            icon="data/LicenseChecker.ico",
            shortcutName="LicenseChecker",
            shortcutDir='ProgramMenuFolder',
            )
        ]
      )

# команда для CMD
#python.exe setup.pyw bdist_msi
#--ext-list-file=data/Lpro.db, LicenseChecker.png, LicenseChecker.ico  -icon=LicenseChecker.ico

# cd /d D:\LicenseChecker\1.6
