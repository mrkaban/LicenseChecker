from __future__ import print_function
import io
import glob

def SearchKeys(path_file=''):
    word = ["Купить", "купить", "КУПИТЬ", "buy", "Buy", "BUY"]
    #word="купить"
    p={}
    sf=[]
    try:
        with io.open(path_file) as file: #errors='ignore'
            for element in word:
                for line in file:
                    if element in line:
                        p['key']=element
                        p['path']=path_file
    except:
        with io.open(path_file, encoding='utf-8') as file: #errors='ignore'
            for element in word:
                try:
                    for line in file:
                        if element in line:
                            p['key']=element
                            p['path']=path_file
                except UnicodeDecodeError: #return None
                        continue
                except PermissionError:
                        continue
                except FileNotFoundError:
                        continue
    return p

def StartSeachKey(path):
    files = glob.glob(path + "\**\*.txt", recursive=True) #txt, xml, ini, lng, lt
    files1 = glob.glob(path + "\**\*.ini", recursive=True)
    files2 = glob.glob(path + "\**\*.xml", recursive=True)
    files3 = glob.glob(path + "\**\*.lng", recursive=True)
    files4 = glob.glob(path + "\**\*.lt", recursive=True)
    d = []
    for element in files:
        if len(element) == 0:
            continue
        try:
            n = SearchKeys(element)
        except PermissionError:
            n = None
        try:
            if len(n) >=1:
                d.append(SearchKeys(element))
        except TypeError:
            continue
    for element in files1:
        if len(element) == 0:
            continue
        try:
            n = SearchKeys(element)
        except PermissionError:
            n = None
        try:
            if len(n) >=1:
                d.append(SearchKeys(element))
        except TypeError:
            continue
    for element in files2:
        if len(element) == 0:
            continue
        try:
            n = SearchKeys(element)
        except PermissionError:
            n = None
        try:
            if len(n) >=1:
                d.append(SearchKeys(element))
        except TypeError:
            continue
    for element in files3:
        if len(element) == 0:
            continue
        try:
            n = SearchKeys(element)
        except PermissionError:
            n = None
        try:
            if len(n) >=1:
                d.append(SearchKeys(element))
        except TypeError:
            continue
    for element in files4:
        if len(element) == 0:
            continue
        try:
            n = SearchKeys(element)
        except PermissionError:
            n = None
        try:
            if len(n) >=1:
                d.append(SearchKeys(element))
        except TypeError:
            continue
    return d

#StartSeachKey("D:\Public\LicenseChecker")
# try:
#     tt = StartSeachKey("C:\Program Files\\")
#     print(tt)
# except PermissionError:
#     print('Ошибка доступа')
#except UnicodeDecodeError:
#    print('Ошибка доступа')
#tt = StartSeachKey("C:\\Users\\mrKaban\\AppData\\")
#print(tt)
