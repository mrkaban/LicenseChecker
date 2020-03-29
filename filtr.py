


def filter(NameProg):
    edited_NameProg = NameProg

    if NameProg.find("\"", 0, len(NameProg)) >= 1: #Только отдельно, удаление кавычек
         edited_NameProg = NameProg.replace("\"", '')

    spisok = (" CC", " CS", " cc", " cs", " CC 2015", " CC 2016", " CC 2017", " CC 2018", " CC 2019", " CC 2020", " CC 2021", " CC 2022",
    " 2015.1", " 2015.2", " 2015.3", " 2015.4", " 2015.5", " 2016.1", " 2016.2", " 2016.3", " 2016.4", " 2016.5", " 2017.1", " 2017.2",
    " 2017.3", " 2017.4", " 2017.5", " 2018.1", " 2018.2", " 2018.3", " 2018.4", " 2018.5", " 2019.1", " 2019.2", " 2019.3", " 2019.4",
    " 2019.5", " 2020.1", " 2020.2", " 2020.3", " 2020.4", " 2020.5", " 2021.1", " 2021.2", " 2021.3", " 2021.4", " 2021.5", " 2022.1",
    " 2022.2", " 2022.3", " 2022.4", " 2022.5", " (2015", " (2016", " (2017", " (2018", " (2019", " (2007", " (2008", " (2009", " (2010",
    " (2011", " (2012", " (2013", " (2014", " (2020", " (2021", " (2022", " (v0", " (v1", " (v2", " (v3", " (v4", " (v5", " (v6", " (v7",
    " (v8", " (v9", " v0", " v1", " v2", " v3", " v4", " v5", " v6", " v7", " v8", " v9", " v 0.", " v 1.", " v 2.", " v 3.", " v 4.",
    " v 5.", " v 6.", " v 7.", " v 8.", " v 9.", " v.0", " v.1", " v.2", " v.3", " v.4", " v.5", " v.6", " v.7", " v.8", " v.9", " v. 0",
    " v. 1", " v. 2", " v. 3", " v. 4", " v. 5", " v. 6", " v. 7", " v. 8", " v. 9", ", версия", " (версия", " (Версия", ", version",
    " (version", " (Version", " версия", " version", " Версия", " Version", " Ver.", " ver.", " (Version", " (x64", " x64", " (x86",
    " x86", "-x64", " - 64 bit", " (32-разрядная", " (32-Bit", " (32-bit", " (32 bit", " (64-разрядная", " (64-Bit", " (64-bit", " (64 bit",
    " 64-bit", " 32-bit", "64-bit", "32-bit", " 64 bit", " 32 bit", " (V0", " (V1", " (V2", " (V3", " (V4", " (V5", " (V6", " (V7", " (V8",
    " (V9", " V0", " V1", " V2", " V3", " V4", " V5", " V6", " V7", " V8", " V9", " V.0", " V.1", " V.2", " V.3", " V.4", " V.5", " V.6",
    " V.7", " V.8", " V.9", " V. 0", " V. 1", " V. 2", " V. 3", " V. 4", " V. 5", " V. 6", " V. 7", " V. 8", " V. 9", "_64b", " 64b",
    " Trial", " trial", " demo", " Demo", " (Trial", " (trial", " (demo", " (Demo", " with update", " with Update", " With Update",
    " With update", " (build", " (Build", " (0.", " (1.", " (2.", " (3.", " (4.", " (5.", " (6.", " (7.", " (8.", " (9.", " (10.", " -0.",
    " -1.", " -2.", " -3.", " -4.", " -5.", " -6.", " -7.", " -8.", " -9.", " XE8", " XE2", " XE4", " XE6", "™", "-64", " X5", " X6",
    " x5", " x6", " (remove", " (Remove", " [rev", " - English", " 0-", " 1-", " 2-", " 3-", " 4-", " 5-", " 6-", " 7-", " 8-", " 9-",
    " (учебная", " (Учебная", " (Учебная", " (только удаление", " 0.",  " 1.", " 2.", " 3.", " 4.", " 5.", " 6.", " 7.", " 8.", " 9.",
    " 10", " 11", " 12", " 13", " 14", " 15", " 16", " 17", " 18", " 19", ", ", " version ")

    for x in spisok:
        if edited_NameProg.find(x, 0, len(edited_NameProg)) >= 1:
            n = edited_NameProg[edited_NameProg.find(x):]
            edited_NameProg = edited_NameProg.replace(n, '')
    i = 0
    cifri=("1", "2", "3", "4", "5", "6", "7", "8", "9")
    while i < 100:    #Фильтруем 10, 21 и т.п.
            for cifra in cifri:
                f = str(i) + cifra
                f = " " + f
                if edited_NameProg.find(f, 0, len(edited_NameProg)) >= 1:
                    n = edited_NameProg[edited_NameProg.find(f):]
                    edited_NameProg = edited_NameProg.replace(n, '')
            i += 1
    i = 0
    while i < 100:    #Фильтруем 11.1 и т.п.
            for cifra in cifri:
                f = str(i) + "."
                f1 = " " + f
                f2 = "-" + f
                if edited_NameProg.find(f, 0, len(edited_NameProg)) >= 1:
                    n = edited_NameProg[edited_NameProg.find(f):]
                    edited_NameProg = edited_NameProg.replace(n, '')
                elif edited_NameProg.find(f1, 0, len(edited_NameProg)) >= 1:
                    n = edited_NameProg[edited_NameProg.find(f1):]
                    edited_NameProg = edited_NameProg.replace(n, '')
                elif edited_NameProg.find(f2, 0, len(edited_NameProg)) >= 1:
                    n = edited_NameProg[edited_NameProg.find(f2):]
                    edited_NameProg = edited_NameProg.replace(n, '')
            i += 1

    VS_spisok=(" 2015", " 2016", " 2017", " 2018", " 2019", " 2007", " 2008", " 2009", " 2010", " 2011", " 2012",
    " 2013", " 2014", " 2020", " 2021", " 2022") #Чтобы исключить некорректную фильтрацию из Microsoft Visual Studio
    for d in VS_spisok:
        if edited_NameProg.find("Microsoft Visual Studio", 0, len(edited_NameProg)) <= 1:
            if edited_NameProg.find(d, 0, len(edited_NameProg)) >= 1:
                n = edited_NameProg[edited_NameProg.find(d):]
                edited_NameProg = edited_NameProg.replace(n, '')
        if edited_NameProg.find("Microsoft Visual Studio", 0, len(edited_NameProg)) >= 1:
            if edited_NameProg.find(d, 0, len(edited_NameProg)) >= 1:
                 edited_NameProg = edited_NameProg.replace(d, '')


    return edited_NameProg
