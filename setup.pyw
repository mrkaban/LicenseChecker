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
product_name = 'LicenseCheker'
base = None
if sys.platform == "win32":
    base = "Win32GUI"

if 'bdist_msi' in sys.argv:
    sys.argv += ['--initial-target-dir', 'C:\\LicenseCheker']

bdist_msi_options = {
    'build_msi': {
        'include_msvcr': True,
        'upgrade_code': '{66620F3A-DC3A-11E2-B341-002219E9B01E}',
        'include_files': include_files,
        "excludes": excludes,
        'initial_target_dir': r'[ProgramFilesFolder]\%s\%s' % (product_name),
    }
}

build_exe_options = {
    'includes': ['data'],
    "excludes": ['asyncio', '', 'collections', 'concurrent', 'distutils', 'email', 'PyQt5',
    'shiboken2', 'test', 'unittest', 'libcrypto-1_1'],
    }

setup(name='LicenseCheker',
      version='0.2',
      description='LicenseCheker',
      options={
          'bdist_msi': bdist_msi_options,
          'build_exe': build_exe_options}),
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
