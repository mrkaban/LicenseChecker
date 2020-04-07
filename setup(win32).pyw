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
    sys.argv += ['--initial-target-dir', 'C:\\LicenseChecker']

options = {
    'build_msi': {
        'include_msvcr': True,
        'upgrade_code': '{66620F3A-DC3A-11E2-B341-002219E9B01E}',
        'include_files': include_files,
        "excludes": excludes,
        'initial_target_dir': '[ProgramFilesFolder]\LicenseChecker',
         }
}

setup(name='LicenseChecker',
      version='0.2',
      description='LicenseChecker',
      options=options,
      data_files=[('data', ['data/LicenseChecker.ico']),
                  ('data', ['data/LicenseChecker.png']),
                  ('data', ['data/Lpro.db']),
                  ('data', ['data/LicenseChecker.ico'])
                  ],
      #data_files=[('data/LicenseChecker.ico', ['data']),
      #            ('data/LicenseChecker.png', ['data']),
      #            ('data/Lpro.db', ['data'])
      #            ],
      executables = [
        Executable(
            script = "main.pyw",
            copyright="КонтинентСвободы.рф",
            base=base,
            icon="data/LicenseChecker.ico",
            shortcutName="LicenseChecker",
            shortcutDir="DesktopFolder",
            )
        ]
      )

# команда для CMD
#python.exe setup.pyw bdist_msi
#--ext-list-file=data/Lpro.db, LicenseChecker.png, LicenseChecker.ico  -icon=LicenseChecker.ico

# cd /d D:\Public\LicenseChecker\0.2
