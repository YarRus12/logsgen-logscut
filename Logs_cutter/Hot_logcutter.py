#! usr/bin/python

"""Вводный блок"""

import os
import shutil
import datetime
from pathlib import Path
import subprocess as sub
date_time = datetime.datetime.now()
date = f'{date_time.date()}'
patterns = ['utrnno','orgdev', 'hpan', 'pattern']
all_modules = ['nwint', 'txrout', 'acqint', 'crout', 'all'] #Все модули, которые могут быть исследованы
object_type = input(f'По какому критерию будет осуществляться поиск логов? {patterns}').lower()
if object_type == 'pattern' or object_type not in patterns:
    object_name = int(input(f'Введите искомый {object_type}'))
    object_type = ' '
else:
    object_name = int(input(f'Введите номер {object_type}'))

search_modules = ''
src_folder = Path('../..', '..') #Задаем путь до папки с лог файлами
target_folder = Path(os.getcwd(), f'{date}_{object_type}_{object_name}') #Целевая подпапка в текущей директории
BORDER = '*************************************************************************************\n'


"""Функциональный блок"""

def grep(src_folder:str, object_type:str, object_name:str, module: str):
    """Функция выполняет команду grep в указанной папке и добавляет имена в итоговый список"""
    if module == 'all' or module not in all_modules:
        module_name = ''
    else: module_name = module
    grep = [f'/usr/xpg4/bin/grep -E -l {object_type}.*{object_name} {src_folder}{module_name}']
    data = sub.Popen(grep, shell=True, stdout=sub.PIPE)
    print(f'Выполняется поиск {object_type} {object_name} в файлах модуля {module_name} папки {src_folder}')
    line = str(data.communicate()[0])[2:] #преобразуем из битового в строковый
    full_filesnames = [file for file in line.split('\\') if len(file) > 2]
    print(f'Выборка составила {len(full_filesnames)} файлов(-а)')
    return full_filesnames

def logs_copy(src_folder:str, target_folder:str, full_filesnames: list) -> list:
    """Функция проверяет рпсширения файлов с логами, приводит их в читаемый форма
    и выполняет копирование в указанную директорию"""
    if not os.path.exists(target_folder):
        os.makedirs(target_folder, exist_ok=True)
        print(f'Создана папка {target_folder}')
    end_of_file_name = []
    #У некоторых файлов нестандартное (цифровое) окончание наименования,
    # поэтому для корректной работы необходимо перенести цифровую часть имени файла
    # и чтобы не перебирать список два раза результирующие файлы копируем в новую папку
    for i in full_filesnames:
        if len(i.split('.')) > 2:
            target_file = Path(target_folder, '.'.join((i.split('/')[-1].split('.')[:2])))
            src_file = Path(src_folder, i.split('/')[-1])
            shutil.copy(src_file, target_file)
            end_of_file_name.append('.'.join((i.split('/')[-1].split('.')[:2])))
        else:
            target_file = Path(target_folder, i.split('/')[-1])
            src_file = Path(src_folder, i.split('/')[-1])
            shutil.copy(src_file, target_file)
            end_of_file_name.append(i.split('/')[-1])
    print(f'Файлы скопированы в папку {target_folder}')
    return end_of_file_name


def cutter(content, index_patern, border = BORDER):
    """Центральная функция определяющая блок лога, который необходимо извлечь"""
    #Ищем индекс первой нижней границы после патерна
    index_down_border = content[index_patern:].find(border)
    #Ищем индекс первой верхней границы перед патерном
    index_up_border = content[index_patern-1::-1].find(border)
    return content[index_patern-index_up_border:index_patern+index_down_border+len(border)-1]

def result_writter(path, files, object_type, object_name):
    """Функция принимает в себя путь до файла, наименование файла в нем,
     а также паттерн для поиска и записывает в результирующий файл"""
    with open(Path(path, f'{object_type}:{object_name}_logs_report.txt'), 'w', encoding='utf-8') as report:
        for i in files:
            #Чтобы избежать распарсевания системных файлов обработаем окончание
            if len(i) > 10:
                with open(Path(path, i), 'r', encoding='Latin-1') as file:
                    content = file.read()
                    # Вызываем функцию нарезчика
                    report.write(f'Record from {i}')
                    if object_type == ' ':
                        indexes = [t.start(0) for t in re.finditer(f'{object_name}', content)] # Ищем и сохраняем все индексы вхождения патерна в текстовый файл
                    else:
                        indexes = [t.start(0) for t in re.finditer(f'{object_type}:.*{object_name}',content)]
                    for index in indexes:
                        result = cutter(content, index)
                    report.write(result)
                    report.write(f'END OF FILE {i}')
                    report.write(f'{BORDER}\n\n')
                    print(f"В файл _logs_report.txt в {path} записаны сведения из лога {i}")

full_filesnames = []
for i in search_modules:
    if object_type == '':
        full_filesnames.extend(grep(src_folder, object_type, str(object_name), i))
    else:
        full_filesnames.extend(grep(src_folder, object_type+':', str(object_name), i))
if len(full_filesnames) == 0:
    exit(f'В папке {src_folder} ахождений {object_name} не обнаружено')
end_of_file_name = logs_copy(src_folder, target_folder, full_filesnames)
result_writter(target_folder, os.listdir(target_folder), object_type, object_name)