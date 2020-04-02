# coding: utf-8

from cx_Freeze import setup, Executable
import sys

excludes = ['asyncio', '', 'collections', 'concurrent', 'distutils', 'email', 'PyQt5',
'shiboken2', 'test', 'unittest', 'libcrypto-1_1']

include_files = ['data']
base = None
if sys.platform == "win32":
    base = "Win32GUI"

if 'bdist_msi' in sys.argv:
    sys.argv += ['--initial-target-dir', 'C:\\LicenseCheker']

options = {
    'build_msi': {
        'include_msvcr': True,
        'upgrade_code': '{66620F3A-DC3A-11E2-B341-002219E9B011}',
        'product_code': '{66620F3A-DC3A-11E2-B341-002219E9B011}',
        'include_files': include_files,
        "excludes": excludes,
    }
}


setup(name='LicenseCheker',
      version='0.3',
      description='LicenseCheker - Проверка лицензий установленных программ',
      author = 'mrkaban (КонтинентСвободы.рф)',
      data_files=[
                  ('data', ['data/LicenseCheker.png']),
                  ('data', ['data/Lpro.db']),
                  ('data', ['data/LicenseCheker.ico']),
                  ('data', ['data/gpl-2.0.rtf']),
                  ],
      options=options,
            executables = [
        Executable(
            script = "main.pyw",
            copyright ='mrkaban (КонтинентСвободы.рф)',
            base=base,
            icon="data/LicenseCheker.ico",
            shortcutName="LicenseCheker",
            shortcutDir='ProgramMenuFolder',
            )
        ]
      )

# команда для CMD
#python.exe setup.pyw bdist_msi
#--ext-list-file=data/Lpro.db, LicenseCheker.png, LicenseCheker.ico  -icon=LicenseCheker.ico

# cd /d D:\Public\LicenseCheker\0.3
