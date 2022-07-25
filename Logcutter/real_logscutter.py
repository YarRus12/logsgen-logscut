#! usr/bin/python

"""Необходимо доделатьЖ
    1. Рекурсивное обращение к функции cutter в функции writter для поиска всех вхождений в текст лога
    2. Обработка отсутствия результатов поиска в папке
    3. Реализация поиска холодных логов в архивах
    """

"""Вводный блок"""

import os
import shutil
import datetime
from pathlib import Path
import subprocess as sub
date_time = datetime.datetime.now()
date = f'{date_time.date()}'
#Задаем путь до папки с лог файлами
src_folder = Path('../..', '..')
#Задаем путь и имя до конечной папки, куда будет выведен результат и копии лог-файлов
target_folder = Path('../..', '..')
patterns = ['utrnno', 'orgdev', 'pattern']
module = ['nwint','time', 'ALL']#Все модули, которые могут быть исследованы
object_type = input(f'По какому критерию будет осуществляться поиск логов? {patterns}')
object_name = int(input(f'Введите номер {object_type}'))
seach_models = input(f'Логи каких модулей необходимо расспарсить {module}').lower().split()
BORDER = '*************************************************************************************\n'


def grep(src_folder:str, object_name:str, module: str) -> list:
    """Функция выполняет команду grep в указанной папке и
    возвращает список полных имен файлов, в которых найдено вхождение патерна"""
    if module == 'ALL':
        module_name = ''
    else: module_name = module
    args = [f'grep -l {object_name} {src_folder}/{module_name}*']
    print(f'args = {args}')
    data = sub.Popen(args, shell=True, stdout=sub.PIPE)
    print(f'Выполняется поиск {object_name} в файлах модуля {module_name} папки {src_folder}')
    line = str(data.communicate()[0][2:])# преобразуем из битового в строковый
    full_filesnames = [file for file in line.split("\\n") if len(file) > len(src_folder)]
    print(f'Выборка составила {len(full_filesnames)}')
    return full_filesnames

def logs_copy(src_folder: str, target_folder: str, full_filesnames: list) -> list:
    """Функция проверяет расширение файлов с логами, приводит в читаемый формат
    И выполняет копирование в указанную папку"""
    #Создаем папку для копий файлов
    if not os.path.exists(target_folder):
        os.makedirs(target_folder, exist_ok=True)
        print(f'Создана папка {target_folder}')
    # У некоторых файлов нестандартное (цифровое) окончание наименования,
    # поэтому для корректной работы необходимо перенести цифровую часть имени файла
    # и чтобы не перебирать список два раза результирующие файлы копируем в новую папку
    end_of_file_name = []
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

def result_writter(path, files, object_type, object_name):
    """Функция записи в результирующий файл"""
    with open(Path(path, f'{object_type}_{object_name}_logs_report.txt'), 'w', encoding='utf-8') as report:
        for i in files:
            #Чтобы избежать распарсевания системных файлов обработаем окончание
            if i.endswith('out'):
                with open(Path(path, i), 'r', encoding='Latin-1') as file:
                    content = file.read()
                    # Вызываем функцию нарезчика
                    report.write(f'Record from {i}')
                    result, lust_index = cutter(content, object_type, object_name)
                    report.write(result)
                    report.write(f'END OF FILE {i}')
                    report.write(f'{BORDER}\n\n')
                    print(f"В файл _logs_report.txt в {path} записаны сведения из лога {i}")

full_filesnames = []
for i in len(module):
    full_filesnames.extend(grep(src_folder, str(object_name), i))
end_of_file_name = logs_copy(src_folder, target_folder, full_filesnames)
result_writter(target_folder, end_of_file_name, object_type, object_name)