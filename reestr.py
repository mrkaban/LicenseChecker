import winreg

def foo(hive, flag):
    """Функция получения данных из реестра"""
    aReg = winreg.ConnectRegistry(None, hive)
    aKey = winreg.OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                          0, winreg.KEY_READ | flag)
    #print(aReg)
    count_subkey = winreg.QueryInfoKey(aKey)[0]
    software_list = []

    for i in range(count_subkey):
        software = {}
        try:
            asubkey_name = winreg.EnumKey(aKey, i)
            asubkey = winreg.OpenKey(aKey, asubkey_name)
            #print(asubkey_name)
            software['name'] = winreg.QueryValueEx(asubkey, "DisplayName")[0]
            try:
                software['version'] = winreg.QueryValueEx(asubkey, "DisplayVersion")[0]
            except EnvironmentError:
                software['version'] = 'undefined'
            try:
                software['publisher'] = winreg.QueryValueEx(asubkey, "Publisher")[0]
            except EnvironmentError:
                software['publisher'] = 'undefined'
            try:
                software['InstallLocation'] = winreg.QueryValueEx(asubkey, "InstallLocation")[0]
            #except EnvironmentError:
            except:
                try:
                    software['InstallLocation'] = winreg.QueryValueEx(asubkey, "InstallDir")[0]
                except:
                    try:
                        software['InstallLocation'] = winreg.QueryValueEx(asubkey, "DisplayIcon")[0]
                    except:
                        software['InstallLocation'] = 'undefined'
            #try:
            #    software['InstallLocation'] = winreg.QueryValueEx(asubkey, "InstallLocation")[0]
            #except EnvironmentError:
            #    software['InstallLocation'] = 'undefined'
            software_list.append(software)
        except EnvironmentError:
            continue

    return software_list
