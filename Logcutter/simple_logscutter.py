import os
import shutil
import datetime
import random
from pathlib import Path
import re

utrno = 7773414119
date_time = datetime.datetime.now()
date = f'{date_time.date()}'

src_path = Path("C:\\", "Users", "OMEN", "Desktop", "Folder", "somefiles", "files", "logs") # Windows
target_folder = Path("C:\\", "Users", "OMEN","Desktop","Folder", "somefiles", "files", "copies", f"{utrno}_{date}") #Windows
#src_path = Path("/Users","warlock","Desktop","Users", "OMEN", "Desktop", "Folder", "somefiles", "files", "logs") #Linux
#target_folder = Path("/Users","warlock","Desktop","Users", "OMEN", "Desktop", "Folder", "somefiles", "files", "copies", f"{utrno}_{date}") #Linux

def finder(path, target):
    list_of_files = []
    for i in os.listdir(path):
        #Сюда нужно добавить обработчик патерна, окончания файла лог
        with open(Path(path, i), 'r') as file:
            for line in file:
                result = re.findall(target, line)
                #Проблема поиск возвращает не только вхождение но и [] которые не обработать
                if len(result) >= 1: # пока только так
                    list_of_files.append(i)
    return list_of_files

list_of_files = finder(src_path, f'{utrno}')
print(list_of_files)
if not os.path.exists(target_folder):
    os.makedirs(target_folder, exist_ok=True)





for i in list_of_files:
    src_file = Path(src_path, i)
    target_file = Path(target_folder,i)
    shutil.copy(src_file, target_file)


"""Если парамметры поиска будут отличаться, то можно будет переконфигурировать в ООП"""