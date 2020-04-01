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
        'upgrade_code': '{66620F3A-DC3A-11E2-B341-002219E9B01E}',
        'include_files': include_files,
        "excludes": excludes,
        'initial_target_dir': '[ProgramFilesFolder]\LicenseCheker',
         }
}

setup(name='LicenseCheker',
      version='0.2',
      description='LicenseCheker',
      options=options,
      data_files=[('data', ['data/LicenseCheker.ico']),
                  ('data', ['data/LicenseCheker.png']),
                  ('data', ['data/Lpro.db']),
                  ('data', ['data/LicenseCheker.ico'])
                  ],
      #data_files=[('data/LicenseCheker.ico', ['data']),
      #            ('data/LicenseCheker.png', ['data']),
      #            ('data/Lpro.db', ['data'])
      #            ],
      executables = [
        Executable(
            script = "main.pyw",
            copyright="КонтинентСвободы.рф",
            base=base,
            icon="data/LicenseCheker.ico",
            shortcutName="LicenseCheker",
            shortcutDir="DesktopFolder",
            )
        ]
      )

# команда для CMD
#python.exe setup.pyw bdist_msi
#--ext-list-file=data/Lpro.db, LicenseCheker.png, LicenseCheker.ico  -icon=LicenseCheker.ico

# cd /d D:\Public\LicenseCheker\0.2
