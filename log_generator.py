import os
import shutil
import datetime
import random
from pathlib import Path

"""Нужно исправить лишнюю точку в переименовании и выполнить журналирование"""

date_time = datetime.datetime.now()
date = f'{date_time.date()}'
time = f'{date_time.time()}'[:8]

path = Path("C:\\", "Users", "OMEN", "Desktop", "Folder", "somefiles", "files", "logs")
#path = Path("/Users","warlock","Desktop","Users", "OMEN", "Desktop", "Folder", "somefiles", "files", "logs")
#print(path)
#print(os.path.dirname(os.path.abspath(__file__)))
def random_text(lenght):
    text = ''.join([random.choice('01234 56789 qwertyuiop asdfghjk lzxcv bnm') for _ in range(lenght)])
    return text

def logs_generator(target: str, amount: str):
    files_num = 1
    modules = ['nwing', 'support', 'atm']
    numbers = []
    for _ in range(amount):
        number = ''.join([random.choice('0123456789') for _ in range(10)])
        module = random.choice(modules)
        file_name = Path(target, f'{module+ str(files_num)}.txt')
        with open(file_name, 'w', encoding='utf-8') as log_file:
            log_file.write(f'{date}{time}\n')
            log_file.write(f'{module} {random_text(30)} \n')
            log_file.write(f'{random_text(300)} \n')
            log_file.write(f'{random_text(100)} \n')
            log_file.write(f'{random_text(15)} {number} {random_text(10)}\n')
            log_file.write(f'{random_text(25)}{number}{random_text(20)}\n')
            log_file.write(f'{random_text(340)} \n')
        files_num += 1
        numbers.append(number)
    return numbers

def rename(path, ext):
    for i in os.listdir(path):
        file = i.split('.')[0]
        if not os.path.isfile(f'{path}{i}.{ext}'):
            name = f'{file}.{ext}'
            os.rename(Path(path,i), Path(path,name))

numbers = logs_generator(path, 1000)
rename(str(path), 'log')
print(random.choice(numbers))