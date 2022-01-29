import platform
import winreg #Для проверки ключа ОС
import wmi #Для проверки ключа ОС
import os#для поиска следов активации
import re

def DetectOS():
    """Функция обнаружения операционной системы"""
    SlovarOS={'Windows XP ProfessionalEdition':3870, 'Windows XP HomeEdition':1480,
    'Windows XP 64-bitEdition':4140, 'Windows XP Профессиональная':3870, 'Windows XP Домашняя':1480,
     'Windows XP TabletPCEdition':1278, 'Windows XP Professionalx64Edition':4140,
     'Windows XP Embedded':4000, 'Windows EmbeddedPOSReady':4000,
     'Windows XP StarterEdition':1250, 'Windows FundamentalsforLegacyPCs':4000,
     'Windows Server 2003 WebEdition':4500, 'Windows XPEditionN':3455,
     'Windows Server 2003 StandardEdition':4500, 'Windows Server 2003 EnterpriseEdition':4500,
     'Windows Server 2003 DatacenterEdition':4500, 'Windows Vista Starter':990,
     'Windows Vista HomeBasic':1990, 'Windows Vista Домашняя базовая':1990,
     'Windows Vista HomePremium':2430, 'Windows Vista Домашняя расширенная':2430,
     'Windows Vista Business':1990, 'Windows Vista Бизнес':1990, 'Windows Vista Начальная':990,
     'Windows Vista Enterprise':1990, 'Windows Vista Корпоративная':1990,
     'Windows Vista Максимальная':3990, 'Windows Vista UltimateUpgradeLimitedNumberedSignatureEdition':9339,
     'Windows Home Server':6803, 'Windows Server 2008 StandardEdition':22500,
     'Windows Server 2008 EnterpriseEdition':114495, 'Windows WebServer2008':44950,
     'Windows Server 2008 DatacenterEdition':20818, 'Windows HPCServer2008':20818,
     'Windows Storage Server2008':20818, 'Windows SmallBusinessServer2008':35624,
     'Windows Essential BusinessServer2008':156581, 'Windows 7 Ultimate':8090,
     'Windows 7 Максимальная':8090, 'Windows 7 Домашняя расширенная':6850,
     'Windows 7 Enterprise':13167, 'Windows 7 Корпоративная':13167, 'Windows 7 Professional':9050,
     'Windows 7 Профессиональная':9050, 'Windows 7 HomePremium':6850,
     'Windows 7 HomeBasic':5570, 'Windows 7 Домашняя базовая':5570, 'Windows 7 Starter':4390,
     'Windows 7 Начальная':4390, 'Windows Server 2008 R2 Standard':50452,
     'Windows Server 2008 R2 Enterprise':128000, 'Windows Server 2012 Standard':62908,
     'Windows Server 2008 R2 Foundation':50452, 'Windows Home Server 2011':12760,
     'Windows 8 Professional':5480, 'Windows 8 Профессиональная':5480, 'Windows 8 Pro':5480,
     'Windows 8 Корпоративная':5480, 'Windows 8 Enterprise':5480, 'Windows 8 Core':5480,
     'Windows Server 2012 Foundation':16270, 'Windows Server 2012 Essentials':28502,
     'Windows Server 2012 Datacenter':280392, 'Windows RT 8.1':5480, 'Windows 8.1 Pro':5480,
     'Windows 8.1 Профессиональная':5480, 'Windows 10 HomeWithBing':8699,
     'Windows 8.1 Корпоративная':5480, 'Windows 8.1 Enterprise':5480,
     'Windows 10 Домашняя':8699, 'Windows 10 Home':8699, 'Windows 10 Профессиональная':12599,
     'Windows 10 Pro':12599, 'Windows 10 Корпоративная':8935, 'Windows 10 Enterprise':8935,
     'Windows 10 Домашняя для одного языка':8699, 'Windows 10 HomeSingleLanguage':8699,
     'Windows 10 HomeSL':8699, 'Windows RT':5480, 'Windows Vista Ultimate':3990,
     'Windows 10 CoreSingleLanguage':7499, 'Windows 10 Домашняя с Bing':8699,
     'Windows 10 S':7750, 'Windows 10 Pro для образовательных учреждений':12599,
     'Windows 10 ProEducation':12599, 'Windows 8.1 Professional':5480,
     'Windows 10 Pro Для рабочих станций':12599, 'Windows 10 ProforWorkstations':12599,
     'Windows 10 Корпоративная с долгосрочным обслуживанием':16460, 'Windows 10 EnterpriseLTSC':16460,
     'Windows 10 EnterpriseLTSB':16460, 'Windows 10 для образовательных учреждений':8699,
     'Windows 10 Education':8699, 'Windows 7':4000, 'Windows Vista':2000,
     'Windows 10 Team':7000, 'Windows 10 HomeSLN':8699, 'Windows 10 HomeN':8699,
     'Windows 10 SN':7000, 'Windows 10 ProN':12599, 'Windows 10 EntepriseN':8935,
     'Windows 10 EnterpiseLTSCN':16460, 'Windows 10 HomeSLKN':8699, 'Windows 10 HomeKN':8699,
     'Windows 10 SKN':7000, 'Windows 10 ProKN':12599, 'Windows 10 EntepriseKN':8935,
     'Windows 10 Enterpise LTSCKN':16460, 'Windows 10 Entry':7000, 'Windows 10 Value':7000,
     'Windows 10 Core':8699, 'Windows 10 Core +':8699, 'Windows 10 Core+':8699,
     'Windows 10 Advanced':7000, 'Windows 10 IoTCore':7000, 'Windows 10 IoTMobile':7000,
     'Windows 10 IoTEnterprise':7000, 'Windows 10 IoTMobileEnterprise':7000,
     'Windows 10 Мобильная корпоративная':7000, 'Windows 8.1 Core':5480, 'Windows 8.1 с Bing':5480,
     'Windows 8.1 для одного языка':5480, 'Windows 8.1':5480, 'Windows 8':5480,
     'Windows 10':7000, 'Windows 10 Мобильная':7000,
     'Windows 11 Домашняя':8699, 'Windows 11 Home':8699, 'Windows 11 Профессиональная':12599,
     'Windows 11 Pro':12599, 'Windows 11 Корпоративная':8935, 'Windows 11 Enterprise':8935,
     'Windows 11 Домашняя для одного языка':8699, 'Windows 11 HomeSingleLanguage':8699,
     'Windows 11 HomeSL':8699, 'Windows RT':5480, 'Windows Vista Ultimate':3990,
     'Windows 11 CoreSingleLanguage':7499, 'Windows 11 Домашняя с Bing':8699,
     'Windows 11 S':7750, 'Windows 11 Pro для образовательных учреждений':12599,
     'Windows 11 ProEducation':12599, 'Windows 8.1 Professional':5480,
     'Windows 11 Pro Для рабочих станций':12599, 'Windows 11 ProforWorkstations':12599,
     'Windows 11 Корпоративная с долгосрочным обслуживанием':16460, 'Windows 11 EnterpriseLTSC':16460,
     'Windows 11 EnterpriseLTSB':16460, 'Windows 11 для образовательных учреждений':8699,
     'Windows 11 Education':8699, 
     'Windows 11 Team':7000, 'Windows 11 HomeSLN':8699, 'Windows 11 HomeN':8699,
     'Windows 11 SN':7000, 'Windows 11 ProN':12599, 'Windows 11 EntepriseN':8935,
     'Windows 11 EnterpiseLTSCN':16460, 'Windows 11 HomeSLKN':8699, 'Windows 11 HomeKN':8699,
     'Windows 11 SKN':7000, 'Windows 11 ProKN':12599, 'Windows 11 EntepriseKN':8935,
     'Windows 11 Enterpise LTSCKN':16460, 'Windows 11 Entry':7000, 'Windows 11 Value':7000,
     'Windows 11 Core':8699, 'Windows 11 Core +':8699, 'Windows 11 Core+':8699,
     'Windows 11 Advanced':7000, 'Windows 11 IoTCore':7000, 'Windows 11 IoTMobile':7000,
     'Windows 11 IoTEnterprise':7000, 'Windows 11 IoTMobileEnterprise':7000,
     'Windows 11 Мобильная корпоративная':7000, 'Windows 8.1 Core':5480, 'Windows 8.1 с Bing':5480,
     'Windows 8.1 для одного языка':5480, 'Windows 8.1':5480, 'Windows 8':5480,
     'Windows 11':7000, 'Windows 11 Мобильная':7000,
     }
    sys_rel_ed = platform.system() + ' ' + platform.release() + ' ' + platform.win32_edition()
    sys_ed = platform.system() + ' ' + platform.win32_edition()
    sys_rel = platform.system() + ' ' + platform.release()
    s=''
    matchOS = False
    for itemOS in SlovarOS:
        s = SlovarOS[itemOS]
        if sys_rel_ed == itemOS:
            matchOS = True
            return itemOS, s
        elif sys_ed == itemOS:
            matchOS = True
            return sys_ed, s
        elif sys_rel == itemOS:
            matchOS = True
            return sys_rel, s
        else:
            s = '???'
    if matchOS == False:
        return sys_rel_ed, s
#Конец проверки версии ОС

#Начало проверки ключа ОС
# This function is derived from https://gist.github.com/Spaceghost/877110
def decode_key(rpk):
    rpkOffset = 52
    i = 28
    szPossibleChars = "BCDFGHJKMPQRTVWXY2346789"
    szProductKey = ""

    while i >= 0:
        dwAccumulator = 0
        j = 14
        while j >= 0:
            dwAccumulator = dwAccumulator * 256
            d = rpk[j + rpkOffset]
            if isinstance(d, str):
                d = ord(d)
            dwAccumulator = d + dwAccumulator
            rpk[j + rpkOffset] = int(dwAccumulator / 24) if int(dwAccumulator / 24) <= 255 else 255
            dwAccumulator = dwAccumulator % 24
            j = j - 1
        i = i - 1
        szProductKey = szPossibleChars[dwAccumulator] + szProductKey

        if ((29 - i) % 6) == 0 and i != -1:
            i = i - 1
            szProductKey = "-" + szProductKey
    return szProductKey


def get_key_from_reg_location(key, value='DigitalProductID'):
    arch_keys = [0, winreg.KEY_WOW64_32KEY, winreg.KEY_WOW64_64KEY]
    for arch in arch_keys:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key, 0, winreg.KEY_READ | arch)
            value, type = winreg.QueryValueEx(key, value)
            # Return the first match
            return decode_key(list(value))
        except (FileNotFoundError, TypeError) as e:
            pass


def get_windows_product_key_from_reg():
    return get_key_from_reg_location('SOFTWARE\Microsoft\Windows NT\CurrentVersion')


def get_windows_product_key_from_wmi():
    w = wmi.WMI()
    try:
        product_key = w.softwarelicensingservice()[0].OA3xOriginalProductKey
        if product_key != '':
            return product_key
        else:
            return None
    except AttributeError:
        return None
def sled_activation():
    dir = 'C:\\Windows\\'
    spisok=[]
    if os.path.exists('C:\\ProgramData\\KMSAutoS\\'):
        spisok.append('C:\\ProgramData\\KMSAutoS\\')
    for root, dirs, files in os.walk(dir):
        for subdir in dirs:
            pattern=r'Активатор|Activator|активатор|AAct_Tools|ConsoleAct|KMSAutoS|AutoKMS'
            search_exemple = re.search(pattern, subdir, re.M|re.I)
            if search_exemple:
                s1 = root+'\\'+subdir+'\\'
                if s1.find("\\\\", 0, len(s1)) >= 1: #Только отдельно, удаление кавычек
                     s1 = s1.replace("\\\\", '\\')
                spisok.append(s1)
    return spisok
#Конец проверки ключа ОС
if __name__ == "__main__":
    a, b = DetectOS()
    print('Значение а: ', a, 'Значение b: ', b)
    print('Key from WMI: %s' % get_windows_product_key_from_wmi())
    print('Key from REG: %s' % get_windows_product_key_from_reg())
    print(sled_activation())
