from tkinter import *
import tkinter.ttk as ttk
import sqlite3
import webbrowser #Для открытия веб-страницы
from htmltree import *
from tkinter import filedialog
from tkinter import messagebox
import os
spisok=[]
slovar={}
#dir = 'C:\\'
dir = 'C:\\Program Files\\'
for root, dirs, files in os.walk(dir):
     # пройти по директории рекурсивно
     for name in files:
         if name[-4:]=='.exe':
             fullname = os.path.join(root, name) # получаем полное имя файла
             slovar[name]=fullname
             spisok.append(name)

root = Tk()

#Функция для меню
def close_win():
    """Закрываем окно"""
    root.destroy()
def about():
    """окно о программе"""
    win= Toplevel(root)
    win.title("О программе LicenseCheker")
    win.minsize(width=200, height=100)
    lab=Label(win, text="LicenseCheker 1.0 \nЛицензия: GNU GPL v2 \nРазработчик: Алексей Черемных mrKaban \n\
Официальный сайт: КонтинентСвободы.рф", justify="left", relief="ridge")
    lab.pack()
def WebStr():
    """открытие веб-страницы в браузере по умолчанию"""
    webbrowser.open_new_tab("https://xn--90abhbolvbbfgb9aje4m.xn--p1ai/")
def Save():
    SbHTML = """
<h1 align=center>Lpro - Проверка лицензий установленных программ</h1>
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
    """
    SbHTML = SbHTML + s2
    head = Head()
    body = Body(SbHTML)
    doc = Html(head, body)

    ftypes = [('HTML', '.html')]
    file_name = filedialog.asksaveasfilename(filetypes=ftypes, defaultextension='.html')
    fileurl = doc.renderToFile(file_name)
    messagebox.showinfo("Файл сохранен", "Файл успешно сохранен: " + file_name)


#Создание меню
m=Menu(root)
root.config(menu=m)
fm=Menu(m)
m.add_cascade(label="Файл", menu=fm)
fm.add_command(label="Выход", command=close_win)
fm.add_command(label="Сохранить", command=Save)
hm=Menu(m)
m.add_cascade(label="?", menu=hm)
hm.add_command(label="О программе", command=about)
hm.add_command(label="Официальный сайт", command=WebStr)

#Рисуем таблицу
tree = ttk.Treeview(root)

frame = Frame(root)

tree = ttk.Treeview(frame, selectmode='browse')

scrollbar_vertical = ttk.Scrollbar(frame, orient='vertical', command = tree.yview)

scrollbar_vertical.pack(side='right', fill=Y)

tree.configure(yscrollcommand=scrollbar_vertical.set)

tree.pack(side=LEFT, fill=BOTH, expand=False)

frame.pack(expand=False)

#заполняем таблицу
tree["columns"]=("Name", "NameDB", "Type", "Lic", "Cena")
tree.column("#0", width=50)
tree.column("Name", width=350, stretch=True)
tree.column("NameDB", width=120, stretch=True)
tree.column("Type", width=150, stretch=True)
tree.column("Lic", width=120, stretch=True)
tree.column("Cena", width=80, stretch=True)
tree.heading("#0", text="№:")
tree.heading("Name", text="Название:")
tree.heading("NameDB", text="В базе:")
tree.heading("Type", text="Тип:")
tree.heading("Lic", text="Лицензия:")
tree.heading("Cena", text="~Цена:")
#i = 1
#for itemsoft in software_list:
#    tree.insert("" , i-1, text=i, values=(itemsoft['name'], itemsoft['version'], itemsoft['publisher']))
#    i += 1

#Пробую работать с SQLite
BaseLpro = sqlite3.connect(r"Lpro.db", uri=True)
BaseLpro.row_factory = sqlite3.Row
CurBLpro = BaseLpro.cursor()

#print(fullname)
slovarSave= {}
i = 1
for itemsoft in spisok:
     NameP=itemsoft
     NamePF = NameP.replace((NameP[NameP.find('.exe'):]), '')
     #s = 'SELECT * FROM program WHERE (name LIKE "' + itemsoft['name'] + '%%")'
     s = 'SELECT * FROM program WHERE (file LIKE "' + NamePF + '")'
     CurBLpro.execute(s)
     records = CurBLpro.fetchall()
     for row in records:
         tree.insert("" , i-1, text=i, values=(slovar[itemsoft], row[1], row[2], row[3], row[4]))
         slovarSave[row[1]] = {'Address':slovar[itemsoft], 'Name':row[1], 'TipPO':row[2], 'License':row[3], 'Cena':row[4]}
         break
     i += 1
#print(slovar)
CurBLpro.close()
BaseLpro.close()

#Создаем окно
tree.pack()
root.mainloop()
