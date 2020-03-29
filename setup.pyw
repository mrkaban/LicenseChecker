# coding: utf-8

from cx_Freeze import setup, Executable
import sys

excludes = ['asyncio', '', 'collections', 'concurrent', 'distutils', 'email', 'PyQt5',
'shiboken2', 'test', 'unittest', 'libcrypto-1_1']

#executables = [Executable('main.pyw',
#                          targetName='exe/LicenseCheker.exe',
#                          base='Win32GUI',
#                          icon='data/LicenseCheker.ico')]
include_files = ['data']

base = None
if sys.platform == "win32":
    base = "Win32GUI"

if 'bdist_msi' in sys.argv:
    sys.argv += ['--initial-target-dir', 'C:\\LicenseCheker']

options = {
    'build_msi': {
        'include_msvcr': True,
        'include_files': include_files,
        "excludes": excludes,
        'initial_target_dir': 'C:\\LicenseCheker',
    }
}

setup(name='LicenseCheker',
      version='0.2',
      description='LicenseCheker',
      options=options,
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
