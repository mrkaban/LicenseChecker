# LicenseCheker
LicenseCheker - Программа для проверки легальности используемого программного обеспечения

В программе присутствует автоматический поиск с возможностью просмотра подробной информации о найденных программах, ручной поиск, медиа поиск, просмотр базы данных, обновление базы данных и проверка новых версий программы. Полностью на русском языке.

Официальная веб-страница программы: https://континентсвободы.рф/утилиты/система/licensecheker-легальность-программ.html

LicenseCheker написана при помощи интерпретатора Python 3.8.2 и следующих бибилиотек: urllib, winreg, tkinter, sqlite3, webbrowser, os, datetime, socket, PIL, platform, wmi, re, io, glob, future

Известные на данный момент ошибки:

-в ручном поиске по умолчанию указано "1 каталог", но при нажатии обзор просит указать два каталога;
-проблемы с вычислением ширины окна в ручном поиске при появлении в результатах слишком длинных путей;
-отсутствие автоматической настройки ширины в медиа-поиске.

Планируется в долгосрочной перспективе:

-изучение с возможным переходом библиотек PyQT и wxPython;

-сортировка результатов поиска;

-окраска результатов, согласно типу ПО (зеленый, желтый и красный);

-поиск игр;
-итоговая сумма;
-средство просмотра ключей реестра;
-запуск программы с параметрами для автоматизации всех видов поиска без участия пользователя, позволяющее упростить работу системных администраторов с большим парком компьютеров.

Планируется в ближайшей перспективе:

-оптимизация кода (в данный момент основные функции содержатся в файле main.pyw, планируется разнести их по отдельным файлам);
-исправление ошибок, указанных в разделе "известные ошибки".
