#! usr/bin/python

"""Вводный блок"""

import os
import shutil
import datetime
from pathlib import Path
import subprocess as sub
date_time = datetime.datetime.now()
date = f'{date_time.date()}'
#Задаем путь до папки с лог файлами
src_folder = Path('..', '..')
#Задаем путь и имя до конечной папки, куда будет выведен результат и копии лог-файлов
target_folder = Path('..', '..')
BORDER = '*************************************************************************************\n'

"""Инфраструктурный блок"""
patern = int(input())
# Ищем файлы с содержанием патерна с помощью grep
args = [f'grep -l {patern} {src_folder}/*']
grep = sub.Popen(args, shell = True, stdout = sub.PIPE)
print(f'Дана команда grep для поиска {patern} в содержании файла {src_folder}')
result = str(grep.communicate()[0])[2:] # преобразуем из битового в строковый
# Обработка имен файлов
list_of_files = [file for file in result.split('\\') if len(file) > 2] # Обрасываем имена системных файлов
list_of_files = [name.split('/')[-1] for name in list_of_files]

#Создание папки для копий файлов с логами
if not os.path.exists(target_folder):
    os.makedirs(target_folder, exist_ok=True)
    print(f'Создана папка {target_folder}')

#У некоторых файлов нестандартное (цифровое) окончание наименования,
# поэтому для корректной работы необходимо перенести цифровую часть имени файла
# и чтобы не перебирать список два раза результирующие файлы копируем в новую папку
for i in list_of_files:
    if len(i.split('.')) > 2:
        target_file = Path(target_folder, '.'.join((i.split('/')[-1].split('.')[:2])))
        src_file = Path(src_folder, i.split('/')[-1])
        shutil.copy(src_file, target_file)
        list_of_files.remove(i)
        list_of_files.insert(0, '.'.join((i.split('/')[-1].split('.')[:2])))
    else:
        target_file = Path(target_folder, i.split('/')[-1])
        src_file = Path(src_folder, i.split('/')[-1])
        shutil.copy(src_file, target_file)
print(f'Файлы скопированы в папку {target_folder}')

"""Функциональный блок"""

def cutter(content, patern, border = BORDER):
    """Центральная функция определяющая блок лога, который необходимо извлечь"""
    """ ПРОБЛЕМА ФУНКЦИЯ ДОЛЖНА ПРИНИМАТЬ В СЕБЯ МАСКУ UTRNNO, PATER, ORGDEV, а также 
    И возвращать контент и индекс нижней гринцы блока"""

    #Ищем индекс патерна в тексте
    index_patern = content.find(str(patern))
    #Ищем индекс первой нижней границы после патерна
    index_down_border = content[index_patern:].find(border)
    #Ищем индекс первой верхней границы перед патерном
    index_up_border = content[index_patern-1::-1].find(border)
    return content[index_patern-index_up_border:index_patern+index_down_border+len(border)-1]

def result_writter(path, files, patern):
    """Функция записи в результирующий файл"""
    with open(Path(path, f'{patern}_logs_report.txt'), 'w', encoding='utf-8') as report:
        for i in files:
            #Чтобы избежать распарсевания системных файлов обработаем окончание
            if i.endswith('out'):
                with open(Path(path, i), 'r', encoding='Latin-1') as file:
                    content = file.read()
                    # Вызываем функцию нарезчика
                    report.write(f'Record from {i}')
                    result, lust_index = cutter(content, patern)
                    report.write(result)
                    report.write(f'END OF FILE {i}')
                    report.write(f'{BORDER}\n\n')
                    print(f"В файл _logs_report.txt в {path} записаны сведения из лога {i}")