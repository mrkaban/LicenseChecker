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
dir = 'D:\\клипы\\'
for root, dirs, files in os.walk(dir):
     # пройти по директории рекурсивно
     SpisokFormatov = ['.tiff', '.jpeg', '.bmp', '.jpe', '.jpg', '.png', '.gif', '.psd', '.mpeg', '.flv', '.mov', '.m4a', '.ac3', '.aac',
     '.h264', '.m4v', '.mkv', '.mp4', '.3gp', '.avi', '.ogg', '.vob', '.wma', '.mp3', '.wav', '.mpg', '.wmv']
     for name in files:
         for format in SpisokFormatov:
             if name[-4:]==format:
                 fullname = os.path.join(root, name) # получаем полное имя файла
                 slovar[name]=fullname
                 spisok.append(name)
root = Tk()

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
tree["columns"]=("Name", "Type", "Size")
tree.column("#0", width=50)
tree.column("Name", width=350, stretch=True)
tree.column("Type", width=150, stretch=True)
tree.column("Size", width=120, stretch=True)
tree.heading("#0", text="№:")
tree.heading("Name", text="Имя файла:")
tree.heading("Type", text="Тип:")
tree.heading("Size", text="Размер:")


size1 = None
size2 = None
slovarSave= {}
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
    tree.insert("" , i-1, text=i, values=(slovar[itemsoft], TipFile, razmerFileStr))
    #     slovarSave[row[1]] = {'Address':slovar[itemsoft], 'Name':row[1], 'TipPO':row[2], 'License':row[3], 'Cena':row[4]}
    i += 1
if size1 == None:
    size1 = 380
if size2 == None:
    size2 = 120
tree.pack(side = LEFT, expand=True)
root.minsize(width=(size1+ size2 + 180), height=200)
tree.column("Name", width=size1, stretch=True)
tree.column("Size", width=size2, stretch=True)

#Создаем окно
tree.pack()
root.mainloop()
