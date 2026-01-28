import os
import sys
from pathlib import Path

def _iterfiles(path, size_min_in_mb):
    for root, dirs, files in os.walk(path):
        try:
            for file in files:
                p = Path(os.path.join(root, file))
                try:
                    size = p.stat().st_size
                except PermissionError:
                    size = 0
                if size >= size_min_in_mb:
                    yield size
                else:
                    yield 0
        except PermissionError:
            yield 0

def _iterdirs(path, size_min_in_mb=50):
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
        except PermissionError:
            pass

    return _directory_info

def main(path, size_min_in_mb):
    try:
        folder_info = _iterdirs(path, size_min_in_mb)
        for folder in reversed(list(set(sorted(folder_info.items(), key=lambda x:x[1])))):
            folder_name, size = folder
            if float(size) >= 20.0:
                print('{}: {:.1f}MB'.format(folder_name, size))
    except Exception as Err:
        print("Error: {}".format(Err))


if __name__ == '__main__':
    if len(sys.argv) != 1 and len(sys.argv) != 0:
        main(sys.argv[1], 50)
    else:
        main(input('Search PATH: ') or os.getcwd(), 50)
