import os
import shutil
import datetime
import random
from pathlib import Path
import re

#path = Path("C:\\", "Users", "OMEN", "Desktop", "Folder", "somefiles", "files", "logs")
path = Path("/Users","warlock","Desktop","Users", "OMEN", "Desktop", "Folder", "somefiles", "files", "logs")

def finder(path, target):
    list_of_files = []
    for i in os.listdir(path):
        with open(Path(path, i), 'r') as file:
            for line in file:
                result = re.findall(target, line)
                #Проблема поиск возвращает не только вхождение но и [] которые не обработать
                if len(result) >= 1: # пока только так
                    list_of_files.append(i)
    return list_of_files

result = finder(path, '105757775')
print(result)
