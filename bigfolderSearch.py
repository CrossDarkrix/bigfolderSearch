import os
from pathlib import Path

def _iterfiles(path, size_min_in_mb):
    for root, dirs, files in os.walk(path):
        try:
            for file in files:
                p = Path(os.path.join(root, file))
                try:
                    size = p.stat().st_size
                except:
                    size = 0
                if size >= size_min_in_mb:
                    yield size
        except:
            yield 0

def _iterdirs(path, size_min_in_mb):
    _directory_info = {}
    def calc_total(path):
        total = 0
        for size in _iterfiles(path, size_min_in_mb):
            total += size >> 20
        return total
    for root, dirs, files in os.walk(path):
        try:
            for directory in dirs:
                folder = os.path.join(root, directory)
                _directory_info[folder] = calc_total(folder)
        except:
            pass

    return _directory_info

def main(path, size_min_in_mb):
    try:
        folder_info = _iterdirs(path, size_min_in_mb)
        for folder in reversed(sorted(folder_info.items(), key=lambda x:x[1])):
            folder_name, size = folder
            if float(size) >= 20.0:
                print('{}: {:.1f}MB'.format(folder_name, size))
    except:
        print("Error")

main(os.getcwd(), 50)
