from pathlib import Path
import os
import shutil
import re

def normalize(filename):
    translit_dict = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
        'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c',
        'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya'
    }
    filename = filename.lower()
    for char in filename:
        if char in translit_dict:
            filename = filename.replace(char, translit_dict[char])
        elif not char.isalpha() and not char.isdigit():
            filename = filename.replace(char, '_')
    return filename

if len(sys.argv) > 1:
    directory = sys.argv[1]
else:
    directory = '.'

def sort_files(directory):
    images_ext = ('JPEG', 'PNG', 'JPG', 'SVG')
    video_ext = ('AVI', 'MP4', 'MOV', 'MKV')
    doc_ext = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
    audio_ext = ('MP3', 'OGG', 'WAV', 'AMR')
    archive_ext = ('ZIP', 'GZ', 'TAR')
    unknown_ext = set()

    # Проверяем каждый файл в папке
    for file_path in Path(directory).glob('**/*.*'):
        # Получаем расширение файла
        ext = file_path.suffix[1:].upper()

        # Если расширение известно, перемещаем файл в соответствующую папку и переименовываем его
        if ext in images_ext:
            dst_dir = 'images'
        elif ext in video_ext:
            dst_dir = 'video'
        elif ext in doc_ext:
            dst_dir = 'documents'
        elif ext in audio_ext:
            dst_dir = 'audio'
        elif ext in archive_ext:
            dst_dir = 'archives'
            # Если файл является архивом, распаковываем его в папку с архивами
            shutil.unpack_archive(str(file_path), str(Path(directory) / dst_dir))
            continue
        else:
            # Если расширение неизвестно, добавляем его в множество неизвестных расширений
            unknown_ext.add(ext)
            continue
           # Удаляем пупку если она пустая
        if not any(os.scandir(file_path)):
            os.rmdir(file_path)

        # Создаем папку, если ее нет
        dst_dir = os.path.join(directory, dst_dir)
        os.makedirs(dst_dir, exist_ok=True)

        # Перемещаем и переименовываем файл
        file_name = normalize(file_path.stem)
        dst_file_path = os.path.join(dst_dir, f'{file_name}{file_path.suffix}')
        shutil.move(str(file_path), dst_file_path)
