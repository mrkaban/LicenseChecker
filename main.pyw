from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QTableWidgetItem
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
from SearchKey import * #Поиск слов купить и т.п. в папке с программой
from poisklicsogl import *
import urllib.request #для проверки наличия новых версий
from PyQt5.QtWidgets import QStyledItemDelegate #Для окрашивания строк
from PyQt5.QtGui import QColor, QPalette #Для окрашивания строк
import configparser #для создания настроек
import parametr



app = QtWidgets.QApplication([])
win = uic.loadUi("data\\main.ui") #графика главного окна
win.setFixedSize(801, 276)
winMore = uic.loadUi("data\\DoubleClick.ui") #графика подробности по двойному клику в автопоиске
winPoiskZamen = uic.loadUi("data\\PoisZamen.ui") #графика поиск замен
winSpravka = uic.loadUi("data\\Spravka.ui") #графика справка
winViewBD = uic.loadUi("data\\ViewBD.ui") #графика поиск в базе
winAbout = uic.loadUi("data\\About.ui") #графика О программе
winRuchPoisk = uic.loadUi("data\\RuchPoisk.ui") #графика Ручной поиск
winMediaPoisk = uic.loadUi("data\\Media.ui") #графика медиа поиск
winSettings = uic.loadUi("data\\settings.ui") #графика медиа поиск

config = configparser.ConfigParser()
path = "data\\settings.ini"
config.read(path)
try:
    synhTest = config.get("Settings", "synh")
except:
    QMessageBox.critical(win, "Отсутствует файл настроек", "Не удалось получить доступ к файлу settings.ini \
в папке с программой. Настройки будут перезаписаны на значения по умолчанию.")
    config.add_section("Settings")
    config.set("Settings", "synh", "off")
    config.set("Settings", "color_Avto_Text", "on")
    with open(path, "w") as config_file:
        config.write(config_file)
#synh = config.get("Settings", "synh")
#color_Avto_Text = config.get("Settings", "color_Avto_Text")

def Avtopoisk(self=None):
    """Автоматический поиск при запуске программы"""
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
        for row in records:
            if row[6] == None:
                break
            g = row[6] + '.exe'
            spisokExe.append(g)
        TitleWinMore = s + " - Подробности"
        winMore.setWindowTitle(TitleWinMore)
        data=[]
        data.append(('Название:', s))
        data.append(('Тип ПО:', win.tableWidget.item(item.row(), 1).text()))
        data.append(('Лицензия:', win.tableWidget.item(item.row(), 2).text()))
        data.append(('Стоимость:', win.tableWidget.item(item.row(), 3).text()))
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
                data.append(('Путь:', s3))
            #data.append(('Путь:', IntallPath[s]))
            if s3 == 'undefined':
                data.append(('Путь:', 'Неизвестно'))
        except KeyError: #если в реестре он не указан
            data.append(('Путь:', 'Неизвестно'))
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
                            data.append(('Подтверждение:', fullname))
        except KeyError:
            data.append(('Подтверждение:', 'Не найдено'))
        except IndexError:
            data.append(('Подтверждение:', 'Не найдено'))
        try:#поиск слов купить, как доп вариант опознавания платных программ
            if (len(IntallPath[s]))>2:
                h=StartSeachKey(IntallPath[s])
                h1 = h[0]
                data.append(('Поиск слов "Купить":', h1['path']))
            else:
                data.append(('Поиск слов "Купить":', 'Не найдены'))
        except:
            data.append(('Поиск слов "Купить":', 'Не найдены'))
        #Поиск ключа Windows и следов активации
        search_exemple = re.search( r'Windows', s, re.M|re.I)
        if search_exemple:
            data.append(('Ключ Windows:', get_windows_product_key_from_reg()))
            i1 = 1
            i2 = 0
            sled_spisok = sled_activation()
            for sled in sled_spisok:
                if i1 <= i2:
                    data.append(('-', sled))
                    i1 += 1
                    i2 += 1
                else:
                    data.append(('Следы активации:', sled))
                    i1 += 1
                    i2 = i1
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
                        data.append(('Лицензионное соглашение:', lic_sogl))
                        i1 += 1
                        i2 = i1
            else:
                data.append(('Лицензионное соглашение:', 'Не найдено'))
        except KeyError:
            data.append(('Лицензионное соглашение:', 'Корневой каталог приложения не указан'))

        winMore.tableWidget.setRowCount(len(data))
        winMore.tableWidget.setColumnCount(2)
        winMore.tableWidget.setHorizontalHeaderLabels(
                ('Пункт:', 'Параметр:'))
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
        winMore.resize(size1+200, 281)
        winMore.tableWidget.resize(size1+200, 281)
        x = size1+200
        y = 281
        #winMore.move(x, y)
        winMore.setFixedSize(x, 281)
        CurDC.close()
        BaseDC.close()
        winMore.show()

    def SaveAvto():
        """Сохранить отчет автопоиска в HTML"""
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
        options = QFileDialog.Options()
        fileName = QFileDialog.getSaveFileName(self,"Укажите куда необходимо сохранить отчет?",".html","HTML файлы (*.html)", options=options)
        try:
            f = open(fileName[0],'w+')
            f.write(SbHTML) #Записываем в файл
            f.close()
            QMessageBox.about(self, "Файл сохранен", "Файл успешно сохранен: " + fileName[0])
        except:
            QMessageBox.critical(win, "Не удалось сохранить файл:", "Не удалось сохранить файл отчета.")
            #QMessageBox.about(self, "Не удалось сохранить", "Не удалось сохранить файл: " + fileName[0])
    #Добавляем действия к пунктам меню
    win.mSaveAvto.triggered.connect(SaveAvto)
    win.tableWidget.doubleClicked.connect(DoubleClic)

    win.tableWidget.setRowCount(len(data))
    win.tableWidget.setColumnCount(4)
    win.tableWidget.setHorizontalHeaderLabels(
            ('Название:', 'Тип:', 'Лицензия:', '~Цена:')
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
    class ColorDelegate(QStyledItemDelegate):
        def paint(self, painter, option, index):
            if index.data() == 'Свободная программа':
                for j in range(win.tableWidget.columnCount()):
                    win.tableWidget.item(index.row(), j).setForeground(QColor("green"))
            elif index.data() == 'Платное ПО':
                for j in range(win.tableWidget.columnCount()):
                    win.tableWidget.item(index.row(), j).setForeground(QColor("red"))
            elif index.data() == 'Условно-бесплатное ПО':
                for j in range(win.tableWidget.columnCount()):
                    win.tableWidget.item(index.row(), j).setForeground(QColor(192, 162, 17))
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
    webbrowser.open_new_tab("https://xn--90abhbolvbbfgb9aje4m.xn--p1ai/%D1%83%D1%82%D0%B8%D0%BB%D0%B8%D1%82%D1%8B/%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B0/licensechecker-%D0%BB%D0%B5%D0%B3%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%D1%81%D1%82%D1%8C-%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC.html")
win.mWebStr.triggered.connect(WebStr)
def WebHelp():
    """открытие веб-страницы в браузере по умолчанию"""
    webbrowser.open_new_tab("https://github.com/mrkaban/LicenseChecker/issues")
win.mWebHelp.triggered.connect(WebHelp)

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
        url_kluch = 'https://xn--90abhbolvbbfgb9aje4m.xn--p1ai/component/search/?searchword='+textp
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
        QMessageBox.critical(win, "Нет соединения с сервером", "Не удалось проверить наличие обновлений.")
        return
    search_exemple = re.search(r'1.3', h, re.M|re.I) # ТУТ НАДО ИСПРАВИТЬ ВЕРСИЮ ПРОГРАММЫ!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if not search_exemple:
        try:
            QMessageBox.about(win, "Обнаружена новая версия", "Сейчас будет открыта веб-страница с доступными релизами.\
Скачайте подходящую для Вас версию. Если не получается найти файлы, нажмите на \'Assets\'.")
            webbrowser.open_new_tab("https://github.com/mrkaban/LicenseChecker/releases")
        except:
            QMessageBox.critical(win, "Не получилось открыть страницу", "Не получилось открыть ссылку в веб-браузере.")
            return
    else:
        QMessageBox.about(win, "Программа актуальна", "Используемая Вами версия программы актуальна.")
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
        f = urllib.request.urlopen("https://xn--90abhbolvbbfgb9aje4m.xn--p1ai/images/lpro-base-version.txt")
        h = str(f.read())
        h = h.replace("'", "")
        h = h.replace("b", "")
    except:
        QMessageBox.critical(win, "Нет соединения с сервером", "Не удалось проверить наличие обновлений базы данных.")
        return
    for row in records:
        g = str(row[0])
        g = g.replace(" ", "")
        if g != h:
            try:
                bd1 = urllib.request.urlopen("https://xn--90abhbolvbbfgb9aje4m.xn--p1ai/images/Lpro.db").read()
                f = open("data\\Lpro.db", "wb")
                f.write(bd1)
                f.close()
                QMessageBox.about(win, "База обновлена", "База данных успешно обновлена до версии ")
            except:
                QMessageBox.critical(win, "Не удалось загрузить БД", "Не удалось загрузить базу данных.")
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
                    QMessageBox.critical(win, "Не удалось синхронизировать БД", "Не удалось синхронизировать пользовательскую\
базу данных с основной. Проверьте наличие файла data\\User-DB.db в папке с программой.")
                    sinh = False
                if sinh == True:
                    QMessageBox.about(win, "Синхронизация успешно завершена", "Пользовательская база данных успешно\
синхронизиррована с основной базой.")
        else:
            QMessageBox.about(win, "База данных актуальна", "Обновление базы данных не требуется.")
    CurUpdateBase.close() #Закрываю соединение с базой и с курсором для базы
    BaseUpdateBase.close()
win.mUpdateBase.triggered.connect(UpdateBase)

def ViewBD():
    """Поиск и просмотр базы данных"""
    #if textbd == None or textbd == '': если поле пусто, завершить функцию
    #    return True
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
        size2 = None
        added = False
        i = 1
        for row in records:
            size2= 0
            h = row[4]
            h = h.replace("\n", "")
            dataBD.append((row[1], row[2], row[3], h))
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
        winViewBD.tableWidgetBD.setHorizontalHeaderLabels(
                ('Название:', 'Тип:', 'Лицензия:', '~Цена:')
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
    try:
        if 300<=((len(h1['path']))*6):
            size1 = (len(h1['path']))*6 #пробую задать ширину окна по содержимому
        else:
            size1 = 300
    except:
        try:
            if 300<=((len(h1['path']))*6):
                size1 = (len(IntallPath[s]))*6
            else:
                size1 = 300
        except:
            size1 = 300
    winViewBD.tableWidgetBD.resizeColumnsToContents()
    winViewBD.resize(size1+410, 270)
    winViewBD.tableWidgetBD.resize(size1+321, 201)
    x = size1+410
    y = 270
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
        if winRuchPoisk.rb1kat.isChecked():
            d = QFileDialog.getExistingDirectory(winRuchPoisk,"Указать каталог для поиска остатков программ", PredKatalog)
            dirlist.append(d)
            winRuchPoisk.leKatalog.setText(dirlist[0])
        if winRuchPoisk.rb2kat.isChecked():
            d = QFileDialog.getExistingDirectory(winRuchPoisk,"Указать первый каталог для поиска остатков программ", PredKatalog)
            dirlist.append(d)
            d = QFileDialog.getExistingDirectory(winRuchPoisk,"Указать второй каталог для поиска остатков программ", PredKatalog)
            dirlist.append(d)
            winRuchPoisk.leKatalog.setText(dirlist[0] + ' ' + dirlist[1])
        if winRuchPoisk.rb3kat.isChecked():
            d = QFileDialog.getExistingDirectory(winRuchPoisk,"Указать первый каталог для поиска остатков программ", PredKatalog)
            dirlist.append(d)
            d = QFileDialog.getExistingDirectory(winRuchPoisk,"Указать второй каталог для поиска остатков программ", PredKatalog)
            dirlist.append(d)
            d = QFileDialog.getExistingDirectory(winRuchPoisk,"Указать третий каталог для поиска остатков программ", PredKatalog)
            dirlist.append(d)
            winRuchPoisk.leKatalog.setText(dirlist[0] + ' ' + dirlist[1] + ' ' + dirlist[2])
    winRuchPoisk.pbObzor.clicked.connect(OpenKatalog)
    def ButtonRuchPoisk():
        """Функция для кнопки поиск"""
        winRuchPoisk.tableWidgetRuch.clear()
        spisok=[]
        slovar={}
        try:
            if dirlist[0] == '' or dirlist[0] == None:
                if not(os.path.exists(winRuchPoisk.leKatalog.text())):
                    return
        except IndexError:
            if not(os.path.exists(winRuchPoisk.leKatalog.text())):
                return
        if winRuchPoisk.rb1kat.isChecked():
            try:
                dir = dirlist[0]
            except:
                dir = winRuchPoisk.leKatalog.text()
            for root, dirs, files in os.walk(dir): # пройти по директории рекурсивно
                 for name in files:
                     if name[-4:]=='.exe':
                         fullname = os.path.join(root, name) # получаем полное имя файла
                         fullname = fullname.replace("/", "\\")
                         slovar[name]=fullname
                         spisok.append(name)
        if winRuchPoisk.rb2kat.isChecked():
            try:
                dir = dirlist[0]
            except:
                QMessageBox.critical(winRuchPoisk, "Ошибка", "Вручную можно указать только 1 каталог.")
                return
            for root, dirs, files in os.walk(dir): # пройти по директории рекурсивно
                for name in files:
                    if name[-4:]=='.exe':
                        fullname = os.path.join(root, name) # получаем полное имя файла
                        fullname = fullname.replace("/", "\\")
                        slovar[name]=fullname
                        spisok.append(name)
            dir = dirlist[1]
            for root, dirs, files in os.walk(dir): # пройти по директории рекурсивно
                for name in files:
                    if name[-4:]=='.exe':
                        fullname = os.path.join(root, name) # получаем полное имя файла
                        fullname = fullname.replace("/", "\\")
                        slovar[name]=fullname
                        spisok.append(name)
        if winRuchPoisk.rb3kat.isChecked():
            try:
                dir = dirlist[0]
            except:
                QMessageBox.critical(winRuchPoisk, "Ошибка", "Вручную можно указать только 1 каталог.")
                return
            for root, dirs, files in os.walk(dir): # пройти по директории рекурсивно
                for name in files:
                    if name[-4:]=='.exe':
                        fullname = os.path.join(root, name) # получаем полное имя файла
                        fullname = fullname.replace("/", "\\")
                        slovar[name]=fullname
                        spisok.append(name)
            dir = dirlist[1]
            for root, dirs, files in os.walk(dir): # пройти по директории рекурсивно
                for name in files:
                    if name[-4:]=='.exe':
                        fullname = os.path.join(root, name) # получаем полное имя файла
                        fullname = fullname.replace("/", "\\")
                        slovar[name]=fullname
                        spisok.append(name)
            dir = dirlist[2]
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
        winRuchPoisk.tableWidgetRuch.setRowCount(len(data))
        winRuchPoisk.tableWidgetRuch.setColumnCount(5)
        winRuchPoisk.tableWidgetRuch.setHorizontalHeaderLabels(
                ('Название:', "В базе:", 'Тип:', 'Лицензия:', '~Цена:')
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
        y = 289
        #winRuchPoisk.move(x, y)
        winRuchPoisk.setFixedSize(x, 289)
        winRuchPoisk.show()
    winRuchPoisk.pbPoisk.clicked.connect(ButtonRuchPoisk)
    winRuchPoisk.leKatalog.returnPressed.connect(ButtonRuchPoisk)
    def SaveRuch():
        """Сохранить отчет в HTML"""
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
        options = QFileDialog.Options()
        fileName = QFileDialog.getSaveFileName(winRuchPoisk,"Укажите куда необходимо сохранить отчет?",".html","HTML файлы (*.html)", options=options)
        try:
            f = open(fileName[0],'w+')
            f.write(SbHTML) #Записываем в файл
            f.close()
            QMessageBox.about(winRuchPoisk, "Файл сохранен", "Файл успешно сохранен: " + fileName[0])
        except:
            QMessageBox.about(winRuchPoisk, "Не удалось сохранить", "Не удалось сохранить файл: " + fileName[0])
    winRuchPoisk.pbSave.clicked.connect(SaveRuch)
    #winRuchPoisk.show()
    winRuchPoisk.show()
win.mRuchPoisk.triggered.connect(RuchPoisk)
def MediaPoisk():
    """Ручной поиск программ"""
    #winMediaPoisk.setFixedSize(819, 273)
    size_list=[]
    size1 = None
    slovarMediaSave= {}
    katalog = None
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
        katalog = QFileDialog.getExistingDirectory(winMediaPoisk,"Указать каталог для медиа-файлов", PredKatalog)
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
        data=[]
        for root, dirs, files in os.walk(katalog):
             # пройти по директории рекурсивно
             SpisokFormatov = ['.tiff', '.jpeg', '.bmp', '.jpe', '.jpg', '.png', '.gif', '.psd', '.mpeg', '.flv', '.mov', '.m4a', '.ac3', '.aac',
             '.h264', '.m4v', '.mkv', '.mp4', '.3gp', '.avi', '.ogg', '.vob', '.wma', '.mp3', '.wav', '.mpg', '.wmv']
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
                             print('Исключение при сравнении размера файлов', fullname)
                         spisok.append(name)
                         size_list.append(((len(fullname))*6))
        #i = 1
        for itemsoft in spisok:
            NameP=itemsoft
            ext = os.path.splitext(slovar[itemsoft])[1]
            TipFile = '?'
            SpImages = ['.tiff', '.jpeg', '.bmp', '.jpe', '.jpg', '.png', '.gif', '.psd']
            SpAudio = ['.m4a', '.ac3', '.aac', '.ogg', '.wma', '.mp3', '.wav']
            SpVideo = ['.mpeg', '.flv', '.mov', '.h264', '.m4v', '.mkv', '.mp4', '.3gp', '.avi', '.vob', '.mov', '.mpg', '.wmv']
            for format in SpImages:
                if ext==format:
                    TipFile = 'Изображение'
            for format in SpAudio:
                if ext==format:
                    TipFile = 'Аудио'
            for format in SpVideo:
                if ext==format:
                    TipFile = 'Видео'
            razmerFile = os.path.getsize(slovar[itemsoft])
            razmerFile = round(((razmerFile/1024)/1024), 2)
            razmerFileStr = str(razmerFile) + ' МБ'
            data.append((slovar[itemsoft], TipFile, razmerFileStr))
            slovarMediaSave[slovar[itemsoft]] = {'File':slovar[itemsoft], 'Tip':TipFile, 'Size':razmerFileStr}
        winMediaPoisk.tableWidgetMedia.setRowCount(len(data))
        winMediaPoisk.tableWidgetMedia.setColumnCount(3)
        winMediaPoisk.tableWidgetMedia.setHorizontalHeaderLabels(
                    ("Имя файла:", "Тип:", "Размер:")
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
        y = 273
        #winMediaPoisk.move(x, y)
        winMediaPoisk.setFixedSize(x, 273)
        winMediaPoisk.show()
    winMediaPoisk.pbPoisk.clicked.connect(ButtonMediaPoisk)
    winMediaPoisk.leKatalog.returnPressed.connect(ButtonMediaPoisk)
    def SaveMedia():
        """Сохранить отчет в HTML"""
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
        s=''
        s1=''
        for itemsoft in slovarMediaSave:
            s = slovarMediaSave[itemsoft]
            s1 = '<tr><td> ' + s['File'] + '\n' + '<td> ' + s['Tip'] + '\n' + '<td> ' + s['Size'] + '\n'
            SbHTML = SbHTML + s1
        s2 = """
            </table>
            <p align=center>Официальный сайт: <a href="http://xn--90abhbolvbbfgb9aje4m.xn--p1ai/">КонтинентСвободы.рф</a></p>
            </html>
            """
        SbHTML = SbHTML + s2
        ftypes = [('HTML', '.html')] #Указываю тип расширение
        options = QFileDialog.Options()
        fileMediaName = QFileDialog.getSaveFileName(winMediaPoisk,"Укажите куда необходимо сохранить отчет?",".html","HTML файлы (*.html)", options=options)
        try:
            g = open(fileMediaName[0],'w+', encoding='utf-8')
            g.write(SbHTML) #Записываем в файл
            g.close()
            QMessageBox.about(winMediaPoisk, "Файл сохранен", "Файл успешно сохранен: " + fileMediaName[0])
        except:
            QMessageBox.about(winMediaPoisk, "Не удалось сохранить", "Не удалось сохранить файл: " + fileMediaName[0])
    winMediaPoisk.pbSave.clicked.connect(SaveMedia)
    winMediaPoisk.show()
win.mMediaPoisk.triggered.connect(MediaPoisk)

#Пример ярлыка для запуска с параметрами:
#D:\LicenseChecker\1.3\exe\LicenseChecker\LicenseChecker.exe AutoHidden "D:\\Public\\2.html"
#D:\LicenseChecker\1.3\exe\LicenseChecker\LicenseChecker.exe AutoHidden "default"
#D:\LicenseChecker\1.3\exe\LicenseChecker\LicenseChecker.exe RuchHidden "C:\\Program Files" "D:\\Public\\3.html"
#D:\LicenseChecker\1.3\exe\LicenseChecker\LicenseChecker.exe RuchHidden "C:\\Program Files" "default"
try:
    if sys.argv[1] == 'AutoHidden':
        parametr.AutoHidden()
    elif sys.argv[1] == 'RuchHidden':
        parametr.RuchHidden()
    else:
        Avtopoisk()
        win.show()
        sys.exit(app.exec())
except:
    Avtopoisk()
    win.show()
    sys.exit(app.exec())
