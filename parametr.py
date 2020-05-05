from CheckOS import *
import sys
from reestr import foo #функция получения данных из реестра
import winreg #Нужна для работы со значением типа реестр
from filtr import filter #Фильтрация автопоиска
import sqlite3 #База данных SQLite
from datetime import datetime #какая дата и время
import socket #Для получения имени компьютера
import webbrowser #Для открытия веб-страницы
import os #Для поиска файлов


def AutoHidden(self=None):
    """Автопоиск при запуске с параметрами"""
    #Получаем данные из реестра в список(словари)
    software_list = foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY)+ foo(winreg.HKEY_CURRENT_USER, 0)
    #Добавляю ОС и стоимость
    name_os, cena_os = DetectOS()
    data = []
    data.append((name_os, 'Платное ПО', 'Shareware', cena_os))
    slovarSave = {}#Словарь для сохранения результатов поиска в HTML
    #Пробую работать с SQLite
    BaseLpro = sqlite3.connect(r"data\Lpro.db", uri=True)
    BaseLpro.row_factory = sqlite3.Row
    CurBLpro = BaseLpro.cursor()
    IntallPath = {}
    i = 2
    software_list = sorted(software_list, key=lambda x: x['name']) #Сортировка списка словарей в автопоиске
    n1 = [] #список для удаления дублей, в него добавляю, чтобы сравнить есть ли уже этот элемент
    for itemsoft in software_list:
        NameP=filter(itemsoft['name'])
        if NameP not in n1: #Удаляю дубли
            n1.append(NameP)
        else:
            continue #иначе переходим к следующей итеоации
        try:
            IntallPath[NameP] = itemsoft['InstallLocation']
        except:
            IntallPath[itemsoft['name']] = itemsoft['InstallLocation']
        s = 'SELECT * FROM program WHERE (name LIKE "' + NameP + '%%")'
        CurBLpro.execute(s)
        records = CurBLpro.fetchall()
        added = False
        for row in records:
            #tree.insert("" , i-1, text=i, values=(NameP, row[2], row[3], row[4]))
            h = row[4]
            h = h.replace("\n", "")
            data.append((NameP, row[2], row[3], h))
            slovarSave[NameP] = {'Name':NameP, 'TipPO':row[2], 'License':row[3], 'Cena':h}
            added = True
            break
        if added == False:
            #tree.insert("" , i-1, text=i, values=(itemsoft['name'], "Неизвестно", "Неизвестно", "???"))
            data.append((itemsoft['name'], "Неизвестно", "Неизвестно", "???"))
            slovarSave[NameP] = {'Name':NameP, 'TipPO':"Неизвестно", 'License':"Неизвестно", 'Cena':"???"}
        i += 1
    CurBLpro.close()
    BaseLpro.close()
    #Сохраняем отчет автопоиска в HTML
    SbHTML = """
    <html>
    <head>
    </head>
    <h1 align=center>Отчет автопоиска LicenseChecker</h1>"""
    SbHTML = SbHTML + '<h2 align=center>ПК: '+socket.gethostname() + ' в ' + datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S") +'</h1>'
    SbHTML = SbHTML + """
    <html>
    <table border=1 align=center>
    <tr><td> Название в БД
    <td> Тип ПО
    <td> Лицензия
    <td> Стоимость
    </tr>
    """
    s=''
    s1=''
    for itemsoft in slovarSave:
        s = slovarSave[itemsoft]
        s1 = '<tr><td> ' + s['Name'] + '\n' + '<td> ' + s['TipPO'] + '\n'
        s1 = s1 + '<td> ' + s['License'] + '\n' + '<td> ' + s['Cena'] + '\n'
        SbHTML = SbHTML + s1
    s2 = """
    </table>
    <p align=center>Официальный сайт: <a href="http://xn--90abhbolvbbfgb9aje4m.xn--p1ai/">КонтинентСвободы.рф</a></p>
    </html>
    """
    SbHTML = SbHTML + s2
    ftypes = [('HTML', '.html')] #Указываю тип расширение
    #options = QFileDialog.Options()
    #fileName = 'D:\\Public\\1.html'
    fileName = sys.argv[2]
    if fileName == 'default':
        sdf = socket.gethostname() + datetime.strftime(datetime.now(), "_%d-%m-%Y_%H-%M-%S")
        fileName = str(os.path.dirname(os.path.abspath(__file__))) +'\\' + 'auto_' + sdf +'.html'
    try:
        f = open(fileName,'w+')
        f.write(SbHTML) #Записываем в файл
        f.close()
    except:
        sdf = socket.gethostname() + datetime.strftime(datetime.now(), "_%d-%m-%Y_%H-%M-%S")
        fileName = str(os.path.dirname(os.path.abspath(__file__))) +'\\' + 'auto_' + sdf +'.html'
        f = open(fileName,'w+')
        f.write(SbHTML) #Записываем в файл
        f.close()
def RuchHidden(self=None):
    """Ручной поиск при запуске с параметрами"""
    slovarSave= {}
    size_list=[]
    dirlist = []
    dir = sys.argv[2]
    #dir = 'C:\\Program Files'
    spisok=[]
    slovar={}
    for root, dirs, files in os.walk(dir): # пройти по директории рекурсивно
        for name in files:
            if name[-4:]=='.exe':
                fullname = os.path.join(root, name) # получаем полное имя файла
                fullname = fullname.replace("/", "\\")
                slovar[name]=fullname
                spisok.append(name)
    BaseLproRuch = sqlite3.connect(r"data\Lpro.db", uri=True)
    BaseLproRuch.row_factory = sqlite3.Row #подключаем базу данных и курсор
    CurBLproRuch = BaseLproRuch.cursor()
    data = []
    added = False #Для отслеживания добавлен вариант из списка или нет
    for itemsoft in spisok: #В списке имена файлом с расширением exe
        NameP=itemsoft
        NamePF = NameP.replace((NameP[NameP.find('.exe'):]), '')
        s = 'SELECT * FROM program WHERE (file LIKE "' + NamePF + '")'
        CurBLproRuch.execute(s)
        records = CurBLproRuch.fetchall()
        for row in records:
            h = row[4]
            h = h.replace("\n", "")
            data.append((slovar[itemsoft], row[1], row[2], row[3], h))
            size_list.append(((len(slovar[itemsoft]))*6))
            #Создаю словари внутри словаря
            slovarSave[row[1]] = {'Address':slovar[itemsoft], 'Name':row[1], 'TipPO':row[2], 'License':row[3], 'Cena':row[4]}
            added = True
        if added == False:
            #Если не найдено в поле file, тогда ищем в поле name
            s = 'SELECT * FROM program WHERE (name LIKE "' + NamePF + '%%")'
            CurBLproRuch.execute(s)
            records = CurBLproRuch.fetchall()
            for row in records:
                h = row[4]
                h = h.replace("\n", "")
                data.append((slovar[itemsoft], row[1], row[2], row[3], h))
                size_list.append(((len(slovar[itemsoft]))*6))
                #Создаю словари внутри словаря
                slovarSave[row[1]] = {'Address':slovar[itemsoft], 'Name':row[1], 'TipPO':row[2], 'License':row[3], 'Cena':row[4]}
                added = True
    CurBLproRuch.close() #Закрываю соединение с базой и с курсором для базы
    BaseLproRuch.close()
    SbHTML = """
    <html>
    <head>
    </head>
    <h1 align=center>Отчет ручного поиска LicenseChecker</h1>"""
    SbHTML = SbHTML + '<h2 align=center>ПК: '+socket.gethostname() + ' в ' + datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S") +'</h1>'
    SbHTML = SbHTML + """
    <html>
    <table border=1 align=center>
    <tr><td> Название в БД
    <td> Путь
    <td> Тип ПО
    <td> Лицензия
    <td> Стоимость
    </tr>
    """
    s=''
    s1=''
    for itemsoft in slovarSave:
        s = slovarSave[itemsoft]
        s1 = '<tr><td> ' + s['Name'] + '\n' + '<td> ' + s['Address'] + '\n' + '<td> ' + s['TipPO'] + '\n'
        s1 = s1 + '<td> ' + s['License'] + '\n' + '<td> ' + s['Cena'] + '\n'
        SbHTML = SbHTML + s1
    s2 = """
    </table>
    <p align=center>Официальный сайт: <a href="http://xn--90abhbolvbbfgb9aje4m.xn--p1ai/">КонтинентСвободы.рф</a></p>
    </html>
    """
    SbHTML = SbHTML + s2
    ftypes = [('HTML', '.html')] #Указываю тип расширение
    fileName = sys.argv[3]
    if fileName == 'default':
        sdf = socket.gethostname() + datetime.strftime(datetime.now(), "_%d-%m-%Y_%H-%M-%S")
        fileName = str(os.path.dirname(os.path.abspath(__file__))) +'\\' + 'ruch_' + sdf +'.html'
    try:
        f = open(fileName,'w+')
        f.write(SbHTML) #Записываем в файл
        f.close()
    except:
        sdf = socket.gethostname() + datetime.strftime(datetime.now(), "_%d-%m-%Y_%H-%M-%S")
        fileName = str(os.path.dirname(os.path.abspath(__file__))) +'\\' + 'ruch_' + sdf +'.html'
        f = open(fileName,'w+')
        f.write(SbHTML) #Записываем в файл
        f.close()
