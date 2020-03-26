#Автор Алексей Черемных (КонтинентСвободы.рф)
#Лицензия GNU GPL v2
#Импорт библиотек
import urllib.request
import winreg #Нужна для работы со значением типа реестр
from tkinter import *
import tkinter.ttk as ttk
import sqlite3 #База данных SQLite
from reestr import foo #функция получения данных из реестра
from filtr import filter #Фильтрация автопоиска
import webbrowser #Для открытия веб-страницы
import tkinter.filedialog #Для диалога открытия папки
import os #Для поиска файлов
from tkinter import messagebox #Сообщения
from datetime import datetime #какая дата и время
import socket #Для получения имени компьютера
from SearchKey import * #Поиск слов купить и т.п. в папке с программой
from PIL import ImageTk, Image


#Получаем данные из реестра в список(словари)
software_list = foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY)+ foo(winreg.HKEY_CURRENT_USER, 0)

root = Tk()
root.title("LicenseCheker - Проверка лицензий установленных программ")
root.iconbitmap('LicenseCheker.ico')
katalog=''

#Функция для меню
def close_win():
    """Закрываем окно"""
    #root.destroy()
    sys.exit()
def WebStr(self):
    """открытие веб-страницы в браузере по умолчанию"""
    webbrowser.open_new_tab("https://xn--90abhbolvbbfgb9aje4m.xn--p1ai/")
def UpdateProg():
    """проверка наличия новой версии программы"""
    my_version = 0.1
    try:
        f = urllib.request.urlopen("https://github.com/mrkaban/LicenseCheker/raw/master/version")
        h = str(f.read())
    except:
        messagebox.showerror("Нет соединения с сервером", "Не удалось проверить наличие обновлений.")
        return
    if my_version != h:
        try:
            webbrowser.open_new_tab("https://github.com/mrkaban/LicenseCheker/raw/master/LicenseCheker.zip")
        except:
            messagebox.showerror("Не получилось открыть страницу", "Не получилось открыть ссылку в веб-браузере.")
            return
def UpdateBase():
    """Обновление базы данных Lpro.db"""
    BaseUpdateBase = sqlite3.connect(r"Lpro.db", uri=True)
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
        messagebox.showerror("Нет соединения с сервером", "Не удалось проверить наличие обновлений базы данных.")
        return
    for row in records:
        g = str(row[0])
        g = g.replace(" ", "")
        if g != h:
            try:
                bd1 = urllib.request.urlopen("https://xn--90abhbolvbbfgb9aje4m.xn--p1ai/images/Lpro.db").read()
                f = open("Lpro.db", "wb")
                f.write(bd1)
                f.close()
                txt1 = "База данных успешно обновлена до версии " + h + "!"
                messagebox.showinfo("База обновлена", txt1)
            except:
                messagebox.showerror("Не удалось загрузить БД", "Не удалось загрузить базу данных.")
                break
        else:
            messagebox.showinfo("База данных актуальна", "Обновление базы данных не требуется.")
    CurUpdateBase.close() #Закрываю соединение с базой и с курсором для базы
    BaseUpdateBase.close()
def ViewBD():
    """Поиск и просмотр базы данных"""
    winBD= Toplevel(root)
    winBD.iconbitmap('LicenseCheker.ico')
    winBD.resizable(width=False, height=False)
    winBD.title("Поиск и просмотр базы данных")
    winBD.minsize(width=400, height=200)
    #winBD.geometry("900x300")
    frameBD = Frame(winBD)
    treeBD = ttk.Treeview(winBD)

    treeBD = ttk.Treeview(frameBD, selectmode='browse')

    scrollbar_vertical = ttk.Scrollbar(frameBD, orient='vertical', command = treeBD.yview)

    scrollbar_vertical.pack(side='right', fill=Y)

    treeBD.configure(yscrollcommand=scrollbar_vertical.set)

    treeBD.pack(side=LEFT, fill=BOTH, expand=False)

    frameBD.pack(expand=False)

    #заполняем таблицу
    treeBD["columns"]=("Name","Type", "Lic", "Cena")
    treeBD.column("#0", width=50)
    treeBD.column("Name", width=300, stretch=True)
    treeBD.column("Type", width=150, stretch=True)
    treeBD.column("Lic", width=120, stretch=True)
    treeBD.column("Cena", width=80, stretch=True)
    treeBD.heading("#0", text="№:")
    treeBD.heading("Name", text="Название:")
    treeBD.heading("Type", text="Тип:")
    treeBD.heading("Lic", text="Лицензия:")
    treeBD.heading("Cena", text="~Цена:")

    #Пробую работать с SQLite
    BaseBD = sqlite3.connect(r"Lpro.db", uri=True)
    BaseBD.row_factory = sqlite3.Row
    CurBD = BaseBD.cursor()
    s = 'SELECT * FROM program'
    CurBD.execute(s)
    records = CurBD.fetchall()
    added = False
    i = 1
    for row in records:
        treeBD.insert("" , i-1, text=i, values=(row[1], row[2], row[3], row[4]))
        added = True
        i += 1
    CurBD.close()
    BaseBD.close()
    winBD.resizable(width=False, height=False)
    treeBD.pack()

def about():
    """окно о программе"""
    winAbout= Toplevel(root)
    winAbout.iconbitmap('LicenseCheker.ico')
    winAbout.resizable(width=False, height=False)
    winAbout.title("О программе LicenseCheker")
    winAbout.minsize(width=400, height=100)
    img = Image.open("LicenseCheker.png")
    render = ImageTk.PhotoImage(img)
    initil = Label(winAbout, image=render)
    initil.image = render
    initil.pack(side = "left")
    lab=Label(winAbout, text="LicenseCheker 1.0", justify="left", font='Arial 14 bold')
    lab.pack(side = "top")
    lab4=Label(winAbout, text="\nЦель: Помочь разобраться с лицензиями \nна программное обеспечение", justify="left")
    lab4.pack()
    lab2=Label(winAbout, text="\nЛицензия: GNU GPL v2 \n\nРазработчик: Алексей Черемных (mrKaban) \n ", justify="left")
    lab2.pack()
    lab3=Label(winAbout, text="КонтинентСвободы.рф", justify="left", fg="blue")
    lab3.pack()
    lab3.bind('<Button-1>', WebStr)
def RuchSearchProg():
    """Ручной поиск программ"""
    winRuch= Toplevel(root)
    winRuch.iconbitmap('LicenseCheker.ico')
    winRuch.resizable(width=False, height=False)
    winRuch.title("Ручной поиск программ в указанной директории")
    #winRuch.minsize(width=400, height=200)
    winRuch.geometry("900x300")
    frameRuch2 = Frame(winRuch)
    L2 = Label(frameRuch2, text="Укажите каталог для поиска следов программ и нажмите кнопку 'Поиск'")
    L2.pack(side=TOP)
    L1 = Label(frameRuch2, text="Каталог")
    L1.pack(side = LEFT, expand = True)
    message = StringVar()
    E1 = Entry(frameRuch2, width=50, textvariable=message)
    E1.pack(side = LEFT, expand = True)
    slovarSave= {}
    def OpenKatalog():
        """Открыть каталог"""
        E1.delete(first=0,last=50)
        katalog = tkinter.filedialog.askdirectory(parent=winRuch, title='Укажите директорию для поиска')
        E1.insert(0, katalog)
    def PoiskRuchnoiDlyaKnopki():
        """Функция для кнопки поиск"""
        spisok=[]
        slovar={}
        dir = message.get()
        for root, dirs, files in os.walk(dir):
             # пройти по директории рекурсивно
             for name in files:
                 if name[-4:]=='.exe':
                     fullname = os.path.join(root, name) # получаем полное имя файла
                     slovar[name]=fullname
                     spisok.append(name)
        BaseLproRuch = sqlite3.connect(r"Lpro.db", uri=True)
        BaseLproRuch.row_factory = sqlite3.Row #подключаем базу данных и курсор
        CurBLproRuch = BaseLproRuch.cursor()

        added = False #Для отслеживания добавлен вариант из списка или нет
        i = 1
        for itemsoft in spisok: #В списке имена файлом с расширением exe
             NameP=itemsoft
             NamePF = NameP.replace((NameP[NameP.find('.exe'):]), '')
             s = 'SELECT * FROM program WHERE (file LIKE "' + NamePF + '")'
             CurBLproRuch.execute(s)
             records = CurBLproRuch.fetchall()
             for row in records:
                 treeRuch.insert("" , i-1, text=i, values=(slovar[itemsoft], row[1], row[2], row[3], row[4]))
                 #Создаю словари внутри словаря
                 slovarSave[row[1]] = {'Address':slovar[itemsoft], 'Name':row[1], 'TipPO':row[2], 'License':row[3], 'Cena':row[4]}
                 added = True
                 break
             i += 1
             if added == False:
                 i = i -1
        CurBLproRuch.close() #Закрываю соединение с базой и с курсором для базы
        BaseLproRuch.close()

#str(datetime.now())
    def SaveRuch():
        """Сохранить отчет в HTML"""
        SbHTML = """
            <html>
            <head>
            </head>
        <h1 align=center>Отчет ручного поиска LicenseCheker</h1>"""
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
        file_name = tkinter.filedialog.asksaveasfilename(filetypes=ftypes, defaultextension='.html')
        try:
            f = open(file_name,'w+')
            f.write(SbHTML) #Записываем в файл
            f.close()
            messagebox.showinfo("Файл сохранен", "Файл успешно сохранен: " + file_name)
        except:
            messagebox.showinfo("Не удалось сохранить", "Не удалось сохранить файл: " + file_name)

    btnObzor = Button(frameRuch2, text="Обзор", command=OpenKatalog)
    btnObzor.pack(side = LEFT, expand = True)
    btnPoisk = Button(frameRuch2, text="Поиск", command=PoiskRuchnoiDlyaKnopki)
    btnPoisk.pack(side = LEFT, expand = True)
    btnSave = Button(frameRuch2, text="Сохранить", command=SaveRuch)
    btnSave.pack(side = LEFT, expand = True)
    frameRuch2.pack(side = TOP, expand=False)
    #Рисую таблицу для ручного поиска
    treeRuch = ttk.Treeview(winRuch)
    frameRuch = Frame(winRuch)

    treeRuch = ttk.Treeview(frameRuch, selectmode='browse')

    scrollbar_vertical = ttk.Scrollbar(frameRuch, orient='vertical', command = treeRuch.yview)

    scrollbar_vertical.pack(side='right', fill=Y)

    treeRuch.configure(yscrollcommand=scrollbar_vertical.set)

    treeRuch.pack(side = BOTTOM, expand=False)
    frameRuch.pack(side = BOTTOM, expand=False)

    #заполняем таблицу
    treeRuch["columns"]=("Name", "NameDB", "Type", "Lic", "Cena")
    treeRuch.column("#0", width=50)
    treeRuch.column("Name", width=350, stretch=True)
    treeRuch.column("NameDB", width=120, stretch=True)
    treeRuch.column("Type", width=150, stretch=True)
    treeRuch.column("Lic", width=120, stretch=True)
    treeRuch.column("Cena", width=80, stretch=True)
    treeRuch.heading("#0", text="№:")
    treeRuch.heading("Name", text="Название:")
    treeRuch.heading("NameDB", text="В базе:")
    treeRuch.heading("Type", text="Тип:")
    treeRuch.heading("Lic", text="Лицензия:")
    treeRuch.heading("Cena", text="~Цена:")
    treeRuch.pack(side = BOTTOM)


#Сохранить отчет автопоиска
slovarSave = {}
def SaveAuto():
    """Сохранить отчет в HTML"""
    SbHTML = """
        <html>
        <head>
        </head>
    <h1 align=center>Отчет автопоиска LicenseCheker</h1>"""
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
    s='' #slovarSave[NameP] = {'Name':NameP, 'TipPO':row[2], 'License':row[3], 'Cena':row[4]}
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
    file_name = tkinter.filedialog.asksaveasfilename(filetypes=ftypes, defaultextension='.html')
    try:
        f = open(file_name,'w+')
        f.write(SbHTML) #Записываем в файл
        f.close()
        messagebox.showinfo("Файл сохранен", "Файл успешно сохранен: " + file_name)
    except:
        messagebox.showinfo("Не удалось сохранить", "Не удалось сохранить файл: " + file_name)
### Начало медиа поиска
def MediaSearch():
    """Ручной поиск программ"""
    winMedia= Toplevel(root)
    winMedia.iconbitmap('LicenseCheker.ico')
    winMedia.resizable(width=False, height=False)
    winMedia.title("Поиск медиа файлов (аудио, видео, изображения) в указанной директории")
    #winMedia.minsize(width=400, height=200)
    #winMedia.geometry("900x300")
    frameMed2 = Frame(winMedia)
    L2 = Label(frameMed2, text="Укажите каталог для поиска медиа файлов и нажмите кнопку 'Поиск'")
    L2.pack(side=TOP)
    L3 = Label(frameMed2, text="Мин. размер МБ:")
    L3.pack(side = LEFT, expand = True)
    message3 = StringVar()
    E3 = Entry(frameMed2, width=5, textvariable=message3)
    E3.pack(side = LEFT, expand = True)
    E3.delete(0, END)
    E3.insert(0, "0")
    L1 = Label(frameMed2, text="Каталог")
    L1.pack(side = LEFT, expand = True)
    message = StringVar()
    E1 = Entry(frameMed2, width=50, textvariable=message)
    E1.pack(side = LEFT, expand = True)
    size1 = None
    size2 = None
    slovarMediaSave= {}
    def OpenMedKatalog():
        """Открыть каталог"""
        E1.delete(first=0,last=50)
        katalog = tkinter.filedialog.askdirectory(parent=winMedia, title='Укажите директорию для поиска')
        E1.insert(0, katalog)
    def PoiskMediaDlyaKnopki():
        """Функция для кнопки поиск"""
        spisok=[]
        slovar={}
        dir = message.get()
        for root, dirs, files in os.walk(dir):
             # пройти по директории рекурсивно
             SpisokFormatov = ['.tiff', '.jpeg', '.bmp', '.jpe', '.jpg', '.png', '.gif', '.psd', '.mpeg', '.flv', '.mov', '.m4a', '.ac3', '.aac',
             '.h264', '.m4v', '.mkv', '.mp4', '.3gp', '.avi', '.ogg', '.vob', '.wma', '.mp3', '.wav', '.mpg', '.wmv']
             for name in files:
                 for format in SpisokFormatov:
                     if name[-4:]==format:
                         fullname = os.path.join(root, name) # получаем полное имя файла
                         slovar[name]=fullname
                         try: #Проверяем минимальный размер
                             r = int(message3.get())
                             f = ((os.path.getsize(fullname))/1024)/1024
                             if f < r:
                                 continue
                         except:
                             print('Исключение при сравнении размера файлов')
                         spisok.append(name)
        i = 1
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
            size1 = (len(slovar[itemsoft]))*6
            razmerFile = os.path.getsize(slovar[itemsoft])
            razmerFile = round(((razmerFile/1024)/1024), 2)
            razmerFileStr = str(razmerFile) + ' МБ'
            size2 = (len(razmerFileStr))*7
            treeMed.insert("" , i-1, text=i, values=(slovar[itemsoft], TipFile, razmerFileStr))
            slovarMediaSave[slovar[itemsoft]] = {'File':slovar[itemsoft], 'Tip':TipFile, 'Size':razmerFileStr}
            i += 1
    def SaveMedia():
        """Сохранить отчет в HTML"""
        SbHTML = """
            <html>
            <head>
            </head>
        <h1 align=center>Отчет медиа поиска LicenseCheker</h1>"""
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
        file_name = tkinter.filedialog.asksaveasfilename(filetypes=ftypes, defaultextension='.html')
        try:
            f = open(file_name,'w+', encoding='utf-8')
            f.write(SbHTML) #Записываем в файл
            f.close()
            messagebox.showinfo("Файл сохранен", "Файл успешно сохранен: " + file_name)
        except:
            messagebox.showinfo("Не удалось сохранить", "Не удалось сохранить файл: " + file_name)

    btnObzor = Button(frameMed2, text="Обзор", command=OpenMedKatalog)
    btnObzor.pack(side = LEFT, expand = True)
    btnPoisk = Button(frameMed2, text="Поиск", command=PoiskMediaDlyaKnopki)
    btnPoisk.pack(side = LEFT, expand = True)
    btnSave = Button(frameMed2, text="Сохранить", command=SaveMedia)
    btnSave.pack(side = LEFT, expand = True)
    frameMed2.pack(side = TOP, expand=False)
    #Рисую таблицу для ручного поиска
    treeMed = ttk.Treeview(winMedia)
    frameMed = Frame(winMedia)

    treeMed = ttk.Treeview(frameMed, selectmode='browse')

    scrollbar_vertical = ttk.Scrollbar(frameMed, orient='vertical', command = treeMed.yview)

    scrollbar_vertical.pack(side='right', fill=Y)

    treeMed.configure(yscrollcommand=scrollbar_vertical.set)

    treeMed.pack(side = BOTTOM, expand=False)
    frameMed.pack(side = BOTTOM, expand=False)

    #заполняем таблицу
    treeMed["columns"]=("Name", "Type", "Size")
    treeMed.column("#0", width=50)
    treeMed.column("Name", width=350, stretch=True)
    treeMed.column("Type", width=150, stretch=True, anchor=CENTER)
    treeMed.column("Size", width=120, stretch=True, anchor=CENTER)
    treeMed.heading("#0", text="№:")
    treeMed.heading("Name", text="Имя файла:")
    treeMed.heading("Type", text="Тип:")
    treeMed.heading("Size", text="Размер:")
    if size1 == None:
        size1 = 380
    if size2 == None:
        size2 = 120
    winMedia.minsize(width=(size1+ size2 + 180), height=200)
    treeMed.column("Name", width=size1, stretch=True)
    treeMed.column("Size", width=size2, stretch=True, anchor=CENTER)
    treeMed.pack(side = LEFT, expand=True)
### конец медиа поиска

#Создание меню основного окна
m=Menu(root)
root.config(menu=m)
fm=Menu(m)
m.add_cascade(label="Файл", menu=fm)
fm.add_command(label="Сохранить", command=SaveAuto)
fm.add_command(label="Выход", command=close_win)
pm=Menu(m)
m.add_cascade(label="Поиск", menu=pm)
pm.add_command(label="Ручной поиск программ", command=RuchSearchProg)
pm.add_command(label="Медиа поиск", command=MediaSearch)
pm.add_command(label="Поиск в базе", command=ViewBD)
hm=Menu(m)
m.add_cascade(label="?", menu=hm)
hm.add_command(label="О программе", command=about)
hm.add_command(label="Официальный сайт", command=WebStr)
hm.add_command(label="Обновить базу данных", command=UpdateBase)
hm.add_command(label="Проверить наличие новой версии", command=UpdateProg)

#Рисуем таблицу основного окна
tree = ttk.Treeview(root)

frame = Frame(root)

tree = ttk.Treeview(frame, selectmode='browse')

scrollbar_vertical = ttk.Scrollbar(frame, orient='vertical', command = tree.yview)

scrollbar_vertical.pack(side='right', fill=Y)

tree.configure(yscrollcommand=scrollbar_vertical.set)

tree.pack(side=LEFT, fill=BOTH, expand=False)

frame.pack(expand=False)

#заполняем таблицу
tree["columns"]=("Name","Type", "Lic", "Cena")
tree.column("#0", width=50)
tree.column("Name", width=300, stretch=True)
tree.column("Type", width=150, stretch=True)
tree.column("Lic", width=120, stretch=True)
tree.column("Cena", width=80, stretch=True)
tree.heading("#0", text="№:")
tree.heading("Name", text="Название:")
tree.heading("Type", text="Тип:")
tree.heading("Lic", text="Лицензия:")
tree.heading("Cena", text="~Цена:")

#Пробую работать с SQLite
BaseLpro = sqlite3.connect(r"Lpro.db", uri=True)
BaseLpro.row_factory = sqlite3.Row
CurBLpro = BaseLpro.cursor()
IntallPath = {}
i = 1
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
        tree.insert("" , i-1, text=i, values=(NameP, row[2], row[3], row[4]))
        slovarSave[NameP] = {'Name':NameP, 'TipPO':row[2], 'License':row[3], 'Cena':row[4]}
        added = True
        break
    if added == False:
        tree.insert("" , i-1, text=i, values=(itemsoft['name'], "Неизвестно", "Неизвестно", "???"))
        slovarSave[NameP] = {'Name':NameP, 'TipPO':"Неизвестно", 'License':"Неизвестно", 'Cena':"???"}
    i += 1
def DoubleClic(event): #Функция для события двойного клика
    winMore= Toplevel(root)
    winMore.iconbitmap('LicenseCheker.ico')
    winMore.resizable(width=False, height=False)
    try:
        s = ([tree.item(x) for x in tree.selection()]) #Получаю выделенную строку
        s = s[0] #вытаскиваю словарь из списка
    except IndexError:
        winMore.destroy()
        return False
    d = s['values'] #вытаскиваю список из словаря
    BaseDC = sqlite3.connect(r"Lpro.db", uri=True)
    BaseDC.row_factory = sqlite3.Row
    CurDC = BaseDC.cursor()
    edited_d = d[0]
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
    TitleWinMore = d[0] + " - Подробности"
    winMore.title(TitleWinMore)
    winMore.minsize(width=600, height=200)
    #winMore.geometry("900x300")
    frameMore = Frame(winMore)
    frameMore.pack(side = TOP, expand=False)
    treeMore = ttk.Treeview(winMore)
    frameMore = Frame(winMore)
    treeMore = ttk.Treeview(frameMore, selectmode='browse', show='headings')
    scrollbar_vertical_More = ttk.Scrollbar(frameMore, orient='vertical', command = treeMore.yview)
    scrollbar_vertical_More.pack(side='right', fill=Y)
    treeMore.configure(yscrollcommand=scrollbar_vertical_More.set)
    treeMore.pack(side = BOTTOM, expand=True)
    frameMore.pack(side = BOTTOM, expand=True)
    treeMore["columns"]=("Punkt", "Parametr")
    treeMore.column("#0", width=50)
    treeMore.column("Punkt", width=160, stretch=True)
    treeMore.column("Parametr", width=380, stretch=True)
    treeMore.heading("#0", text="№:")
    treeMore.heading("Punkt", text="Пункт:")
    treeMore.heading("Parametr", text="Параметр:")
    treeMore.insert("" , '1', text='1', values=('Название:', d[0]))
    treeMore.insert("" , '2', text='2', values=('Тип ПО:', d[1]))
    treeMore.insert("" , '3', text='3', values=('Лицензия:', d[2]))
    treeMore.insert("" , '4', text='4', values=('Стоимость:', d[3]))
    size1 = None
    try:
        treeMore.insert("" , '5', text='5', values=('Путь:', IntallPath[d[0]]))
        size1 = (len(IntallPath[d[0]]))*7
    except KeyError:
        treeMore.insert("" , '5', text='5', values=('Путь:', 'Неизвестно'))
    try:
        dir = IntallPath[d[0]] + '\\' #IndexError:
        l1 = 0
        for root1, dirs, files in os.walk(dir):
            # пройти по директории рекурсивно
            for name in files:
                if name==spisokExe[0]:
                    fullname = os.path.join(root1, name) # получаем полное имя файла
                    treeMore.insert("" , '6', text='6', values=('Подтверждение:', fullname))
                    if size1 == None or size1<=len(fullname):
                        size1 = (len(fullname))*6
    except KeyError:
        treeMore.insert("" , '6', text='6', values=('Подтверждение:', 'Не найдено'))
    except IndexError:
        treeMore.insert("" , '6', text='6', values=('Подтверждение:', 'Не найдено'))
    try:
        if (len(IntallPath[d[0]]))>2:
            h=StartSeachKey(IntallPath[d[0]])
            h1 = h[0]
            treeMore.insert("" , '7', text='7', values=('Поиск слов "Купить":', h1['path']))
            size1 = (len(h1['path']))*6
        else:
            treeMore.insert("" , '7', text='7', values=('Поиск слов "Купить":', 'Не найдены'))
            if size1 == None:
                size1 = 380
    except:
        treeMore.insert("" , '7', text='7', values=('Поиск слов "Купить":', 'Не найдены'))
        if size1 == None:
            size1 = 380
    if size1 < 380:
        size1 = 380
    treeMore.pack(side = LEFT, expand=True)
    winMore.minsize(width=(size1+180), height=200)
    treeMore.column("Parametr", width=size1, stretch=True)

    CurDC.close()
    BaseDC.close()

root.bind('<Double-Button-1>', DoubleClic)

CurBLpro.close()
BaseLpro.close()
root.resizable(width=False, height=False)
#print ([tree.item(x) for x in tree.selection()]) ВЫДЕЛЕННАЯ СТРОКА

#Создаем окно
tree.pack()
root.mainloop()
