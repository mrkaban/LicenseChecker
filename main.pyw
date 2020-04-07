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
from CheckOS import *
from poisklicsogl import *

#Получаем данные из реестра в список(словари)
software_list = foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_32KEY) + foo(winreg.HKEY_LOCAL_MACHINE, winreg.KEY_WOW64_64KEY)+ foo(winreg.HKEY_CURRENT_USER, 0)

root = Tk()
root.title("LicenseChecker - Проверка легальности установленных программ")
root.iconbitmap('data\\LicenseChecker.ico')
katalog=''

#Функция для меню
def close_win():
    """Закрываем окно"""
    sys.exit()
def WebStr():
    """открытие веб-страницы в браузере по умолчанию"""
    webbrowser.open_new_tab("https://xn--90abhbolvbbfgb9aje4m.xn--p1ai/")
def WebHelp():
    """открытие веб-страницы в браузере по умолчанию"""
    webbrowser.open_new_tab("https://github.com/mrkaban/LicenseChecker/issues")
def PoiskZameni():
    """Поиск замены на сайте КонтинентСвободы.рф"""
    winPZ= Toplevel(root)
    winPZ.iconbitmap('data\\LicenseChecker.ico')
    winPZ.resizable(width=False, height=False)
    winPZ.title("Поиск замены на сайте КонтинентСвободы.рф")
    winPZ.minsize(width=200, height=210)
    framePZ = Frame(winPZ)
    L2 = Label(framePZ, text="Укажите ключевые слова для поиска (например, \"Графический редактор\") и нажмите \
кнопку 'Поиск'", pady=10, padx=0)
    L2.pack(side=TOP)
    L1 = Label(framePZ, text="Ключевое слово:")
    L1.pack(side = LEFT, expand = True)
    message = StringVar()
    E1 = Entry(framePZ, width=50, textvariable=message)
    E1.pack(side = LEFT, expand = True)
    def PoiskZameniDlyaKnopki(event=None):
        """Функция для кнопки поиск"""
        s = message.get()
        if s.find(" ", 0, len(s)) >= 1: #Только отдельно, удаление кавычек
             s = s.replace(" ", '+')
        url_kluch = 'https://xn--90abhbolvbbfgb9aje4m.xn--p1ai/component/search/?searchword='+s
        webbrowser.open_new_tab(url_kluch)
    E1.bind('<Return>', PoiskZameniDlyaKnopki)
    btnPoisk = Button(framePZ, text="Поиск", command=PoiskZameniDlyaKnopki)
    btnPoisk.pack(side = RIGHT, expand = True)
    framePZ.pack(side = TOP, expand=True)
    framePZ2 = Frame(winPZ)
    L3 = Label(framePZ2, text="Пишите кратко, иначе ничего не будет найдено. Если обнаружено мало замен, посмотрите в них\n\
под блоком с кнопкой скачать есть ссылки на похожие материалы. Также можно открыть категорию,\n\
где был найден аналог и посмотреть вручную.")
    L3.pack(side=BOTTOM)
    framePZ2.pack(side = TOP, expand=True)
    winPZ.transient(root) #не даём переключить фокус на главное окно
    winPZ.grab_set()
def Spravka():
    """Справка о программе"""
    winSpravka = Tk()
    winSpravka.iconbitmap('data\\LicenseChecker.ico')
    winSpravka.title("Справка о программе LicenseChecker")
    winSpravka.geometry("400x180")
    winSpravka.resizable(width=False, height=False)
    tab_control = ttk.Notebook(winSpravka)
    tab1 = Frame(tab_control)
    tab2 = Frame(tab_control)
    tab3 = Frame(tab_control)
    tab4 = Frame(tab_control)
    tab_control.add(tab1, text='Автопоиск')
    tab_control.add(tab2, text='Ручной поиск')
    tab_control.add(tab3, text='Медиа поиск')
    tab_control.add(tab4, text='Поиск в базе')
    #вкладка автопоиск
    labTab1=Label(tab1, text="Автоматический поиск", font='Arial 14 bold')
    labTab1.grid(column=0, row=0)
    labTab2=Label(tab1, text="Автоматический поиск срабатывает при запуске программы.\
                                \nПользователь при появлении окна видит его результаты.\
                                \nВсе данные берутся из системного реестра Windows\
                                \nНазвания фильтруются от версий, так как разработчики\
                                \nназвания своих программ в реестре указывают с версиями.\
                                \nЦены указываются примерные, могут не совпадать с реальными.\
                                \nПри двойном клике по строке открываются подробности.\
                                \nВ контекстном меню присутствует пункт копировать.", justify="left", pady=0, padx=1)
    labTab2.grid(column=0, row=2)
    #вкладка ручной поиск
    labTab3=Label(tab2, text="Ручной поиск программ", font='Arial 14 bold')
    labTab3.grid(column=0, row=0)
    labTab4=Label(tab2, text="Ручной поиск программ в указанной директории ищет все\
                                \nисполняемые файлы, собирает их в один список, а далее\
                                \nсравнивает элементы списка с базой данных.\
                                \nМожно указывать отдельную папку, или весь жесткий диск.\
                                \nСтепень обнаружения зависит от наполнения имен файл в базе\
                                \nили совпадением имени файла с названием программы.\
                                \nПри поиске учитываются только exe файлы.", justify="left", pady=0, padx=1)
    labTab4.grid(column=0, row=2)
    #вкладка медиа поиск
    labTab5=Label(tab3, text="Медиа поиск", font='Arial 14 bold')
    labTab5.grid(column=0, row=0)
    labTab6=Label(tab3, text="Медиа поиск позволяет найти в указанной папке все изображения,\
                                \nаудио и видео наиболее популярных форматов (.tiff, .jpeg, .bmp, .jpe,\
                                \n.jpg, .png, .gif, .psd, .mpeg, .flv, .mov, .m4a, .ac3, .aac, .h264,\
                                \n.m4v, .mkv, .mp4, .3gp, .avi, .ogg, .vob, .wma, .mp3, .wav, .mpg, .wmv).\
                                \nМожно указать минимальный размер обнаруживаемых файлов.\
                                \nДля поиска можно указывать отдельные папки или весь диск.", justify="left", pady=0, padx=1)
    labTab6.grid(column=0, row=2)
    #вкладка поиск в базе
    labTab7=Label(tab4, text="Поиск в базе данных", font='Arial 14 bold')
    labTab7.grid(column=0, row=0)
    labTab8=Label(tab4, text="Поиск в базе позволяет найти в ней программу по части названия.\
                                \nНапример, \'Архиватор WinRaR 3.53\', в базе достаточно набрать \'Winrar\'\
                                \nСама база данных хранится в папке с программой \\data\\Lpro.db.", justify="left", pady=0, padx=1)
    labTab8.grid(column=0, row=2)
    tab_control.pack(expand=1, fill='both')
    #winSpravka.transient(root) #не даём переключить фокус на главное окно
    #winSpravka.grab_set() #Тут работает с ошибкой!!!!!!!!!!!!!!
    winSpravka.mainloop()
def UpdateProg():
    """проверка наличия новой версии программы"""
    #my_version = '0.3'
    try:
        f = urllib.request.urlopen("https://github.com/mrkaban/LicenseChecker/raw/master/version")
        h = str(f.read())
    except:
        messagebox.showerror("Нет соединения с сервером", "Не удалось проверить наличие обновлений.")
        return
    search_exemple = re.search(r'1.0', h, re.M|re.I) # ТУТ НАДО ИСПРАВИТЬ ВЕРСИЮ ПРОГРАММЫ!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #if my_version != h:
    if not search_exemple:
        try:
            messagebox.showinfo("Обнаружена новая версия", "Сейчас будет открыта веб-страница с доступными релизами.\
Скачайте подходящую для Вас версию. Если не получается найти файлы, нажмите на \'Assets\'.")
            webbrowser.open_new_tab("https://github.com/mrkaban/LicenseChecker/releases")
        except:
            messagebox.showerror("Не получилось открыть страницу", "Не получилось открыть ссылку в веб-браузере.")
            return
    else:
        messagebox.showinfo("Программа актуальна", "Используемая Вами версия программы актуальна.")
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
        messagebox.showerror("Нет соединения с сервером", "Не удалось проверить наличие обновлений базы данных.")
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
                    messagebox.showerror("Не удалось синхронизировать БД", "Не удалось синхронизировать пользовательскую\
базу данных с основной. Проверьте наличие файла data\\User-DB.db в папке с программой.")
                    sinh = False
                if sinh == False:
                    txt1 = "База данных успешно обновлена до версии " + h + "!"
                else:
                    txt1 = "База данных успешно обновлена до версии " + h + "!" + "Пользовательская база данных успешно\
синхронизиррована с основной базой."
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
    winBD.iconbitmap('data\\LicenseChecker.ico')
    winBD.resizable(width=False, height=False)
    winBD.title("Поиск и просмотр базы данных")
    winBD.minsize(width=400, height=200)
    #winBD.geometry("900x300")
    frameBD2 = Frame(winBD)

    L2 = Label(frameBD2, text="Укажите название программы для поиска в базе данных и нажмите кнопку 'Поиск'")
    L2.pack(side=TOP)
    L1 = Label(frameBD2, text="Название:")
    L1.pack(side = LEFT, expand = True)
    message = StringVar()
    E1 = Entry(frameBD2, width=50, textvariable=message)
    E1.pack(side = LEFT, expand = True)

    def ViewBDDlyaKnopki(event=None):
        """Функция для кнопки поиск"""
        treeBD.delete(*treeBD.get_children())
        name_user_prog = message.get()
        BaseLproVDB = sqlite3.connect(r"data\Lpro.db", uri=True)
        BaseLproVDB.row_factory = sqlite3.Row #подключаем базу данных и курсор
        CurBLproVDB = BaseLproVDB.cursor()
        s = 'SELECT * FROM program WHERE (name LIKE "%%' + name_user_prog + '%%")'
        CurBLproVDB.execute(s)
        records = CurBLproVDB.fetchall()
        size_list=[]
        size2 = None
        added = False
        i = 1
        for row in records:
            size2= 0
            treeBD.insert("" , i-1, text=i, values=(row[1], row[2], row[3], row[4]))
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
        #winBD.minsize(width=size2, height=200)
        #заполняем таблицу
        treeBD["columns"]=("Name","Type", "Lic", "Cena")
        treeBD.column("#0", width=50)
        treeBD.column("Name", width=size2, stretch=True)
        treeBD.column("Type", width=150, stretch=True)
        treeBD.column("Lic", width=120, stretch=True)
        treeBD.column("Cena", width=80, stretch=True)
        treeBD.heading("#0", text="№:")
        treeBD.heading("Name", text="Название:")
        treeBD.heading("Type", text="Тип:")
        treeBD.heading("Lic", text="Лицензия:")
        treeBD.heading("Cena", text="~Цена:")
        #winBD.resizable(width=False, height=False)
        #treeBD.pack(side = BOTTOM)

    E1.bind('<Return>', ViewBDDlyaKnopki)
    btnPoisk = Button(frameBD2, text="Поиск", command=ViewBDDlyaKnopki)
    btnPoisk.pack(side = LEFT, expand = True)
    frameBD2.pack(side = TOP, expand=False)
    frameBD = Frame(winBD)
    treeBD = ttk.Treeview(winBD)

    treeBD = ttk.Treeview(frameBD, selectmode='browse')

    scrollbar_vertical = ttk.Scrollbar(frameBD, orient='vertical', command = treeBD.yview)

    scrollbar_vertical.pack(side='right', fill=Y)

    treeBD.configure(yscrollcommand=scrollbar_vertical.set)

    treeBD.pack(side = BOTTOM, fill=BOTH, expand=False)

    frameBD.pack(side = BOTTOM, expand=False)

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
    winBD.resizable(width=False, height=False)
    treeBD.pack(side = BOTTOM)
    #Создаем контекстное меню для ручного поиска
    def show_menu_BD(evt):
        pr_BD_menu.post(evt.x_root, evt.y_root)
    def CopyBD():
        try:
            s1 = ([treeBD.item(x) for x in treeBD.selection()]) #Получаю выделенную строку
            s1 = s1[0] #вытаскиваю словарь из списка
        except IndexError:
            return False
        d1 = s1['values']
        c = Tk()
        c.withdraw()
        c.clipboard_clear()
        c.clipboard_append(d1[0] + ' ' + d1[1]+ ' ' + d1[2]+ ' ' + d1[3])
        c.update()
        c.destroy()
    pr_BD_menu=Menu(frameBD, tearoff=False)
    pr_BD_menu.add_command(label="Копировать", command=CopyBD)
    treeBD.bind("<Button-3>", show_menu_BD)
    winBD.transient(root) #не даём переключить фокус на главное окно
    winBD.grab_set()

def about():
    """окно о программе"""
    winAbout= Toplevel(root)
    winAbout.iconbitmap('data\\LicenseChecker.ico')
    winAbout.resizable(width=False, height=False)
    winAbout.title("О программе LicenseChecker")
    winAbout.minsize(width=400, height=100)
    img = Image.open("data\\LicenseChecker.png")
    render = ImageTk.PhotoImage(img)
    initil = Label(winAbout, image=render)
    initil.image = render
    initil.pack(side = "left")
    lab=Label(winAbout, text="LicenseChecker 1.0", justify="left", font='Arial 14 bold')
    lab.pack(side = "top")
    lab4=Label(winAbout, text="\nЦель: Помочь разобраться с лицензиями \nна программное обеспечение", justify="left")
    lab4.pack()
    lab2=Label(winAbout, text="\nЛицензия: GNU GPL v2 \n\nРазработчик: Алексей Черемных (mrKaban) \n ", justify="left")
    lab2.pack()
    lab3=Label(winAbout, text="КонтинентСвободы.рф", justify="left", fg="blue")
    lab3.pack()
    lab3.bind('<Button-1>', WebStr)
    winAbout.transient(root) #не даём переключить фокус на главное окно
    winAbout.grab_set()
def RuchSearchProg():
    """Ручной поиск программ"""
    winRuch= Toplevel(root)
    winRuch.iconbitmap('data\\LicenseChecker.ico')
    winRuch.resizable(width=False, height=False)
    winRuch.title("Ручной поиск программ в указанной директории")
    #winRuch.minsize(width=400, height=200)
    winRuch.geometry("900x300")
    frameRuch2 = Frame(winRuch)

    kol_kat = None
    def UkazatOdinKatalog():
        global kol_kat
        btnRuchMen.config(text="1 каталог")
        kol_kat = 1
    def UkazatDvaKataloga():
        global kol_kat
        btnRuchMen.config(text="2 каталога")
        kol_kat = 2
    def UkazatTriKataloga():
        global kol_kat
        btnRuchMen.config(text="3 каталога")
        kol_kat = 3
    menu_ruch_but = tkinter.Menu(frameRuch2, tearoff=False)
    menu_ruch_but.add_command(label='1 каталог', command=UkazatOdinKatalog)
    menu_ruch_but.add_command(label='2 каталога', command=UkazatDvaKataloga)
    menu_ruch_but.add_command(label='3 каталога', command=UkazatTriKataloga)
    btnRuchMen = tkinter.ttk.Menubutton(frameRuch2, text="1 каталог", menu=menu_ruch_but)
    btnRuchMen.pack(side = LEFT)

    L2 = Label(frameRuch2, text="Укажите каталог для поиска следов программ и нажмите кнопку 'Поиск'")
    L2.pack(side=TOP)
    L1 = Label(frameRuch2, text="Каталог")
    L1.pack(side = LEFT, expand = True)
    message = StringVar()
    E1 = Entry(frameRuch2, width=50, textvariable=message)
    E1.pack(side = LEFT, expand = True)
    slovarSave= {}
    size_list=[]
    size2 = None
    kol_kat == None
    spisok_katalogov = []
    def OpenKatalog():
        """Открыть каталог"""
        global kol_kat
        if kol_kat == None or kol_kat == 1:
            E1.delete(first=0,last=50)
            katalog = tkinter.filedialog.askdirectory(parent=winRuch, title='Укажите директорию для поиска')
            E1.insert(0, katalog)
        if kol_kat == 2:
            E1.delete(first=0,last=50)
            katalog = tkinter.filedialog.askdirectory(parent=winRuch, title='Укажите 1 директорию для поиска')
            E1.insert(0, katalog)
            spisok_katalogov.append(katalog)
            katalog = tkinter.filedialog.askdirectory(parent=winRuch, title='Укажите 2 директорию для поиска')
            spisok_katalogov.append(katalog)
        if kol_kat == 3:
            E1.delete(first=0,last=50)
            katalog = tkinter.filedialog.askdirectory(parent=winRuch, title='Укажите 1 директорию для поиска')
            E1.insert(0, katalog)
            spisok_katalogov.append(katalog)
            katalog = tkinter.filedialog.askdirectory(parent=winRuch, title='Укажите 2 директорию для поиска')
            spisok_katalogov.append(katalog)
            katalog = tkinter.filedialog.askdirectory(parent=winRuch, title='Укажите 3 директорию для поиска')
            spisok_katalogov.append(katalog)
    def PoiskRuchnoiDlyaKnopki():
        """Функция для кнопки поиск"""
        treeRuch.delete(*treeRuch.get_children()) #очистка содержимого предыдущего поиска
        spisok=[]
        slovar={}
        size2= 0
        global kol_kat
        if kol_kat == None or kol_kat == 1:
            dir = message.get()
            for root, dirs, files in os.walk(dir): # пройти по директории рекурсивно
                 for name in files:
                     if name[-4:]=='.exe':
                         fullname = os.path.join(root, name) # получаем полное имя файла
                         slovar[name]=fullname
                         spisok.append(name)
        if kol_kat == 2:
            dir = spisok_katalogov[0]
            for root, dirs, files in os.walk(dir): # пройти по директории рекурсивно
                for name in files:
                    if name[-4:]=='.exe':
                        fullname = os.path.join(root, name) # получаем полное имя файла
                        slovar[name]=fullname
                        spisok.append(name)
            dir = spisok_katalogov[1]
            for root, dirs, files in os.walk(dir): # пройти по директории рекурсивно
                for name in files:
                    if name[-4:]=='.exe':
                        fullname = os.path.join(root, name) # получаем полное имя файла
                        slovar[name]=fullname
                        spisok.append(name)
        if kol_kat == 3:
            dir = spisok_katalogov[0]
            for root, dirs, files in os.walk(dir): # пройти по директории рекурсивно
                for name in files:
                    if name[-4:]=='.exe':
                        fullname = os.path.join(root, name) # получаем полное имя файла
                        slovar[name]=fullname
                        spisok.append(name)
            dir = spisok_katalogov[1]
            for root, dirs, files in os.walk(dir): # пройти по директории рекурсивно
                for name in files:
                    if name[-4:]=='.exe':
                        fullname = os.path.join(root, name) # получаем полное имя файла
                        slovar[name]=fullname
                        spisok.append(name)
            dir = spisok_katalogov[2]
            for root, dirs, files in os.walk(dir): # пройти по директории рекурсивно
                for name in files:
                    if name[-4:]=='.exe':
                        fullname = os.path.join(root, name) # получаем полное имя файла
                        slovar[name]=fullname
                        spisok.append(name)
        BaseLproRuch = sqlite3.connect(r"data\Lpro.db", uri=True)
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
                 size_list.append(((len(slovar[itemsoft]))*6))
                 #Создаю словари внутри словаря
                 slovarSave[row[1]] = {'Address':slovar[itemsoft], 'Name':row[1], 'TipPO':row[2], 'License':row[3], 'Cena':row[4]}
                 added = True
                 #break
                 i += 1
             if added == False:
                  #i = i -1
                 #Если не найдено в поле file, тогда ищем в поле name
                 s = 'SELECT * FROM program WHERE (name LIKE "' + NamePF + '%%")'
                 CurBLproRuch.execute(s)
                 records = CurBLproRuch.fetchall()
                 for row in records:
                     treeRuch.insert("" , i-1, text=i, values=(slovar[itemsoft], row[1], row[2], row[3], row[4]))
                     #Создаю словари внутри словаря
                     slovarSave[row[1]] = {'Address':slovar[itemsoft], 'Name':row[1], 'TipPO':row[2], 'License':row[3], 'Cena':row[4]}
                     added = True
                     #break
                     i += 1
        CurBLproRuch.close() #Закрываю соединение с базой и с курсором для базы
        BaseLproRuch.close()
        for itemsize in size_list:
            if size2 <= int(itemsize):
                size2 = int(itemsize)

        if size2 == None:
            size2 = 350
        if size2 < 350:
            size2 = 350
        #заполняем таблицу заново ради автоматического расширения ширины
        treeRuch["columns"]=("Name", "NameDB", "Type", "Lic", "Cena")
        treeRuch.column("#0", width=50)
        winRuch.minsize(width=(size2+550), height=200)
        treeRuch.column("Name", width=size2, stretch=True)
        treeRuch.column("NameDB", width=120, stretch=True)
        treeRuch.column("Type", width=150, stretch=True)
        treeRuch.column("Lic", width=120, stretch=True)
        treeRuch.column("Cena", width=80, stretch=True)
        treeRuch.heading("#0", text="№:") #убирать лишние определения колонок нельзя, иначе все криво
        treeRuch.heading("Name", text="Название:")
        treeRuch.heading("NameDB", text="В базе:")
        treeRuch.heading("Type", text="Тип:")
        treeRuch.heading("Lic", text="Лицензия:")
        treeRuch.heading("Cena", text="~Цена:")
        treeRuch.pack(side = BOTTOM, expand = True)

#str(datetime.now())
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
    frameRuch2.pack(side = TOP, expand=True)
    #Рисую таблицу для ручного поиска
    treeRuch = ttk.Treeview(winRuch)
    frameRuch = Frame(winRuch)

    treeRuch = ttk.Treeview(frameRuch, selectmode='browse')

    scrollbar_vertical = ttk.Scrollbar(frameRuch, orient='vertical', command = treeRuch.yview)

    scrollbar_vertical.pack(side='right', fill=Y)

    treeRuch.configure(yscrollcommand=scrollbar_vertical.set)

    treeRuch.pack(side = BOTTOM, expand=True)
    frameRuch.pack(side = BOTTOM, expand=True)
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
    #Создаем контекстное меню для ручного поиска
    def show_menu_Ruch(evt):
        pr_Ruch_menu.post(evt.x_root, evt.y_root)
    def CopyRuch():
        try:
            s1 = ([treeRuch.item(x) for x in treeRuch.selection()]) #Получаю выделенную строку
            s1 = s1[0] #вытаскиваю словарь из списка
        except IndexError:
            return False
        d1 = s1['values']
        c = Tk()
        c.withdraw()
        c.clipboard_clear()
        c.clipboard_append(d1[0] + ' ' + d1[1]+ ' ' + d1[2]+ ' ' + d1[3]+ ' ' + d1[4])
        c.update()
        c.destroy()
    pr_Ruch_menu=Menu(frameRuch, tearoff=False)
    pr_Ruch_menu.add_command(label="Копировать", command=CopyRuch)
    treeRuch.bind("<Button-3>", show_menu_Ruch)
    winRuch.transient(root) #не даём переключить фокус на главное окно
    winRuch.grab_set()


#Сохранить отчет автопоиска
slovarSave = {}
def SaveAuto():
    """Сохранить отчет в HTML"""
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
    winMedia.iconbitmap('data\\LicenseChecker.ico')
    winMedia.resizable(width=False, height=False)
    winMedia.title("Поиск медиа файлов (аудио, видео, изображения) в указанной директории")
    #winMedia.minsize(width=480, height=200)
    #winMedia.geometry("480x200")
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


    #Рисую таблицу для ручного поиска
    treeMed = ttk.Treeview(winMedia)
    frameMed = Frame(winMedia)

    treeMed = ttk.Treeview(frameMed, selectmode='browse')

    scrollbar_vertical = ttk.Scrollbar(frameMed, orient='vertical', command = treeMed.yview)

    scrollbar_vertical.pack(side='right', fill=Y)

    treeMed.configure(yscrollcommand=scrollbar_vertical.set)

    treeMed.pack(side = BOTTOM, expand=True)
    frameMed.pack(side = BOTTOM, expand=True)
    size_list=[]
    size2 = None
    slovarMediaSave= {}
    def OpenMedKatalog():
        """Открыть каталог"""
        E1.delete(first=0,last=50)
        katalog = tkinter.filedialog.askdirectory(parent=winMedia, title='Укажите директорию для поиска')
        E1.insert(0, katalog)
    def PoiskMediaDlyaKnopki():
        """Функция для кнопки поиск"""
        treeMed.delete(*treeMed.get_children()) #очистка содержимого предыдущего поиска
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
                         size_list.append(((len(fullname))*6))
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
            razmerFile = os.path.getsize(slovar[itemsoft])
            razmerFile = round(((razmerFile/1024)/1024), 2)
            razmerFileStr = str(razmerFile) + ' МБ'
            treeMed.insert("" , i-1, text=i, values=(slovar[itemsoft], TipFile, razmerFileStr))
            slovarMediaSave[slovar[itemsoft]] = {'File':slovar[itemsoft], 'Tip':TipFile, 'Size':razmerFileStr}
            i += 1
            size2= 0
            for itemsize in size_list:
                if size2 <= int(itemsize):
                    size2 = int(itemsize)
            if size2 == None:
                size2 = 350
            if size2 < 350:
                size2 = 350
            #treeMed["columns"]=("Name", "Type", "Size")
            #winMedia.minsize(width=size2+180, height=200)
            # frameMed=Frame(winMedia,width=size2+180)
            # treeMed.column("#0", width=50)
            # treeMed.column("Name", width=size2, stretch=True)
            # treeMed.column("Type", width=150, stretch=True)
            # treeMed.column("Size", width=120, stretch=True)
            # treeMed.heading("#0", text="№:")
            # treeMed.heading("Name", text="Имя файла:")
            # treeMed.heading("Type", text="Тип:")
            # treeMed.heading("Size", text="Размер:")
            # treeMed.pack(side = LEFT, expand=True)
            # frameMed2.pack(side = TOP, expand=True)
            # frameMed.pack(side = BOTTOM, expand=True)
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
    frameMed2.pack(side = TOP, expand=True)
    #заполняем таблицу
    treeMed["columns"]=("Name", "Type", "Size")
    treeMed.column("#0", width=50)
    treeMed.column("Name", width=500, stretch=True)
    treeMed.column("Type", width=150, stretch=True, anchor=CENTER)
    treeMed.column("Size", width=120, stretch=True, anchor=CENTER)
    treeMed.heading("#0", text="№:")
    treeMed.heading("Name", text="Имя файла:")
    treeMed.heading("Type", text="Тип:")
    treeMed.heading("Size", text="Размер:")
    #Создаем контекстное меню для медиа поиска
    def show_menu_media(evt):
        pr_media_menu.post(evt.x_root, evt.y_root)
    def Copymedia():
        try:
            s1 = ([treeMed.item(x) for x in treeMed.selection()]) #Получаю выделенную строку
            s1 = s1[0] #вытаскиваю словарь из списка
        except IndexError:
            return False
        d1 = s1['values']
        c = Tk()
        c.withdraw()
        c.clipboard_clear()
        c.clipboard_append(d1[0] + ' ' + d1[1]+ ' ' + d1[2])
        c.update()
        c.destroy()
    pr_media_menu=Menu(frameMed, tearoff=False)
    pr_media_menu.add_command(label="Копировать", command=Copymedia)
    treeMed.bind("<Button-3>", show_menu_media)

    treeMed.pack(side = LEFT, expand=True)
    winMedia.transient(root) #не даём переключить фокус на главное окно
    winMedia.grab_set()
### конец медиа поиска

#АВТОПОИСК

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
pm.add_command(label="Поиск замены на КонтинентСвободы.рф", command=PoiskZameni)
hm=Menu(m)
m.add_cascade(label="?", menu=hm)
hm.add_command(label="О программе", command=about)
hm.add_command(label="Справка", command=Spravka)
hm.add_command(label="Официальный сайт", command=WebStr)
hm.add_command(label="Служба поддержки", command=WebHelp)
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

#Создаем контекстное меню

def show_menu_root(evt):
    pr_root_menu.post(evt.x_root, evt.y_root)
def CopyRoot():
    try:
        s1 = ([tree.item(x) for x in tree.selection()]) #Получаю выделенную строку
        s1 = s1[0] #вытаскиваю словарь из списка
    except IndexError:
        return False
    d1 = s1['values']
    c = Tk()
    c.withdraw()
    c.clipboard_clear()
    c.clipboard_append(d1[0] + ' ' + d1[1]+ ' ' + d1[2]+ ' ' + d1[3])
    c.update()
    c.destroy()
def Podrobnee():
    tree.event_generate("<<DblClick>>")
    DoubleClic(event=None)
pr_root_menu=Menu(frame, tearoff=False)
pr_root_menu.add_command(label="Копировать", command=CopyRoot)
pr_root_menu.add_command(label="Подробнее", command=Podrobnee)

#Добавляю ОС и стоимость
name_os, cena_os = DetectOS()
tree.insert("" , 1, text='1', values=(name_os, 'Платное ПО', 'Shareware', cena_os))
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
    winMore.iconbitmap('data\\LicenseChecker.ico')
    winMore.resizable(width=False, height=False)
    i1 = 1
    try:
        s = ([tree.item(x) for x in tree.selection()]) #Получаю выделенную строку
        s = s[0] #вытаскиваю словарь из списка
    except IndexError:
        winMore.destroy()
        return False
    d = s['values'] #вытаскиваю список из словаря
    BaseDC = sqlite3.connect(r"data\Lpro.db", uri=True)
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
    winMore.minsize(width=600, height=250)
    #winMore.geometry("900x300")
    frameMore = Frame(winMore)
    frameMore.pack(side = TOP, expand=False)
    treeMore = ttk.Treeview(winMore)
    frameMore = Frame(winMore)
    treeMore = ttk.Treeview(frameMore, selectmode='browse', show='headings', height=12)
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
    treeMore.insert("" , i1, text=i1, values=('Название:', d[0]))
    i1 += 1
    treeMore.insert("" , i1, text=i1, values=('Тип ПО:', d[1]))
    i1 += 1
    treeMore.insert("" , i1, text=i1, values=('Лицензия:', d[2]))
    i1 += 1
    treeMore.insert("" , i1, text=i1, values=('Стоимость:', d[3]))
    i1 += 1
    size1 = None
    try:
        treeMore.insert("" , i1, text=i1, values=('Путь:', IntallPath[d[0]]))
        i1 += 1
        size1 = (len(IntallPath[d[0]]))*7
    except KeyError:
        treeMore.insert("" , i1, text=i1, values=('Путь:', 'Неизвестно'))
        i1 += 1
    try:
        dir = IntallPath[d[0]] + '\\' #IndexError:
        l1 = 0
        for root1, dirs, files in os.walk(dir):
            # пройти по директории рекурсивно
            for name in files:
                if name==spisokExe[0]:
                    fullname = os.path.join(root1, name) # получаем полное имя файла
                    treeMore.insert("" , i1, text=i1, values=('Подтверждение:', fullname))
                    i1 += 1
                    if size1 == None or size1<=len(fullname):
                        size1 = (len(fullname))*6
    except KeyError:
        treeMore.insert("" , i1, text=i1, values=('Подтверждение:', 'Не найдено'))
        i1 += 1
    except IndexError:
        treeMore.insert("" , i1, text=i1, values=('Подтверждение:', 'Не найдено'))
        i1 += 1
    try:
        if (len(IntallPath[d[0]]))>2:
            h=StartSeachKey(IntallPath[d[0]])
            h1 = h[0]
            treeMore.insert("" , i1, text=i1, values=('Поиск слов "Купить":', h1['path']))
            i1 += 1
            size1 = (len(h1['path']))*6
        else:
            treeMore.insert("" , i1, text=i1, values=('Поиск слов "Купить":', 'Не найдены'))
            i1 += 1
            if size1 == None:
                size1 = 380
    except:
        treeMore.insert("" , i1, text=i1, values=('Поиск слов "Купить":', 'Не найдены'))
        i1 += 1
        if size1 == None:
            size1 = 380
    if size1 < 380:
        size1 = 380
    #i1 = 8
    search_exemple = re.search( r'Windows', d[0], re.M|re.I)
    if search_exemple:
        treeMore.insert("" , i1, text=i1, values=('Ключ Windows:', get_windows_product_key_from_reg()))
        i1 += 1
        i2 = 0
        sled_spisok = sled_activation()
        for sled in sled_spisok:
            #i1 = i1 + 1
            if i1 <= i2:
                treeMore.insert("" , i1, text=i1, values=('-', sled))
                i1 += 1
                i2 += 1
            else:
                treeMore.insert("" , i1, text=i1, values=('Следы активации:', sled))
                i1 += 1
                i2 = i1
    try:
        if (len(IntallPath[d[0]])) > 0:
            spisok_lic_sogl = poisk_lic_sogl(IntallPath[d[0]])
            i2 = 0
            for lic_sogl in spisok_lic_sogl:
                if i1 <= i2:
                    treeMore.insert("" , i1, text=i1, values=('-', lic_sogl))
                    i1 += 1
                    i2 += 1
                else:
                    treeMore.insert("" , i1, text=i1, values=('Лицензионное соглашение:', lic_sogl))
                    i1 += 1
                    i2 = i1
        else:
            treeMore.insert("" , i1, text=i1, values=('Лицензионное соглашение:', 'Не найдено'))
            i1 += 1
    except KeyError:
        treeMore.insert("" , i1, text=i1, values=('Лицензионное соглашение:', 'Корневой каталог приложения не указан'))
        i1 += 1
    def show_menu(evt):
        pr_menu.post(evt.x_root, evt.y_root)
    def CopyDC():
        try:
            s1 = ([treeMore.item(x) for x in treeMore.selection()]) #Получаю выделенную строку
            s1 = s1[0] #вытаскиваю словарь из списка
        except IndexError:
            return False
        d1 = s1['values']
        c = Tk()
        c.withdraw()
        c.clipboard_clear()
        c.clipboard_append(d1[1])
        c.update()
        c.destroy()
    pr_menu=Menu(winMore, tearoff=False)
    pr_menu.add_command(label="Копировать", command=CopyDC)
    treeMore.bind("<Button-3>", show_menu)
    winMore.minsize(width=(size1+180), height=250)
    treeMore.pack(side = LEFT, expand=True)
    treeMore.column("Parametr", width=size1, stretch=True)
    CurDC.close()
    BaseDC.close()
    winMore.transient(root) #не даём переключить фокус на главное окно
    winMore.grab_set()

root.bind('<Double-Button-1>', DoubleClic)
tree.bind("<Button-3>", show_menu_root)

CurBLpro.close()
BaseLpro.close()
root.resizable(width=False, height=False)
#print ([tree.item(x) for x in tree.selection()]) ВЫДЕЛЕННАЯ СТРОКА

#Создаем окно
tree.pack()
root.mainloop()
