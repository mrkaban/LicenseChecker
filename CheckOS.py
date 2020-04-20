import platform
import winreg #Для проверки ключа ОС
import wmi #Для проверки ключа ОС
import os#для поиска следов активации
import re

def DetectOS():
    """Функция обнаружения операционной системы"""
    SlovarOS={'Windows XP ProfessionalEdition': '3 870 руб', 'Windows XP HomeEdition': '1 480 руб',
    'Windows XP 64-bitEdition':'4 140 руб', 'Windows XP Профессиональная': '3 870 руб', 'Windows XP Домашняя': '1 480 руб',
     'Windows XP TabletPCEdition':'1 278 руб', 'Windows XP Professionalx64Edition':'4 140 руб',
     'Windows XP Embedded':'от 4 000 руб', 'Windows EmbeddedPOSReady':'от 4 000 руб',
     'Windows XP StarterEdition':'1 250 руб', 'Windows FundamentalsforLegacyPCs':'от 4 000 руб',
     'Windows Server 2003 WebEdition':'4 500 руб', 'Windows XPEditionN':'3 455 руб',
     'Windows Server 2003 StandardEdition':'4 500 руб', 'Windows Server 2003 EnterpriseEdition':'4 500 руб',
     'Windows Server 2003 DatacenterEdition':'4 500 руб', 'Windows Vista Starter':'990 руб',
     'Windows Vista HomeBasic':'1 990 руб', 'Windows Vista Домашняя базовая':'1 990 руб',
     'Windows Vista HomePremium':'2 430 руб', 'Windows Vista Домашняя расширенная':'2 430 руб',
     'Windows Vista Business':'1 990 руб', 'Windows Vista Бизнес':'1 990 руб', 'Windows Vista Начальная':'990 руб',
     'Windows Vista Enterprise':'1 990 руб', 'Windows Vista Корпоративная':'1 990 руб',
     'Windows Vista Максимальная':'3 990 руб', 'Windows Vista UltimateUpgradeLimitedNumberedSignatureEdition':'9 339 руб',
     'Windows Home Server':'6 803 руб', 'Windows Server 2008 StandardEdition':'22 500 руб',
     'Windows Server 2008 EnterpriseEdition':'114 495 руб', 'Windows WebServer2008':'44 950 руб',
     'Windows Server 2008 DatacenterEdition':'20 818 руб', 'Windows HPCServer2008':'от 20 818 руб',
     'Windows Storage Server2008':'от 20 818 руб', 'Windows SmallBusinessServer2008':'35624 руб',
     'Windows Essential BusinessServer2008':'156 581 руб', 'Windows 7 Ultimate':'8 090 руб',
     'Windows 7 Максимальная':'8 090 руб', 'Windows 7 Домашняя расширенная':'6 850 руб',
     'Windows 7 Enterprise':'13 167 руб', 'Windows 7 Корпоративная':'13 167 руб', 'Windows 7 Professional':'9 050 руб',
     'Windows 7 Профессиональная':'9 050 руб', 'Windows 7 HomePremium':'6 850 руб',
     'Windows 7 HomeBasic':'5 570 руб', 'Windows 7 Домашняя базовая':'5 570 руб', 'Windows 7 Starter':'4 390 руб',
     'Windows 7 Начальная':'4 390 руб', 'Windows Server 2008 R2 Standard':'50 452 руб',
     'Windows Server 2008 R2 Enterprise':'128 000 руб', 'Windows Server 2012 Standard':'62 908 руб',
     'Windows Server 2008 R2 Foundation':'50 452 руб', 'Windows Home Server 2011':'12 760 руб',
     'Windows 8 Professional':'5 480 руб', 'Windows 8 Профессиональная':'5 480 руб', 'Windows 8 Pro':'5 480 руб',
     'Windows 8 Корпоративная':'5 480 руб', 'Windows 8 Enterprise':'5 480 руб', 'Windows 8 Core':'5 480 руб',
     'Windows Server 2012 Foundation':'16 270 руб', 'Windows Server 2012 Essentials':'28 502 руб',
     'Windows Server 2012 Datacenter':'280 392 руб', 'Windows RT 8.1':'5 480 руб', 'Windows 8.1 Pro':'5 480 руб',
     'Windows 8.1 Профессиональная':'5 480 руб', 'Windows 10 HomeWithBing':'8 699 руб',
     'Windows 8.1 Корпоративная':'5 480 руб', 'Windows 8.1 Enterprise':'5 480 руб',
     'Windows 10 Домашняя':'8 699 руб', 'Windows 10 Home':'8 699 руб', 'Windows 10 Профессиональная':'12 599 руб',
     'Windows 10 Pro':'12 599 руб', 'Windows 10 Корпоративная':'8 935 руб', 'Windows 10 Enterprise':'8 935 руб',
     'Windows 10 Домашняя для одного языка':'8 699 руб', 'Windows 10 HomeSingleLanguage':'8 699 руб',
     'Windows 10 HomeSL':'8 699 руб', 'Windows RT':'5 480 руб', 'Windows Vista Ultimate':'3 990 руб',
     'Windows 10 CoreSingleLanguage':'7 499 руб', 'Windows 10 Домашняя с Bing':'8 699 руб',
     'Windows 10 S':'7 750 руб', 'Windows 10 Pro для образовательных учреждений':'12 599 руб',
     'Windows 10 ProEducation':'12 599 руб', 'Windows 8.1 Professional':'5 480 руб',
     'Windows 10 Pro Для рабочих станций':'12 599 руб', 'Windows 10 ProforWorkstations':'12 599 руб',
     'Windows 10 Корпоративная с долгосрочным обслуживанием':'16 460 руб', 'Windows 10 EnterpriseLTSC':'16 460 руб',
     'Windows 10 EnterpriseLTSB':'16 460 руб', 'Windows 10 для образовательных учреждений':'8 699 руб',
     'Windows 10 Education':'8 699 руб', 'Windows 7':'от 4 000 руб', 'Windows Vista':'от 2 000 руб',
     'Windows 10 Team':'от 7 000 руб', 'Windows 10 HomeSLN':'8 699 руб', 'Windows 10 HomeN':'8 699 руб',
     'Windows 10 SN':'от 7 000 руб', 'Windows 10 ProN':'12 599 руб', 'Windows 10 EntepriseN':'8 935 руб',
     'Windows 10 EnterpiseLTSCN':'16 460 руб', 'Windows 10 HomeSLKN':'8 699 руб', 'Windows 10 HomeKN':'8 699 руб',
     'Windows 10 SKN':'от 7 000 руб', 'Windows 10 ProKN':'', 'Windows 10 EntepriseKN':'8 935 руб',
     'Windows 10 Enterpise LTSCKN':'16 460 руб', 'Windows 10 Entry':'от 7 000 руб', 'Windows 10 Value':'от 7 000 руб',
     'Windows 10 Core':'8 699 руб', 'Windows 10 Core +':'8 699 руб', 'Windows 10 Core+':'8 699 руб',
     'Windows 10 Advanced':'от 7 000 руб', 'Windows 10 IoTCore':'от 7 000 руб', 'Windows 10 IoTMobile':'от 7 000 руб',
     'Windows 10 IoTEnterprise':'от 7 000 руб', 'Windows 10 IoTMobileEnterprise':'от 7 000 руб',
     'Windows 10 Мобильная корпоративная':'от 7 000 руб', 'Windows 8.1 Core':'5 480 руб', 'Windows 8.1 с Bing':'5 480 руб',
     'Windows 8.1 для одного языка':'5 480 руб', 'Windows 8.1':'5 480 руб', 'Windows 8':'5 480 руб',
     'Windows 10':'от 7 000 руб', 'Windows 10 Мобильная':'от 7 000 руб',
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
