import os
import re
import shutil
import datetime
from pathlib import Path
import subprocess as sub
import tarfile

date_time = datetime.datetime.now()
date = f'{date_time.date()}'

direction = {1: 'path'}
patterns = ['utrnno', 'orgdev', 'pattern']
object_type = ''  # input(f'{patterns}: ').lower()
if object_type == 'pattern' or object_type not in patterns:
    object_name = ''  # input(f'{object_type}: ')
    object_type = ''
else:
    object_name = ''  # input(f'{object_type}: ')
all_modules = []
search_modules = ''
node_id = ''
u_date = ''
time = ''
if len(time) < 3:
    time = f'00{time}'
time_interval = '' #int(input))
start_time = int(time[:-2])
end_time = int(time[:-2])+int(time_interval)
BORDER = ''

search_direction = direction[node_id] #Определяем в какой папке искать по узлу
target_folder = Path(os.getcwd(), f'{object_name}')

def arch_grep(search_direction, search_module, u_date, start_time, end_time):
    grep = f'ls {search_direction} | grep {search_module} | grep {u_date}'
    data = sub.Popen(grep, shell=True, stdout=sub.PIPE)
    line = str(data.communicate()[0])[2:] #преобразуем из битового в строковый
    filenames = [file for file in line.split("\\") if len(file) > 10]
    full_filenames.extend([file for file in filenames if (start_time <= int(file.split('.')[1].cplit('_') <= end_time))])

def cutter(content, index_patern, border = BORDER):
    """Центральная функция определяющая блок лога, который необходимо извлечь"""
    #Ищем индекс первой нижней границы после патерна
    index_down_border = content[index_patern:].find(border)
    #Ищем индекс первой верхней границы перед патерном
    index_up_border = content[index_patern-1::-1].find(border)
    return content[index_patern-index_up_border:index_patern+index_down_border+len(border)-1]

def result_writter(path, target_folder, files, object_type, object_name):
    """Функция принимает в себя путь до файла, наименование файла в нем,
     а также паттерн для поиска и записывает в результирующий файл"""
    report_name = f'{object_type}:{object_name}_logs_report.txt'
    with open(Path(path,report_name), 'w', encoding='utf-8') as report:
        for f in files:
            #Чтобы избежать распарсевания системных файлов обработаем окончание
            if len(i) > 10:
                with open(Path(target_folder, f), 'r', encoding='Latin-1') as file:
                    content = file.read()
                    # Вызываем функцию нарезчика
                    report.write(f'Record from {f}')
                    if object_type == ' ':
                        indexes = [t.start(0) for t in re.finditer(f'{object_name}', content)] # Ищем и сохраняем все индексы вхождения патерна в текстовый файл
                    else:
                        indexes = [t.start(0) for t in re.finditer(f'{object_type}:.*{object_name}',content)]
                    print(f'В файле {f} обнаружено {len(indexes)} вхождений')
                    for index in indexes:
                        result = cutter(content, index)
                        report.write(result)
                    report.write(f'END OF FILE {i}')
                    report.write(f'{BORDER}\n\n')
                    print(f"В файл {Path(path, report_name)} записаны сведения из лога {i}")

full_filenames = []
for i in search_modules:
    arch_grep(search_direction, i, u_date, start_time, end_time)

print(f'Обнаружено {len(full_filenames)} файлов: ', *full_filenames)

if not os.path.exists(target_folder):
    os.makedirs(target_folder, exist_ok=True)
    print(f'Создана папка {target_folder}')


for i in full_filenames:
    file = tarfile.open(Path(search_direction,i))
    print(f'Выполняется разархивирование файла {i} в папку {target_folder}')
    file.extractall(f'{target_folder}')

"""
БЛОК УДАЛЕНИЯ ЛИШНИХ ФАЙЛОВ
"""

result_writter(Path.cwd(), target_folder, os.listdir(target_folder), object_type, str(object_name))
print('Скрипт завершен')
print()
