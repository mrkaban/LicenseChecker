import requests
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QApplication, QHeaderView, QFileDialog
from PyQt5.QtCore import QRect, QCoreApplication, Qt, QMetaObject
from PyQt5.QtWidgets import QTableWidgetItem
from CheckOS import DetectOS, sled_activation, get_windows_product_key_from_reg
import sys
from reestr import foo #функция получения данных из реестра
import winreg #Нужна для работы со значением типа реестр
from filtr import filter #Фильтрация автопоиска
import sqlite3 #База данных SQLite
from datetime import datetime #какая дата и время
import socket #Для получения имени компьютера
import webbrowser #Для открытия веб-страницы
import os #Для поиска файлов
#Поиск слов купить и т.п. в папке с программой
from SearchKey import StartSeachKey
from poisklicsogl import poisk_lic_sogl
import urllib.request #для проверки наличия новых версий
from PyQt5.QtWidgets import QStyledItemDelegate #Для окрашивания строк
from PyQt5.QtGui import QColor#, QPalette #Для окрашивания строк
import configparser #для создания настроек
import parametr
#import io
import re
import glob
import platform
import requests


# Язык системы
import locale
try:
    #LanguageSystem = locale.getdefaultlocale()[0]
    LanguageSystem = 1 # ~!!!!!!!!!!!ggfg!!!!!!!!!!!!!dghgff!!!!!!!!!!!!!!!
except:
    LanguageSystem = 'Неизвестно'


app = QApplication([])
#пробую сделать графику основного окна в виде класса
class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        if LanguageSystem == 'ru_RU':
            uic.loadUi("data\\main.ui", self)
        else:
            uic.loadUi("data\\main-en.ui", self)
        self.setupUi(self)
        self.w = self.size().width()     # "определение ширины"
        self.h = self.size().height()   # "определение высоты"
    def resizeEvent(self, event):
        width =  self.size().width()
        height = self.size().height()

        koefW = width / self.w
        koefH = height / self.h

        s1 = int(90 * koefW)
        s2 = int(0 * koefH)
        s3 = int(831 * koefW)
        s4 = int(291 * koefH)
        self.tableWidget.setGeometry(s1, s2, s3, s4)
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(921, 336)
        self.tableWidget.setGeometry(QRect(90, 0, 831, 291))

        self.retranslateUi(Form)
        QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate

win = UI()

# изначально стиль брал только из файла, но из-за авторазмера окна закрыл
#win = uic.loadUi("data\\main.ui") #графика главного окна
#win.setFixedSize(801, 276) Это запрещает изменять размер основного окна

if LanguageSystem == 'ru_RU':
    winMore = uic.loadUi("data\\DoubleClick.ui") #графика подробности по двойному клику в автопоиске
    winPoiskZamen = uic.loadUi("data\\PoisZamen.ui") #графика поиск замен
    winSpravka = uic.loadUi("data\\Spravka.ui") #графика справка
    winViewBD = uic.loadUi("data\\ViewBD.ui") #графика поиск в базе
    winAbout = uic.loadUi("data\\About.ui") #графика О программе
    winRuchPoisk = uic.loadUi("data\\RuchPoisk.ui") #графика Ручной поиск
    winMediaPoisk = uic.loadUi("data\\Media.ui") #графика медиа поиск
    winSettings = uic.loadUi("data\\settings.ui") #графика медиа поиск
    mesNetFailaNastroek1 = 'Отсутствует файл настроек'
    mesNetFailaNastroek2 = 'Не удалось получить доступ к файлу settings.ini в папке с программой. Настройки будут перезаписаны на значения по умолчанию.'
else:
    winMore = uic.loadUi("data\\DoubleClick-en.ui") #графика подробности по двойному клику в автопоиске
    winPoiskZamen = uic.loadUi("data\\PoisZamen-en.ui") #графика поиск замен
    winSpravka = uic.loadUi("data\\Spravka-en.ui") #графика справка
    winViewBD = uic.loadUi("data\\ViewBD-en.ui") #графика поиск в базе
    winAbout = uic.loadUi("data\\About-en.ui") #графика О программе
    winRuchPoisk = uic.loadUi("data\\RuchPoisk-en.ui") #графика Ручной поиск
    winMediaPoisk = uic.loadUi("data\\Media-en.ui") #графика медиа поиск
    winSettings = uic.loadUi("data\\settings-en.ui") #графика медиа поиск
    mesNetFailaNastroek1 = 'Missing settings file'
    mesNetFailaNastroek2 = 'Failed to access the settings.ini file in the program folder. The settings will be overwritten with the default values.'

config = configparser.ConfigParser()
path = "data\\settings.ini"
config.read(path)
try:
    synhTest = config.get("Settings", "synh")
except:
    QMessageBox.critical(win, mesNetFailaNastroek1, mesNetFailaNastroek2)
    config.add_section("Settings")
    config.set("Settings", "synh", "off")
    config.set("Settings", "color_Avto_Text", "on")
    with open(path, "w") as config_file:
        config.write(config_file)

def Avtopoisk(self=None):
    """Автоматический поиск при запуске программы"""
    #Получаем данные из реестра в список(словари)
    software_list = foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY)+ foo(winreg.HKEY_CURRENT_USER, 0)
    #Добавляю ОС и стоимость
    name_os, cena_os = DetectOS()
    if LanguageSystem == 'ru_RU':
        cena_os = str(cena_os) + ' руб'
    else:
        hgf = cena_os // 70
        cena_os = '$' + str(hgf)
    
    data = []
    slovarSave = {}#Словарь для сохранения результатов поиска в HTML
    if LanguageSystem == 'ru_RU':
        data.append((name_os, 'Платное ПО', 'Shareware', cena_os, '-'))
        slovarSave[name_os] = {'Name':name_os, 'TipPO':"Платное ПО", 'License':"Shareware", 'Cena':cena_os, 'Zamena':"-"}
    else:
        data.append((name_os, 'Paid', 'Shareware', cena_os, '-'))
        slovarSave[name_os] = {'Name':name_os, 'TipPO':"Paid", 'License':"Shareware", 'Cena':cena_os, 'Zamena':"-"}
    #Пробую работать с SQLite
    BaseLpro = sqlite3.connect(r"data\Lpro.db", uri=True)
    BaseLpro.row_factory = sqlite3.Row
    CurBLpro = BaseLpro.cursor()
    IntallPath = {}
    i = 2
    software_list = sorted(software_list, key=lambda x: x['name']) #Сортировка списка словарей в автопоиске
    n1 = [] #список для удаления дублей, в него добавляю, чтобы сравнить есть ли уже этот элемент
    online_spisok = ''
    for itemsoft in software_list:
        NameP=filter(itemsoft['name'])
        if NameP not in n1: #Удаляю дубли
            n1.append(NameP)
        else:
            continue #иначе переходим к следующей итерации
        try:
            IntallPath[NameP] = itemsoft['InstallLocation']
        except:
            IntallPath[itemsoft['name']] = itemsoft['InstallLocation']
        s = 'SELECT * FROM program WHERE (name LIKE "' + NameP + '%%")'
        CurBLpro.execute(s)
        records = CurBLpro.fetchall()
        added = False
        tip4ikPO = ''
        for row in records:
            if LanguageSystem == 'ru_RU':
                # Цена
                if '0' == row[4] or 0 == row[4]:
                    h = 'Бесплатно'
                else:
                    if '~' in str(row[4]):
                        rep = row[4]
                        rep = rep.replace('~', '')
                        rep = float(rep)
                        ghj = rep * 70
                        jkl = round(ghj, 2)
                        h = 'от ' + str(jkl) + ' руб'
                    else:
                        ghj = row[4] * 70
                        jkl = round(ghj, 2)
                        h = str(jkl) + ' руб'
                # Тип
                tip4ikPO = row[2]
            else:
                # Цена
                if '0' == row[4] or 0 == row[4]:
                    #h = 'Free'
                    h = str(row[4])
                else:
                    if '~' in str(row[4]):
                        rep = str(row[4])
                        rep = rep.replace('~', '')
                        h = 'from $' + rep
                    else:
                        hgf = int(row[4])
                        h = '$' + str(hgf)
                # Тип
                tip4ikPO = row[2]
                if tip4ikPO == 'Свободная программа':
                    tip4ikPO = 'Libre'
                if tip4ikPO == 'Платное ПО':
                    tip4ikPO = 'Paid'
                if tip4ikPO == 'Условно-бесплатное ПО':
                    tip4ikPO = 'Free'
            data.append((NameP, tip4ikPO, row[3], h, row[5]))
            slovarSave[NameP] = {'Name':NameP, 'TipPO':tip4ikPO, 'License':row[3], 'Cena':h, 'Zamena':row[5]}
            added = True
            break
        if added == False:
            #tree.insert("" , i-1, text=i, values=(itemsoft['name'], "Неизвестно", "Неизвестно", "???"))

            # если программа неизвестна, ищем в онлайн базе
            #url = "https://www.mrkaban.ru/whatlic/" + NameP + "/"
            #url.replace(' ', '@-')
            # online_spisok = online_spisok + "::" + NameP
            #request1 = requests.get(url, allow_redirects=False)
            # k = request1.text
            # k = k.replace(' января ', '.01.')
            # g = re.search(r'([Обновлено: ]|[Опубликовано: ]|[Создано: ])+\d{2}[.]+\d{2}[.]+\d{4}', k)
            # if g is None:
            #     pass
            # else:
            #     j = g.group()
            #     j = j.replace('.', '-')
            if LanguageSystem == 'ru_RU':
                data.append((itemsoft['name'], "Неизвестно", "Неизвестно", "???", "-"))
                slovarSave[NameP] = {'Name':NameP, 'TipPO':"Неизвестно", 'License':"Неизвестно", 'Cena':"???", 'Zamena':"-"}
            else:
                data.append((itemsoft['name'], "Unknown", "Unknown", "???", "-"))
                slovarSave[NameP] = {'Name':NameP, 'TipPO':"Unknown", 'License':"Unknown", 'Cena':"???", 'Zamena':"-"}
            
        i += 1
    # try:
    #     url = "https://www.mrkaban.ru/whatlic/" + online_spisok + "/"
    #     request1 = requests.get(url, allow_redirects=False)
    # except:
    #     print("Ошибка")
    CurBLpro.close()
    BaseLpro.close()

    def DoubleClic():
        """подробности при двойном клике"""
        #winMore = uic.loadUi("DoubleClick.ui") #графика главного окна
        #winMore.setFixedSize(551, 281)
        try:
            for item in win.tableWidget.selectedIndexes():
            #print(win.tableWidget.item(item.row(), 0).text())
                s=win.tableWidget.item(item.row(), 0).text()
                #s = ([tree.item(x) for x in tree.selection()]) #Получаю выделенную строку
                #s = s[0] #вытаскиваю словарь из списка
        except IndexError:
            winMore.destroy()
            return False
        BaseDC = sqlite3.connect(r"data\Lpro.db", uri=True)
        BaseDC.row_factory = sqlite3.Row
        CurDC = BaseDC.cursor()
        edited_d = s
        edited_d = edited_d.replace('"', '') #Удаляю кавычки из запроса
        zapros = 'SELECT * FROM program WHERE (name LIKE "' + edited_d + '%%")'
        CurDC.execute(zapros)
        records = CurDC.fetchall()
        spisokExe = []
        spisokZamen = []
        for row in records:
            if row[6] == None:
                break
            g = row[6] + '.exe'
            spisokExe.append(g)
        for row in records:
            if row[5] == None:
                break
            k = row[5]
            spisokZamen.append(k)
        if LanguageSystem == 'ru_RU':
            TitleWinMore = s + " - Подробности"
            winMore.setWindowTitle(TitleWinMore)
            data=[]
            data.append(('Название:', s))
            data.append(('Тип ПО:', win.tableWidget.item(item.row(), 1).text()))
            data.append(('Лицензия:', win.tableWidget.item(item.row(), 2).text()))
            data.append(('Стоимость:', win.tableWidget.item(item.row(), 3).text()))
            k1 = 'Ключ Windows:'
            k2 = 'Следы активации:'
            k3 = 'Альтернативное ПО:'
            k4 = 'Не найдено'
            k5 = 'Путь:'
            k6 = 'Неизвестно'
            k7 = 'Подтверждение:'
            k8 = 'Поиск слов "Купить":'
            k9 = 'Лицензионное соглашение:'
            k10 = 'Корневой каталог приложения не указан'
            k11 = 'Пункт:'
            k12 = 'Параметр:'
        else:
            TitleWinMore = s + " - Details"
            winMore.setWindowTitle(TitleWinMore)
            data=[]
            data.append(('Name:', s))
            data.append(('Type:', win.tableWidget.item(item.row(), 1).text()))
            data.append(('License:', win.tableWidget.item(item.row(), 2).text()))
            data.append(('Price:', win.tableWidget.item(item.row(), 3).text()))
            k1 = 'Windows key:'
            k2 = 'Activation traces:'
            k3 = 'Alternative software:'
            k4 = 'Not found'
            k5 = 'Path:'
            k6 = 'Unknown'
            k7 = 'Confirmation:'
            k8 = 'Search words "Buy":'
            k9 = 'License agreement:'
            k10 = 'Application root directory not specified'
            k11 = 'Paragraph:'
            k12 = 'Parameter:'
        #Поиск ключа Windows и следов активации
        search_exemple = re.search( r'Windows', s, re.M|re.I)
        if search_exemple:
            data.append((k1, get_windows_product_key_from_reg()))
            i1 = 1
            i2 = 0
            sled_spisok = sled_activation()
            for sled in sled_spisok:
                if i1 <= i2:
                    data.append(('-', sled))
                    i1 += 1
                    i2 += 1
                else:
                    data.append((k2, sled))
                    i1 += 1
                    i2 = i1
        if not search_exemple:
            try:
                data.append((k3, spisokZamen[0]))
            except:
                data.append((k3, k4))
        if not search_exemple:
            try: #Заполняем путь из реестра
                s3 = IntallPath[s]
                search_file = re.search( r'.exe', s3, re.M|re.I)
                if search_file:
                    s3 = s3.replace('"', '')
                    s4 = os.path.basename(s3)#получаю имя файла
                    s3 = s3.replace(s4, '') # Удаляю имя файла из пути
                else:
                    s3 = s3.replace('"', '')
                if os.path.exists(s3) or os.path.isfile(s3):
                    data.append((k5, s3))
            #data.append(('Путь:', IntallPath[s]))
                if s3 == 'undefined':
                    bit = platform.win32_is_iot()
                    try:
                        if bit:
                            putishko = glob.glob('C:\\Program Files\\**\\'+spisokExe[0], recursive=True)
                            for el in putishko:
                                data.append((k5, el))
                        else:
                            putishko = glob.glob('C:\\Program Files\\**\\'+spisokExe[0], recursive=True)
                            putishko1 = glob.glob('C:\\Program Files (x86)\\**\\'+spisokExe[0], recursive=True)
                            for el in putishko:
                                data.append((k5, el))
                            for el in putishko1:
                                data.append((k5, el))
                    except:
                        data.append((k5, k6))
            except KeyError: #если в реестре он не указан
                data.append((k5, k6))
            try:#Ищим основной исполняемый для подтверждения
                dir = IntallPath[s] + '\\' #IndexError:
                dir = dir.replace("/", "\\")
                dir = dir.replace("\\\\", "\\")
                for root1, dirs, files in os.walk(dir):
                # пройти по директории рекурсивно
                    for name in files:
                        if name==spisokExe[0]:
                            fullname = os.path.join(root1, name) # получаем полное имя файла
                            if os.path.exists(fullname):
                                data.append((k7, fullname))
            except KeyError:
                data.append((k7, k4))
            except IndexError:
                data.append((k7, k4))
        if not search_exemple:
            try:#поиск слов купить, как доп вариант опознавания платных программ
                if (len(IntallPath[s]))>2:
                    h=StartSeachKey(IntallPath[s])
                    h1 = h[0]
                    data.append((k8, h1['path']))
                else:
                    data.append((k8, k4))
            except:
                data.append((k8, k4))
        if not search_exemple:
        #Поиск лицензионного соглашения
            try:
                if (len(IntallPath[s])) > 0:
                    spisok_lic_sogl = poisk_lic_sogl(IntallPath[s])
                    i1=1
                    i2 = 0
                    for lic_sogl in spisok_lic_sogl:
                        if i1 <= i2:
                            data.append(('-', lic_sogl))
                            i1 += 1
                            i2 += 1
                        else:
                            data.append((k9, lic_sogl))
                            i1 += 1
                            i2 = i1
                else:
                    data.append((k9, k4))
            except KeyError:
                data.append((k9, k10))

        winMore.tableWidget.setRowCount(len(data))
        winMore.tableWidget.setColumnCount(2)
        winMore.tableWidget.setHorizontalHeaderLabels(
                (k11, k12))
        row = 0
        for tup in data:
            col = 0
            for item in tup:
                cellinfo = QTableWidgetItem(item)
                cellinfo.setFlags(
                            Qt.ItemIsSelectable | Qt.ItemIsEnabled
                        )
                winMore.tableWidget.setItem(row, col, cellinfo)
                col += 1

            row += 1
        winMore.tableWidget.resizeColumnsToContents()
        winMore.tableWidget.setColumnWidth(2, 50)
        winMore.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)


        try:
            if 351<=((len(h1['path']))*6):
                size1 = (len(h1['path']))*6 #пробую задать ширину окна по содержимому
            else:
                size1 = 351
        except:
            try:
                if 351<=((len(h1['path']))*6):
                    size1 = (len(IntallPath[s]))*6
                else:
                    size1 = 351
            except:
                size1 = 351
        winMore.resize(size1+200, 295)
        winMore.tableWidget.resize(size1+200, 295)
        x = size1+200
        #y = 281
        #winMore.move(x, y)
        winMore.setFixedSize(x, 295)
        CurDC.close()
        BaseDC.close()
        winMore.show()

    def SaveAvto():
        """Сохранить отчет автопоиска в HTML"""
        if LanguageSystem == 'ru_RU':
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
            <td> Замена
            </tr>
            """
        else:
            SbHTML = """
            <html>
            <head>
            </head>
            <h1 align=center>LicenseChecker auto-search report</h1>"""
            SbHTML = SbHTML + '<h2 align=center>PC: '+socket.gethostname() + ' at ' + datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S") +'</h1>'
            SbHTML = SbHTML + """
            <html>
            <table border=1 align=center>
           <tr><td> Database name
             <td> Software type
             <td> License
             <td> Cost
             <td> Replacement
            </tr>
            """
        s=''
        s1=''
        for itemsoft in slovarSave: # Zamena
            s = slovarSave[itemsoft]
            s1 = '<tr><td> ' + s['Name'] + '\n' + '<td> ' + s['TipPO'] + '\n'
            s1 = s1 + '<td> ' + s['License'] + '\n' + '<td> ' + str(s['Cena']) + '\n'
            s1 = s1 + '<td> ' + s['Zamena'] + '\n'
            SbHTML = SbHTML + s1
        if LanguageSystem == 'ru_RU':    
            s2 = """
            </table>
            <p align=center>Официальный сайт: <a href="https://xn--90abhbolvbbfgb9aje4m.xn--p1ai/">КонтинентСвободы.рф</a></p>
            </html>
            """
            sk1 = 'Файл сохранен'
            sk2 = 'Файл успешно сохранен: '
            sk3 = 'Не удалось сохранить файл:'
            sk4 = 'Не удалось сохранить файл отчета.'
            sk5 = 'Укажите куда необходимо сохранить отчет?'
        else:
            s2 = """
            </table>
            <p align=center>Official site: <a href="https://openwinsoft.org/">openwinsoft.org</a></p>
            </html>
            """
            sk1 = 'File saved'
            sk2 = 'File saved successfully: '
            sk3 = 'Failed to save file:'
            sk4 = 'Failed to save log file.'
            sk5 = 'Where do you want to save the report?'
        SbHTML = SbHTML + s2
        #ftypes = [('HTML', '.html')] #Указываю тип расширение
        options = QFileDialog.Options()
        fileName = QFileDialog.getSaveFileName(self,sk5,".html","HTML (*.html)", options=options)
        try:
            f = open(fileName[0],'w+')
            f.write(SbHTML) #Записываем в файл
            f.close()
            QMessageBox.about(self, sk1, sk2 + fileName[0])
        except:
            QMessageBox.critical(win, sk3, sk4)
            #QMessageBox.about(self, "Не удалось сохранить", "Не удалось сохранить файл: " + fileName[0])
    #Добавляем действия к пунктам меню
    win.mSaveAvto.triggered.connect(SaveAvto)
    win.tableWidget.doubleClicked.connect(DoubleClic)

    win.tableWidget.setGeometry(QRect(90, 0, 831, 291))
    win.tableWidget.setGeometry(QRect(90, 0, 831, 291))
    win.tableWidget.setRowCount(len(data))
    win.tableWidget.setColumnCount(5)
    if LanguageSystem == 'ru_RU':
        win.tableWidget.setHorizontalHeaderLabels(
                ('Название:', 'Тип:', 'Лицензия:', '~Цена:', 'Замена:')
            )
    else:
        win.tableWidget.setHorizontalHeaderLabels(
                ('Name:', 'Type:', 'License:', '~Price:', 'Replacement:')
            )
    row = 0
    for tup in data:
        col = 0
        for item in tup:
            cellinfo = QTableWidgetItem(item)
            cellinfo.setFlags(
                        Qt.ItemIsSelectable | Qt.ItemIsEnabled
                    )
            win.tableWidget.setItem(row, col, cellinfo)
            col += 1

        row += 1
    win.tableWidget.resizeColumnsToContents()
    win.tableWidget.setColumnWidth(1, 150)
    win.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
    #Меня цвет строк
    if LanguageSystem == 'ru_RU':
        class ColorDelegate(QStyledItemDelegate):
            def paint(self, painter, option, index):
                if index.data() == 'Свободная программа':
                    for j in range(win.tableWidget.columnCount()):
                        #print(index.row())
                        win.tableWidget.item(index.row(), j).setForeground(QColor("green"))
                elif index.data() == 'Платное ПО':
                    for j in range(win.tableWidget.columnCount()):
                        win.tableWidget.item(index.row(), j).setForeground(QColor("red"))
                elif index.data() == 'Условно-бесплатное ПО':
                    for j in range(win.tableWidget.columnCount()):
                        win.tableWidget.item(index.row(), j).setForeground(QColor(192, 162, 17))
                QStyledItemDelegate.paint(self, painter, option, index)
    else:
        class ColorDelegate(QStyledItemDelegate):
            def paint(self, painter, option, index):
                if index.data() == 'Libre':
                    for j in range(win.tableWidget.columnCount()):
                        win.tableWidget.item(index.row(), j).setForeground(QColor("green"))
                elif index.data() == 'Free':
                    for j in range(win.tableWidget.columnCount()):
                        #print(index.data())
                        win.tableWidget.item(index.row(), j).setForeground(QColor(192, 162, 17))
                elif index.data() == 'Paid':
                    for j in range(win.tableWidget.columnCount()):
                        #print(index.row())
                        win.tableWidget.item(index.row(), j).setForeground(QColor("red"))

                QStyledItemDelegate.paint(self, painter, option, index)

    color_Avto_Text = config.get("Settings", "color_Avto_Text")
    if color_Avto_Text == 'on': #Если окраска включена в настройках, тогда окрашиваем
        win.tableWidget.setItemDelegate(ColorDelegate())



#Заполняю пункты меню
def close_win(): #Вкладка Файл \ Выход
    """Закрываем окно"""
    sys.exit()
win.mExit.triggered.connect(close_win)
def WebStr(self=None): #Вкладка ? \ Официальный сайт
    """открытие веб-страницы в браузере по умолчанию"""
    if LanguageSystem == 'ru_RU':
        webstranichka = 'https://xn--90abhbolvbbfgb9aje4m.xn--p1ai/%D1%83%D1%82%D0%B8%D0%BB%D0%B8%D1%82%D1%8B/%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0/licensechecker-%D0%BB%D0%B5%D0%B3%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D1%81%D1%82%D1%8C-%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC.html'
    else:
        webstranichka = 'https://openwinsoft.org/licensechecker/'
    webbrowser.open_new_tab(webstranichka)
win.mWebStr.triggered.connect(WebStr)
def WebHelp():
    """открытие веб-страницы в браузере по умолчанию"""
    webbrowser.open_new_tab("https://github.com/mrkaban/LicenseChecker/issues")
win.mWebHelp.triggered.connect(WebHelp)

def Pozhertv():
    """открытие веб-страницы для пожертвований на развитие программы"""
    webbrowser.open_new_tab("https://money.yandex.ru/to/410011359577019")
win.mPozhertv.triggered.connect(Pozhertv)

def Settings():
    """Настройки программы"""
    synh = config.get("Settings", "synh")
    color_Avto_Text = config.get("Settings", "color_Avto_Text")
    if synh == 'on':
        winSettings.rbSynhOn.setChecked(True)
    if synh == 'off':
        winSettings.rbSynhOff.setChecked(True)
    if color_Avto_Text == 'on':
        winSettings.rbColorAvtoTextOn.setChecked(True)
    if color_Avto_Text == 'off':
        winSettings.rbColorAvtoTextOff.setChecked(True)
    winSettings.setFixedSize(361, 292)
    def KnopkaOk():
        """Кнопка Ok"""
        if winSettings.rbSynhOn.isChecked():
            config.set("Settings", "synh", "on") # Меняем значения из конфиг. файла.
        else:
            config.set("Settings", "synh", "off")
        if winSettings.rbColorAvtoTextOn.isChecked():
            config.set("Settings", "color_Avto_Text", "on")
        else:
            config.set("Settings", "color_Avto_Text", "off")
        with open(path, "w") as config_file: # Вносим изменения в конфиг. файл.
            config.write(config_file)
        winSettings.close()
    winSettings.pbOk.clicked.connect(KnopkaOk)
    def KnopkaOtmena():
        """Кнопка Отмена"""
        winSettings.close()
    winSettings.pbOtmena.clicked.connect(KnopkaOtmena)
    def KnopkaPrimenit():
        """Кнопка Отмена"""
        if winSettings.rbSynhOn.isChecked():
            config.set("Settings", "synh", "on") # Меняем значения из конфиг. файла.
        else:
            config.set("Settings", "synh", "off")
        if winSettings.rbColorAvtoTextOn.isChecked():
            config.set("Settings", "color_Avto_Text", "on")
        else:
            config.set("Settings", "color_Avto_Text", "off")
        with open(path, "w") as config_file: # Вносим изменения в конфиг. файл.
            config.write(config_file)
    winSettings.pbPrimenit.clicked.connect(KnopkaPrimenit)
    winSettings.show()
win.mSettings.triggered.connect(Settings)

def PoiskZamen():
    """Поиск замены на сайте КонтинентСвободы.рф"""
    winPoiskZamen.setFixedSize(587, 230)
    def KnopkaPoiskDliaZamen():
        """Кнопка поиск замен"""
        textp = winPoiskZamen.leKluch.text()
        if textp == None or textp == '':
            return True
        if textp.find(" ", 0, len(textp)) >= 1: #Только отдельно, удаление кавычек
             textp = textp.replace(" ", '+')
        if LanguageSystem == 'ru_RU':
            url_kluch = 'https://xn--90abhbolvbbfgb9aje4m.xn--p1ai/search/?s='+textp
        else:
            url_kluch = 'https://openwinsoft.org/search/?s='+textp
        webbrowser.open_new_tab(url_kluch)
    winPoiskZamen.pbPosik.clicked.connect(KnopkaPoiskDliaZamen)
    winPoiskZamen.leKluch.returnPressed.connect(KnopkaPoiskDliaZamen)
    winPoiskZamen.show()
win.mPoiskZameni.triggered.connect(PoiskZamen)
def Spravka():
    """Справка о программе"""
    winSpravka.setFixedSize(463, 301)
    winSpravka.show()
win.mSpravka.triggered.connect(Spravka)
def UpdateProg():
    """проверка наличия новой версии программы"""
    try:
        f = urllib.request.urlopen("https://github.com/mrkaban/LicenseChecker/raw/master/version")
        h = str(f.read())
    except:
        #QMessageBox.about(self, "Файл сохранен", "Файл успешно сохранен: " + fileName[0])
        if LanguageSystem == 'ru_RU':
            QMessageBox.critical(win, "Нет соединения с сервером", "Не удалось проверить наличие обновлений.")
        else:
            QMessageBox.critical(win, "No connection to server", "Failed to check for updates.")
        return
    search_exemple = re.search(r'1.8', h, re.M|re.I)
    """!!!!!!!!!!!!!!!!ТУТ НАДО ИСПРАВИТЬ ВЕРСИЮ ПРОГРАММЫ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""
    if not search_exemple:
        if LanguageSystem == 'ru_RU':
            try:
                QMessageBox.about(win, "Обнаружена новая версия", "Сейчас будет открыта веб-страница с доступными релизами.\
    Скачайте подходящую для Вас версию. Если не получается найти файлы, нажмите на \'Assets\'.")
                webbrowser.open_new_tab("https://github.com/mrkaban/LicenseChecker/releases")
            except:
                QMessageBox.critical(win, "Не получилось открыть страницу", "Не получилось открыть ссылку в веб-браузере.")
                return
        else:
            try:
                 QMessageBox.about(win, "New version found", "A web page with available releases will now open.\
     Download the version that suits you. If you can't find the files, click on \'Assets\'.")
                 webbrowser.open_new_tab("https://github.com/mrkaban/LicenseChecker/releases")
            except:
                 QMessageBox.critical(win, "Could not open page", "Could not open link in web browser.")
                 return
    else:
        if LanguageSystem == 'ru_RU':
            QMessageBox.about(win, "Программа актуальна", "Используемая Вами версия программы актуальна.")
        else:
            QMessageBox.about(win, "The program is up to date", "The version of the program you are using is up to date.")
win.mUpdateProg.triggered.connect(UpdateProg)
def UpdateBase():
    """Обновление базы данных Lpro.db"""
    BaseUpdateBase = sqlite3.connect(r"data\Lpro.db", uri=True)
    BaseUpdateBase.row_factory = sqlite3.Row #подключаем базу данных и курсор
    CurUpdateBase = BaseUpdateBase.cursor()
    s1 = 'SELECT * FROM version WHERE date'
    CurUpdateBase.execute(s1)
    records = CurUpdateBase.fetchall()
    try:
        f = urllib.request.urlopen("https://github.com/mrkaban/LicenseChecker/raw/master/lpro-base-version.txt")
        h = str(f.read())
        h = h.replace("'", "")
        h = h.replace("b", "")
    except:
        if LanguageSystem == 'ru_RU':
            QMessageBox.critical(win, "Нет соединения с сервером", "Не удалось проверить наличие обновлений базы данных.")
        else:
            QMessageBox.critical(win, "No connection to server", "Failed to check for database updates.")
        return
    if LanguageSystem == 'ru_RU':
        uk1 = 'База обновлена'
        uk2 = 'База данных успешно обновлена до версии '
        uk3 = 'Не удалось загрузить БД'
        uk4 = 'Не удалось загрузить базу данных.'
        uk5 = 'Не удалось синхронизировать БД'
        uk6 = 'Не удалось синхронизировать пользовательскую\
базу данных с основной. Проверьте наличие файла data\\User-DB.db в папке с программой.'
        uk7 = 'Синхронизация успешно завершена'
        uk8 = 'Пользовательская база данных успешно синхронизиррована с основной базой.'
        uk9 = 'База данных актуальна'
        uk10 = 'Обновление базы данных не требуется.'
    else:
        uk1 = 'Database updated'
        uk2 = 'Database upgraded successfully to '
        uk3 = 'Failed to load database'
        uk4 = 'Failed to load database.'
        uk5 = 'Failed to sync database'
        uk6 = 'Failed to sync user\
database with main. Check for the presence of the data\\User-DB.db file in the program folder.'
        uk7 = 'Sync completed successfully'
        uk8 = 'The user database has been successfully synchronized with the main database.'
        uk9 = 'Database up to date'
        uk10 = 'No database update required.'
    for row in records:
        g = str(row[0])
        g = g.replace(" ", "")
        try:
            h = g.replace("\n", "")
        except:
            pass
        if g != h:
            try:
                bd1 = urllib.request.urlopen("https://github.com/mrkaban/LicenseChecker/raw/master/Lpro.db").read()
                f = open("data\\Lpro.db", "wb")
                f.write(bd1)
                f.close()
                QMessageBox.about(win, uk1, uk2 + h)
            except:
                QMessageBox.critical(win, uk3, uk4)
                break
            synh = config.get("Settings", "synh")
            if synh != 'off':
                #синхронизируем пользовательскую базу данных
                sinh = False
                try:
                    BaseUserSinh = sqlite3.connect(r"data\User-DB.db", uri=True)
                    BaseUserSinh.row_factory = sqlite3.Row #подключаем базу данных и курсор
                    CurUserSinh = BaseUserSinh.cursor()
                    s = 'SELECT * FROM UserProgram'
                    CurUserSinh.execute(s)
                    records = CurUserSinh.fetchall()
                    zapis_v_lpro = []
                    r = 20000
                    for row in records:
                        f = (r, row[0], row[1], row[2], row[3], row[4], row[5])
                        zapis_v_lpro.append(f)
                        r = r + 1
                    CurUpdateBase.executemany("INSERT INTO program VALUES (?,?,?,?,?,?,?)", zapis_v_lpro)
                    BaseUpdateBase.commit()
                    sinh = True
                except:
                    QMessageBox.critical(win, uk5, uk6)
                    sinh = False
                if sinh == True:
                    QMessageBox.about(win, uk7, uk8)
        else:
            QMessageBox.about(win, uk9, uk10)
    CurUpdateBase.close() #Закрываю соединение с базой и с курсором для базы
    BaseUpdateBase.close()
win.mUpdateBase.triggered.connect(UpdateBase)

def ViewBD():
    """Поиск и просмотр базы данных"""
    #if textbd == None or textbd == '': если поле пусто, завершить функцию
    #    return True
    size2 = None
    def ViewBDDlyaKnopki(event=None):
        """Функция для кнопки поиск"""
        name_user_prog =winViewBD.leKluchBD.text()
        winViewBD.tableWidgetBD.clear()
        BaseLproVDB = sqlite3.connect(r"data\Lpro.db", uri=True)
        BaseLproVDB.row_factory = sqlite3.Row #подключаем базу данных и курсор
        CurBLproVDB = BaseLproVDB.cursor()
        s = 'SELECT * FROM program WHERE (name LIKE "%%' + name_user_prog + '%%")'
        CurBLproVDB.execute(s)
        records = CurBLproVDB.fetchall()
        size_list=[]
        dataBD = []
        global size2
        #size2 = None
        tip4ikPO = ''
        added = False
        i = 1
        for row in records:
            size2= 0
            if LanguageSystem == 'ru_RU':
                # Цена
                if '0' == row[4] or 0 == row[4]:
                    h = 'Бесплатно'
                else:
                    if '~' in str(row[4]):
                        rep = row[4]
                        rep = rep.replace('~', '')
                        rep = float(rep)
                        ghj = rep * 70
                        jkl = round(ghj, 2)
                        h = 'от ' + str(jkl) + ' руб'
                    else:
                        ghj = row[4] * 70
                        jkl = round(ghj, 2)
                        h = str(jkl) + ' руб'
                # Тип
                tip4ikPO = row[2]
            else:
                # Цена
                if '0' == row[4] or 0 == row[4]:
                    h = 'Free'
                else:
                    if '~' in str(row[4]):
                        rep = str(row[4])
                        rep = rep.replace('~', '')
                        h = 'from $' + rep
                    else:
                        hgf = int(row[4])
                        h = '$' + str(hgf)
                # Тип
                tip4ikPO = row[2]
                if tip4ikPO == 'Свободная программа':
                    tip4ikPO = 'Libre'
                if tip4ikPO == 'Платное ПО':
                    tip4ikPO = 'Paid'
                if tip4ikPO == 'Условно-бесплатное ПО':
                    tip4ikPO = 'Free'
            # h = row[4]
            h = h.replace("\n", "")
            dataBD.append((row[1], tip4ikPO, row[3], h))
            size_list.append(((len(row[1]))*6))
            added = True
            i += 1

            if added == False:
                i = i -1
        CurBLproVDB.close() #Закрываю соединение с базой и с курсором для базы
        BaseLproVDB.close()

        for itemsize in size_list:
            if size2 <= int(itemsize):
                size2 = int(itemsize)
        if size2 == None:
            size2 = 300
        if size2 < 300:
            size2 = 300
        winViewBD.tableWidgetBD.setRowCount(len(dataBD))
        winViewBD.tableWidgetBD.setColumnCount(4)
        if LanguageSystem == 'ru_RU':
            winViewBD.tableWidgetBD.setHorizontalHeaderLabels(
                    ('Название:', 'Тип:', 'Лицензия:', '~Цена:')
                )
        else:
            winViewBD.tableWidgetBD.setHorizontalHeaderLabels(
                 ('Name:', 'Type:', 'License:', '~Price:')
             )
        row = 0
        for tup in dataBD:
            col = 0
            for item in tup:
                cellinfo = QTableWidgetItem(item)
                cellinfo.setFlags(
                            Qt.ItemIsSelectable | Qt.ItemIsEnabled
                        )
                winViewBD.tableWidgetBD.setItem(row, col, cellinfo)
                col += 1

            row += 1
        winViewBD.tableWidgetBD.resizeColumnsToContents()
        winViewBD.tableWidgetBD.setColumnWidth(1, 150)
        winViewBD.tableWidgetBD.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

    winViewBD.pbPoiskBD.clicked.connect(ViewBDDlyaKnopki)
    winViewBD.leKluchBD.returnPressed.connect(ViewBDDlyaKnopki)
    
    if size2 == None:
        size2 = 300
    winViewBD.tableWidgetBD.resizeColumnsToContents()
    winViewBD.resize(size2+410, 270)
    winViewBD.tableWidgetBD.resize(size2+321, 201)
    x = size2+410
    #y = 270
    #winViewBD.move(x, y)
    winViewBD.setFixedSize(x, 270)
    #winViewBD.setFixedSize(710, 270)
    winViewBD.show()
win.mViewBD.triggered.connect(ViewBD)
def About():
    """Окно о программе"""
    winAbout.setFixedSize(424, 241)
    winAbout.show()
win.mAbout.triggered.connect(About)
def RuchPoisk():
    """Ручной поиск программ"""
    winRuchPoisk.setFixedSize(891, 289)
    slovarSave= {}
    size_list=[]
    #size1 = None
    
    if LanguageSystem == 'ru_RU':
        msgruch1 = "Указать 1 каталог"
        msgruch2 = "Список exe, msi, rar и zip"
        msgruch3 = "Указать каталог для поиска остатков программ"
        msgruch4 = "Указать 2 каталога"
        msgruch5 = "Указать первый каталог для поиска остатков программ"
        msgruch6 = "Указать второй каталог для поиска остатков программ"
        msgruch7 = "Указать 3 каталога"
        msgruch8 = "Указать первый каталог для поиска остатков программ"
        msgruch9 = "Указать второй каталог для поиска остатков программ"
        msgruch10 = "Указать третий каталог для поиска остатков программ"
        msgruch11 = "Указать 1 каталог"
        msgruch12 = "Список exe, msi, rar и zip"
        msgruch13 = "Указать 2 каталога"
        msgruch14 = "Ошибка"
        msgruch15 = "Вручную можно указать только 1 каталог."
        msgruch16 = "Указать 3 каталога"
        msgruch17 = "Список exe, msi, rar и zip"
        msgruch18 = "МБ"
        msgruch19 = 'Неизвестно'
    else:
        msgruch1 = "Specify 1 directory"
        msgruch2 = "List exe, msi, rar and zip"
        msgruch3 = "Specify directory to search for program leftovers"
        msgruch4 = "Specify 2 directories"
        msgruch5 = "Specify the first directory to search for program leftovers"
        msgruch6 = "Specify a second directory to search for program leftovers"
        msgruch7 = "Specify 3 directories"
        msgruch8 = "Specify the first directory to search for program leftovers"
        msgruch9 = "Specify a second directory to search for program leftovers"
        msgruch10 = "Specify a third directory to search for program leftovers"
        msgruch11 = "Specify 1 directory"
        msgruch12 = "List exe, msi, rar and zip"
        msgruch13 = "Specify 2 directories"
        msgruch14 = "Error"
        msgruch15 = "You can only specify 1 directory manually."
        msgruch16 = "Specify 3 directories"
        msgruch17 = "List exe, msi, rar and zip"
        msgruch18 = "MB"
        msgruch19 = 'Unknown'
    
    dirlist = []
    def OpenKatalog():
        """Открыть каталог"""
        try:
            PredKatalog = winRuchPoisk.leKatalog.text()
            try:
                nachalo = PredKatalog.find(' ')
                konets = len(PredKatalog)
                PredKatalog.replace(PredKatalog[nachalo:konets], '')
            except:
                pass
        except:
            PredKatalog = "."
        winRuchPoisk.leKatalog.setText("")
        winRuchPoisk.tableWidgetRuch.clear()
        dirlist.clear()
        opt1 = winRuchPoisk.cbOptions.currentText()
        #if winRuchPoisk.rb1kat.isChecked():
        if opt1 == msgruch1 or opt1 == msgruch2:
            d = QFileDialog.getExistingDirectory(winRuchPoisk, msgruch3, PredKatalog)
            dirlist.append(d)
            winRuchPoisk.leKatalog.setText(dirlist[0])
        #if winRuchPoisk.rb2kat.isChecked():
        if opt1 == msgruch4:
            d = QFileDialog.getExistingDirectory(winRuchPoisk, msgruch5, PredKatalog)
            dirlist.append(d)
            d = QFileDialog.getExistingDirectory(winRuchPoisk, msgruch6, PredKatalog)
            dirlist.append(d)
            winRuchPoisk.leKatalog.setText(dirlist[0] + ' ' + dirlist[1])
        #if winRuchPoisk.rb3kat.isChecked():
        if opt1 == msgruch7:
            d = QFileDialog.getExistingDirectory(winRuchPoisk, msgruch8, PredKatalog)
            dirlist.append(d)
            d = QFileDialog.getExistingDirectory(winRuchPoisk, msgruch9, PredKatalog)
            dirlist.append(d)
            d = QFileDialog.getExistingDirectory(winRuchPoisk, msgruch10, PredKatalog)
            dirlist.append(d)
            winRuchPoisk.leKatalog.setText(dirlist[0] + ' ' + dirlist[1] + ' ' + dirlist[2])
    winRuchPoisk.pbObzor.clicked.connect(OpenKatalog)
    def ButtonRuchPoisk():
        """Функция для кнопки поиск"""
        winRuchPoisk.tableWidgetRuch.clear()
        spisok=[]
        spisokExeVseh = []
        slovar={}
        slovarSave.clear()
        opt2 = winRuchPoisk.cbOptions.currentText()
        try:
            if dirlist[0] == '' or dirlist[0] == None:
                if not(os.path.exists(winRuchPoisk.leKatalog.text())):
                    return
        except IndexError:
            if not(os.path.exists(winRuchPoisk.leKatalog.text())):
                return
        #if winRuchPoisk.rb1kat.isChecked():
        if opt2 == msgruch11 or opt2 == msgruch12:
            try:
                dir = dirlist[0]
            except:
                dir = winRuchPoisk.leKatalog.text()
            for root, dirs, files in os.walk(dir): # пройти по директории рекурсивно
                 for name in files:
                     if name[-4:]=='.exe' or name[-4:]=='.msi':
                         fullname = os.path.join(root, name) # получаем полное имя файла
                         fullname = fullname.replace("/", "\\")
                         slovar[name]=fullname
                         spisok.append(name)
                         spisokExeVseh.append({name:fullname})
                     if name[-4:]=='.rar' or name[-4:]=='.zip':
                         fullname = os.path.join(root, name) # получаем полное имя файла
                         fullname = fullname.replace("/", "\\")
                         slovar[name]=fullname
                         spisok.append(name)
                         spisokExeVseh.append({name:fullname})
        #if winRuchPoisk.rb2kat.isChecked():
        if opt2 == msgruch13:
            try:
                dir = dirlist[0]
            except:
                QMessageBox.critical(winRuchPoisk, msgruch14, msgruch15)
                return
            for root, dirs, files in os.walk(dir): # пройти по директории рекурсивно
                for name in files:
                    if name[-4:]=='.exe' or name[-4:]=='.msi':
                        fullname = os.path.join(root, name) # получаем полное имя файла
                        fullname = fullname.replace("/", "\\")
                        slovar[name]=fullname
                        spisok.append(name)
                        spisokExeVseh.append({name:fullname})
                    if name[-4:]=='.rar' or name[-4:]=='.zip':
                        fullname = os.path.join(root, name) # получаем полное имя файла
                        fullname = fullname.replace("/", "\\")
                        slovar[name]=fullname
                        spisok.append(name)
                        spisokExeVseh.append({name:fullname})
            dir = dirlist[1]
            for root, dirs, files in os.walk(dir): # пройти по директории рекурсивно
                for name in files:
                    if name[-4:]=='.exe' or name[-4:]=='.msi':
                        fullname = os.path.join(root, name) # получаем полное имя файла
                        fullname = fullname.replace("/", "\\")
                        slovar[name]=fullname
                        spisok.append(name)
                        spisokExeVseh.append({name:fullname})
                    if name[-4:]=='.rar' or name[-4:]=='.zip':
                        fullname = os.path.join(root, name) # получаем полное имя файла
                        fullname = fullname.replace("/", "\\")
                        slovar[name]=fullname
                        spisok.append(name)
                        spisokExeVseh.append({name:fullname})
        #if winRuchPoisk.rb3kat.isChecked():
        if opt2 == msgruch16:
            try:
                dir = dirlist[0]
            except:
                QMessageBox.critical(winRuchPoisk, msgruch14, msgruch15)
                return
            for root, dirs, files in os.walk(dir): # пройти по директории рекурсивно
                for name in files:
                    if name[-4:]=='.exe' or name[-4:]=='.msi':
                        fullname = os.path.join(root, name) # получаем полное имя файла
                        fullname = fullname.replace("/", "\\")
                        slovar[name]=fullname
                        spisok.append(name)
                        spisokExeVseh.append({name:fullname})
                    if name[-4:]=='.rar' or name[-4:]=='.zip':
                        fullname = os.path.join(root, name) # получаем полное имя файла
                        fullname = fullname.replace("/", "\\")
                        slovar[name]=fullname
                        print(fullname)
                        spisok.append(name)
                        spisokExeVseh.append({name:fullname})
            dir = dirlist[1]
            for root, dirs, files in os.walk(dir): # пройти по директории рекурсивно
                for name in files:
                    if name[-4:]=='.exe' or name[-4:]=='.msi':
                        fullname = os.path.join(root, name) # получаем полное имя файла
                        fullname = fullname.replace("/", "\\")
                        slovar[name]=fullname
                        spisok.append(name)
                        spisokExeVseh.append({name:fullname})
                    if name[-4:]=='.rar' or name[-4:]=='.zip':
                        fullname = os.path.join(root, name) # получаем полное имя файла
                        fullname = fullname.replace("/", "\\")
                        slovar[name]=fullname
                        print(fullname)
                        spisok.append(name)
                        spisokExeVseh.append({name:fullname})
            dir = dirlist[2]
            for root, dirs, files in os.walk(dir): # пройти по директории рекурсивно
                for name in files:
                    if name[-4:]=='.exe' or name[-4:]=='.msi':
                        fullname = os.path.join(root, name) # получаем полное имя файла
                        fullname = fullname.replace("/", "\\")
                        slovar[name]=fullname
                        spisok.append(name)
                        spisokExeVseh.append({name:fullname})
                    if name[-4:]=='.rar' or name[-4:]=='.zip':
                        fullname = os.path.join(root, name) # получаем полное имя файла
                        fullname = fullname.replace("/", "\\")
                        slovar[name]=fullname
                        print(fullname)
                        spisok.append(name)
                        spisokExeVseh.append({name:fullname})
        BaseLproRuch = sqlite3.connect(r"data\Lpro.db", uri=True)
        BaseLproRuch.row_factory = sqlite3.Row #подключаем базу данных и курсор
        CurBLproRuch = BaseLproRuch.cursor()
        data = []
        added = False #Для отслеживания добавлен вариант из списка или нет
        n2 = [] #список для исключения дублей
        #opt2 = winRuchPoisk.cbOptions.currentText()
        n3 = []
        for itemsoft in spisok: #В списке имена файлом с расширением exe
             #if winRuchPoisk.cbSpisokExe.isChecked():
             if opt2 == msgruch17:
                 break
             NameP=itemsoft
             NamePF = NameP.replace((NameP[NameP.find('.exe'):]), '')
             s = 'SELECT * FROM program WHERE (file LIKE "' + NamePF + '")'
             CurBLproRuch.execute(s)
             records = CurBLproRuch.fetchall()
             for row in records:
                 if row[1] not in n2: #если нет в списке n2
                     n2.append(row[1]) #тогда добавляем его туда
                 else:
                     continue #иначе переходим к следующей итерации
                 #h = row[4]
                 #h = h.replace("\n", "")

                 if slovar[itemsoft] not in n3: #Удаляю дубли
                    ### Цена и тип
                    if LanguageSystem == 'ru_RU':
                        # Цена
                        if '0' == row[4] or 0 == row[4]:
                            h = 'Бесплатно'
                        else:
                            if '~' in str(row[4]):
                                rep = row[4]
                                rep = rep.replace('~', '')
                                rep = float(rep)
                                ghj = rep * 70
                                jkl = round(ghj, 2)
                                h = 'от ' + str(jkl) + ' руб'
                            else:
                                ghj = row[4] * 70
                                jkl = round(ghj, 2)
                                h = str(jkl) + ' руб'
                        # Тип
                        tip4ikPO = row[2]
                    else:
                        # Цена
                        if '0' == row[4] or 0 == row[4]:
                            h = 'Free'
                        else:
                            if '~' in str(row[4]):
                                rep = str(row[4])
                                rep = rep.replace('~', '')
                                h = 'from $' + rep
                            else:
                                hgf = int(row[4])
                                h = '$' + str(hgf)
                        # Тип
                        tip4ikPO = row[2]
                        if tip4ikPO == 'Свободная программа':
                            tip4ikPO = 'Libre'
                        if tip4ikPO == 'Платное ПО':
                            tip4ikPO = 'Paid'
                        if tip4ikPO == 'Условно-бесплатное ПО':
                            tip4ikPO = 'Free'
                    data.append((slovar[itemsoft], row[1], tip4ikPO, row[3], h))
                    n3.append(slovar[itemsoft])
                 else:
                    continue #иначе переходим к следующей итеоации
                 #data.append((slovar[itemsoft], row[1], row[2], row[3], h))

                 size_list.append(((len(slovar[itemsoft]))*6))
                 #Создаю словари внутри словаря
                 slovarSave[row[1]] = {'Address':slovar[itemsoft], 'Name':row[1], 'TipPO':tip4ikPO, 'License':row[3], 'Cena':h}
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
        # spisokExeVseh.append(slovar[name])
        #if winRuchPoisk.cbSpisokExe.isChecked(): #если поставлена кнопка список exe
        if opt2 == msgruch17:
            for sl1 in spisokExeVseh:
                for keyexefile in sl1:
                    #QMessageBox.about(winRuchPoisk, "1", spisokExeVseh)
                    folder_size = os.path.getsize(sl1[keyexefile])
                    folder_size = folder_size / 1024  # из байт в килобайты
                    folder_size = folder_size / 1024 # из килобайтов в мегабайты
                    folder_size = round(folder_size, 2)  # округляем до двух символов после точки
                    if folder_size < 1: # если меньше мегабайта к следующему циклу
                        continue
                    folder_size = str(folder_size) + msgruch18
                    data.append((sl1[keyexefile], keyexefile, folder_size, msgruch19, msgruch19))
                    slovarSave[keyexefile] = {'Address':sl1[keyexefile], 'Name':keyexefile, 'TipPO':folder_size, 'License':msgruch19, 'Cena':msgruch19}
        CurBLproRuch.close() #Закрываю соединение с базой и с курсором для базы
        BaseLproRuch.close()
        winRuchPoisk.tableWidgetRuch.setRowCount(len(data))
        winRuchPoisk.tableWidgetRuch.setColumnCount(5)
        if LanguageSystem == 'ru_RU':
            winRuchPoisk.tableWidgetRuch.setHorizontalHeaderLabels(
                    ('Название:', "В базе:", 'Тип:', 'Лицензия:', '~Цена:')
                )
        else:
            winRuchPoisk.tableWidgetRuch.setHorizontalHeaderLabels(
                     ('Name:', "In database:", 'Type:', 'License:', '~Price:')
                 )
        row = 0
        for tup in data:
            col = 0
            for item in tup:
                cellinfo = QTableWidgetItem(item)
                cellinfo.setFlags(
                            Qt.ItemIsSelectable | Qt.ItemIsEnabled
                        )
                winRuchPoisk.tableWidgetRuch.setItem(row, col, cellinfo)
                col += 1

            row += 1
        #winRuchPoisk.tableWidgetRuch.resizeColumnsToContents()
        #winRuchPoisk.tableWidgetRuch.setColumnWidth(1, 150)
        #winRuchPoisk.tableWidgetRuch.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        size1 = 400
        for itemsize in size_list:
            if size1 <= int(itemsize):
                size1 = int(itemsize)
        if size1 == None:
            size1 = 400
        if size1 < 400:
            size1 = 400
        if size1 > 650:
            size1 = 650
        winRuchPoisk.tableWidgetRuch.resizeColumnsToContents()
        winRuchPoisk.tableWidgetRuch.setColumnWidth(1, 150)
        winRuchPoisk.tableWidgetRuch.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        winRuchPoisk.resize(size1+491, 289)
        winRuchPoisk.tableWidgetRuch.resize(size1+391, 231)
        x = size1+491
        #y = 289
        #winRuchPoisk.move(x, y)
        winRuchPoisk.setFixedSize(x, 289)
        winRuchPoisk.show()
    winRuchPoisk.pbPoisk.clicked.connect(ButtonRuchPoisk)
    winRuchPoisk.leKatalog.returnPressed.connect(ButtonRuchPoisk)
    def SaveRuch():
        """Сохранить отчет в HTML"""
        if LanguageSystem == 'ru_RU':
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
        else:
            SbHTML="""
                 <html>
                 <head>
                 </head>
             <h1 align=center>LicenseChecker manual search report</h1>"""
            SbHTML = SbHTML + '<h2 align=center>PC: '+socket.gethostname() + ' at ' + datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S") +'</h1>'
            SbHTML = SbHTML + """
             <html>
             <table border=1 align=center>
             <tr><td> Database name
             <td> Path
             <td> Type
             <td> License
             <td> Price
             </tr>
                 """
            
        s=''
        s1=''
        for itemsoft in slovarSave:
            s = slovarSave[itemsoft]
            s1 = '<tr><td> ' + s['Name'] + '\n' + '<td> ' + s['Address'] + '\n' + '<td> ' + s['TipPO'] + '\n'
            s1 = s1 + '<td> ' + s['License'] + '\n' + '<td> ' + str(s['Cena']) + '\n'
            SbHTML = SbHTML + s1
        if LanguageSystem == 'ru_RU':
            s2 = """
                </table>
                <p align=center>Официальный сайт: <a href="https://xn--90abhbolvbbfgb9aje4m.xn--p1ai/">КонтинентСвободы.рф</a></p>
                </html>
                """
            msgruchsave1 = "Укажите куда необходимо сохранить отчет?"
            msgruchsave2 = "Файл сохранен"
            msgruchsave3 = "Файл успешно сохранен: "
            msgruchsave4 = "Не удалось сохранить"
            msgruchsave5 = "Не удалось сохранить файл: "
        else:
            s2="""
                 </table>
                 <p align=center>Official site: <a href="https://openwinsoft.org/">openwinsoft.org</a></p>
                 </html>
                 """
            msgruchsave1 = "Where do you want to save the report?"
            msgruchsave2 = "File Saved"
            msgruchsave3 = "File saved successfully: "
            msgruchsave4 = "Failed to save"
            msgruchsave5 = "Failed to save file: "
        SbHTML = SbHTML + s2
        #ftypes = [('HTML', '.html')] #Указываю тип расширение
        options = QFileDialog.Options()
        fileName = QFileDialog.getSaveFileName(winRuchPoisk, msgruchsave1,".html","HTML (*.html)", options=options)
        try:
            f = open(fileName[0],'w+')
            f.write(SbHTML) #Записываем в файл
            f.close()
            QMessageBox.about(winRuchPoisk, msgruchsave2, msgruchsave3 + fileName[0])
        except:
            QMessageBox.about(winRuchPoisk, msgruchsave4, msgruchsave5 + fileName[0])
    winRuchPoisk.pbSave.clicked.connect(SaveRuch)
    #winRuchPoisk.show()
    winRuchPoisk.show()
win.mRuchPoisk.triggered.connect(RuchPoisk)
def MediaPoisk():
    """Ручной поиск программ"""
    #winMediaPoisk.setFixedSize(819, 273)
    size_list=[]
    #size1 = None
    if LanguageSystem == 'ru_RU':
        msgmed1 = "Указать каталог для медиа-файлов"
        msgmed2 = 'Исключение при сравнении размера файлов'
        msgmed3 = 'Изображение'
        msgmed4 = 'Аудио'
        msgmed5 = 'Видео'
        msgmed6 = ' МБ'
    else:
        msgmed1 = "Specify directory for media files"
        msgmed2 = 'File size comparison exception'
        msgmed3 = 'Image'
        msgmed4 = 'Audio'
        msgmed5 = 'Video'
        msgmed6 = 'MB'
    slovarMediaSave= {}
    katalog = None
    def CheckedRashir():
        if winMediaPoisk.cbActiveRassh.isChecked():
            winMediaPoisk.leRasshirenie.setEnabled(True)
    winMediaPoisk.cbActiveRassh.clicked.connect(CheckedRashir)
    def OpenMedKatalog():
        """Открыть каталог"""
        global katalog
        katalog = None
        try:
            PredKatalog = winMediaPoisk.leKatalog.text()
        except:
            PredKatalog = "."
        winMediaPoisk.leKatalog.setText("")
        #winMediaPoisk.tableWidgetMedia.clear()
        katalog = QFileDialog.getExistingDirectory(winMediaPoisk, msgmed1, PredKatalog)
        winMediaPoisk.leKatalog.setText(katalog)
    winMediaPoisk.pbObzor.clicked.connect(OpenMedKatalog)
    def ButtonMediaPoisk():
        """Функция для кнопки поиск"""
        global katalog
        try:
            if katalog == None:
                return
        except IndexError:
            if (winMediaPoisk.leKatalog.text() == None or winMediaPoisk.leKatalog.text() == ''):
                return
            else:
                katalog = winMediaPoisk.leKatalog.text()
        except NameError:
            if (winMediaPoisk.leKatalog.text() == None or winMediaPoisk.leKatalog.text() == ''):
                return
            else:
                katalog = winMediaPoisk.leKatalog.text()
        winMediaPoisk.tableWidgetMedia.clear()
        spisok=[]
        slovar={}
        slovarMediaSave.clear()
        data=[]
        if winMediaPoisk.cbActiveRassh.isChecked():
            SpisokFormatov = []
            ResSerchRas = re.findall(r'\w{3}|\w{4}', winMediaPoisk.leRasshirenie.text())
            for b1 in ResSerchRas:
                SpisokFormatov.append('.' + b1)
        else:
            SpisokFormatov = ['.tiff', '.jpeg', '.bmp', '.jpe', '.jpg', '.png', '.gif', '.psd', '.mpeg', '.flv', '.mov', '.m4a', '.ac3', '.aac',
             '.h264', '.m4v', '.mkv', '.mp4', '.3gp', '.avi', '.ogg', '.vob', '.wma', '.mp3', '.wav', '.mpg', '.wmv']
        for root, dirs, files in os.walk(katalog):
             # пройти по директории рекурсивно
             #SpisokFormatov = ['.tiff', '.jpeg', '.bmp', '.jpe', '.jpg', '.png', '.gif', '.psd', '.mpeg', '.flv', '.mov', '.m4a', '.ac3', '.aac',
             #'.h264', '.m4v', '.mkv', '.mp4', '.3gp', '.avi', '.ogg', '.vob', '.wma', '.mp3', '.wav', '.mpg', '.wmv']
             for name in files:
                 for format in SpisokFormatov:
                     if name[-4:]==format:
                         fullname = os.path.join(root, name) # получаем полное имя файла
                         fullname = fullname.replace("/", "\\")
                         slovar[name]=fullname
                         try: #Проверяем минимальный размер
                             r = int(winMediaPoisk.leMinSize.text())
                             f = ((os.path.getsize(fullname))/1024)/1024
                             if f < r:
                                 continue
                         except:
                             print(msgmed2, fullname)
                         spisok.append(name)
                         size_list.append(((len(fullname))*6))
        #i = 1
        for itemsoft in spisok:
            #NameP=itemsoft
            ext = os.path.splitext(slovar[itemsoft])[1]
            TipFile = '?'
            SpImages = ['.tiff', '.jpeg', '.bmp', '.jpe', '.jpg', '.png', '.gif', '.psd']
            SpAudio = ['.m4a', '.ac3', '.aac', '.ogg', '.wma', '.mp3', '.wav']
            SpVideo = ['.mpeg', '.flv', '.mov', '.h264', '.m4v', '.mkv', '.mp4', '.3gp', '.avi', '.vob', '.mov', '.mpg', '.wmv']
            for format in SpImages:
                if ext==format:
                    TipFile = msgmed3
            for format in SpAudio:
                if ext==format:
                    TipFile = msgmed4
            for format in SpVideo:
                if ext==format:
                    TipFile = msgmed5
            razmerFile = os.path.getsize(slovar[itemsoft])
            razmerFile = round(((razmerFile/1024)/1024), 2)
            razmerFileStr = str(razmerFile) + msgmed6
            data.append((slovar[itemsoft], TipFile, razmerFileStr))
            slovarMediaSave[slovar[itemsoft]] = {'File':slovar[itemsoft], 'Tip':TipFile, 'Size':razmerFileStr}
        winMediaPoisk.tableWidgetMedia.setRowCount(len(data))
        winMediaPoisk.tableWidgetMedia.setColumnCount(3)
        if LanguageSystem == 'ru_RU':
            winMediaPoisk.tableWidgetMedia.setHorizontalHeaderLabels(
                        ("Имя файла:", "Тип:", "Размер:")
                    )
        else:
            winMediaPoisk.tableWidgetMedia.setHorizontalHeaderLabels(
                     ("Filename:", "Type:", "Size:")
                 )
        row = 0
        for tup in data:
            col = 0
            for item in tup:
                cellinfo = QTableWidgetItem(item)
                cellinfo.setFlags(
                                Qt.ItemIsSelectable | Qt.ItemIsEnabled
                            )
                winMediaPoisk.tableWidgetMedia.setItem(row, col, cellinfo)
                col += 1

            row += 1
        #winMediaPoisk.tableWidgetMedia.resizeColumnsToContents()
        #winMediaPoisk.tableWidgetMedia.setColumnWidth(1, 150)
        #winMediaPoisk.tableWidgetMedia.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        size1 = 400
        for itemsize in size_list:
            if size1 <= int(itemsize):
                size1 = int(itemsize)
        if size1 == None:
            size1 = 400
        if size1 < 400:
            size1 = 400
        if size1 > 650:
            size1 = 650
        winMediaPoisk.tableWidgetMedia.resizeColumnsToContents()
        winMediaPoisk.tableWidgetMedia.setColumnWidth(1, 150)
        winMediaPoisk.tableWidgetMedia.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        winMediaPoisk.resize(size1+419, 273)
        winMediaPoisk.tableWidgetMedia.resize(size1+341, 221)
        x = size1+419
        #y = 273
        #winMediaPoisk.move(x, y)
        winMediaPoisk.setFixedSize(x, 273)
        winMediaPoisk.show()
    winMediaPoisk.pbPoisk.clicked.connect(ButtonMediaPoisk)
    winMediaPoisk.leKatalog.returnPressed.connect(ButtonMediaPoisk)
    def SaveMedia():
        """Сохранить отчет в HTML"""
        if LanguageSystem == 'ru_RU':
            SbHTML = """
                <html>
                <head>
                </head>
            <h1 align=center>Отчет медиа поиска LicenseChecker</h1>"""
            SbHTML = SbHTML + '<h2 align=center>ПК: '+socket.gethostname() + ' в ' + datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S") +'</h1>'
            SbHTML = SbHTML + """
            <html>
            <table border=1 align=center>
            <tr><td> Имя файла
            <td> Тип
            <td> Размер
            </tr>
                """
            s2 = """
            </table>
            <p align=center>Официальный сайт: <a href="https://xn--90abhbolvbbfgb9aje4m.xn--p1ai/">КонтинентСвободы.рф</a></p>
            </html>
            """
            msgmed7 = "Укажите куда необходимо сохранить отчет?"
            msgmed8 = "Файл сохранен"
            msgmed9 = "Файл успешно сохранен: "
            msgmed10 = "Не удалось сохранить"
            msgmed11 = "Не удалось сохранить файл: "
        else:
            SbHTML="""
                 <html>
                 <head>
                 </head>
             <h1 align=center>LicenceChecker media search report</h1>"""
            SbHTML = SbHTML + '<h2 align=center>PC: '+socket.gethostname() + ' at ' + datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S") +'</h1>'
            SbHTML = SbHTML + """
             <html>
             <table border=1 align=center>
             <tr><td> File name
             <td> Type
             <td> Size
             </tr>
                 """
            s2="""
             </table>
             <p align=center>Official site: <a href="https://openwinsoft.org/">openwinsoft.org</a></p>
             </html>
             """
            msgmed7 = "Where do you want to save the report?"
            msgmed8 = "File Saved"
            msgmed9 = "File saved successfully: "
            msgmed10 = "Failed to save"
            msgmed11 = "Failed to save file: "
        s=''
        s1=''
        for itemsoft in slovarMediaSave:
            s = slovarMediaSave[itemsoft]
            s1 = '<tr><td> ' + s['File'] + '\n' + '<td> ' + s['Tip'] + '\n' + '<td> ' + s['Size'] + '\n'
            SbHTML = SbHTML + s1
        SbHTML = SbHTML + s2
        #ftypes = [('HTML', '.html')] #Указываю тип расширение
        options = QFileDialog.Options()
        fileMediaName = QFileDialog.getSaveFileName(winMediaPoisk, msgmed7,".html","HTML (*.html)", options=options)
        try:
            g = open(fileMediaName[0],'w+', encoding='utf-8')
            g.write(SbHTML) #Записываем в файл
            g.close()
            QMessageBox.about(winMediaPoisk, msgmed8, msgmed9 + fileMediaName[0])
        except:
            QMessageBox.about(winMediaPoisk, msgmed10, msgmed11 + fileMediaName[0])
    winMediaPoisk.pbSave.clicked.connect(SaveMedia)
    winMediaPoisk.show()
win.mMediaPoisk.triggered.connect(MediaPoisk)

#Пример ярлыка для запуска с параметрами:
#D:\LicenseChecker\1.3\exe\LicenseChecker\LicenseChecker.exe AutoHidden "D:\\Public\\2.html"
#D:\LicenseChecker\1.3\exe\LicenseChecker\LicenseChecker.exe AutoHidden "default"
#D:\LicenseChecker\1.3\exe\LicenseChecker\LicenseChecker.exe RuchHidden "C:\\Program Files" "D:\\Public\\3.html"
#D:\LicenseChecker\1.3\exe\LicenseChecker\LicenseChecker.exe RuchHidden "C:\\Program Files" "default"
# Безопасный запуск без автоматического старта автопоиска
# D:\LicenseChecker\1.3\exe\LicenseChecker\LicenseChecker.exe SafeMode
try:
    if sys.argv[1] == 'AutoHidden':
        parametr.AutoHidden()
    elif sys.argv[1] == 'RuchHidden':
        parametr.RuchHidden()
    elif sys.argv[1] == 'SafeMode':
        win.show()
        sys.exit(app.exec())
    else:
        Avtopoisk()
        win.show()
        sys.exit(app.exec())
except:
    Avtopoisk()
    win.show()
    sys.exit(app.exec())
