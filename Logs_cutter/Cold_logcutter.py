import os
import re
import shutil
import datetime
from pathlib import Path
import subprocess as sub
import tarfile

date_time = datetime.datetime.now()
date = f'{date_time.date()}'

direction = {}
node_id =''
object_type = ''
object_name = ''
u_date = ''
search_modules = ''
search_module = ''
BORDER = ''

search_direction = direction[node_id] #Определяем в какой папке искать по узлу
target_folder = Path(os.getcwd(), f'{u_date}_{object_type}_{object_name}')

def arch_grep(search_direction, search_module, u_date):
    grep = f'ls {search_direction} | grep {search_module} | grep {u_date}'
    data = sub.Popen(grep, shell=True, stdout=sub.PIPE)
    print(f'Выполняется поиск {object_type} {object_name} в файлах модуля {search_module} папки {search_direction}')
    line = str(data.communicate()[0])[2:] #преобразуем из битового в строковый
    full_filenames.extend([file for file in line.split("\\") if len(file) > 10])

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

full_filenames = []
for i in search_modules:
    arch_grep(search_direction, i, u_date)

print(f'Обнаружено {len(full_filenames)} файлов: ', full_filenames)

arch_folder = Path(target_folder, 'archives')
if not os.path.exists(arch_folder):
    os.makedirs(arch_folder, exist_ok=True)
    print(f'Создана папка {arch_folder}')

for i in full_filenames:
    shutil.copy(Path(search_direction, i), Path(arch_folder, i))
    print(f'Файл {i} скопирован в папку {arch_folder}')

out_folder = Path(target_folder, 'out_files', str(object_name))
if not os.path.exists(out_folder):
    os.makedirs(out_folder, exist_ok=True)
    print(f'Создана папка {out_folder}')

for i in full_filenames:
    file = tarfile.open(Path(arch_folder,i))
    print(f'Выполняется разархивирование файла {i} в папку {out_folder}')
    file.extractall(f'{out_folder}')
result_writter(out_folder, os.listdir(out_folder), object_type, str(object_name))
print('Скрипт завершен')
print()