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

app = QtWidgets.QApplication([])
win = uic.loadUi("main.ui") #графика главного окна
win.setFixedSize(801, 276)
winMore = uic.loadUi("DoubleClick.ui") #графика главного окна


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
        IntallPath[itemsoft['name']] = itemsoft['InstallLocation']
        s = 'SELECT * FROM program WHERE (name LIKE "' + NameP + '%%")'
        CurBLpro.execute(s)
        records = CurBLpro.fetchall()
        added = False
        for row in records:
            #tree.insert("" , i-1, text=i, values=(NameP, row[2], row[3], row[4]))
            data.append((NameP, row[2], row[3], row[4]))
            slovarSave[NameP] = {'Name':NameP, 'TipPO':row[2], 'License':row[3], 'Cena':row[4]}
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
            data.append(('Путь:', IntallPath[s]))
        except KeyError: #если в реестре он не указан
            data.append(('Стоимость:', 'Неизвестно'))
        try:#Ищим основной исполняемый для подтверждения
            dir = IntallPath[s] + '\\' #IndexError:
            for root1, dirs, files in os.walk(dir):
                # пройти по директории рекурсивно
                for name in files:
                    if name==spisokExe[0]:
                        fullname = os.path.join(root1, name) # получаем полное имя файла
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
        winMore.move(x, y)
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
            QMessageBox.about(self, "Не удалось сохранить", "Не удалось сохранить файл: " + fileName[0])
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
    win.tableWidget.setColumnWidth(1, 150)
    win.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

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


Avtopoisk()
win.show()
sys.exit(app.exec())
