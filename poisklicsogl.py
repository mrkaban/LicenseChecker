import os
import re

def poisk_lic_sogl(dir):
    #spisok=[]
    # for root, dirs, files in os.walk(dir):
    #      # пройти по директории рекурсивно
    #      for name in files:
    #          if name[-4:]=='.exe':
    #              fullname = os.path.join(root, name) # получаем полное имя файла
    #              spisok.append(name)
    spisok=[]
    for root, dirs, files in os.walk(dir):
        for name in files:
            pattern=r'(License|EULA|COPYING|GPL)'
            search_exemple = re.search(pattern, name, re.M|re.I)
            if search_exemple:
                fullname = os.path.join(root, name)
                spisok.append(fullname)
    return spisok

if __name__ == "__main__":
    print(poisk_lic_sogl('C:\\Program Files\\7-Zip\\'))
