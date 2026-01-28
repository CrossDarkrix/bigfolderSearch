import os
import sys
from pathlib import Path
from operator import itemgetter

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
                else:
                    yield 0
        except:
            yield 0

def _iterdirs(path, size_min_in_mb=50):
    _directory = []
    def calc_total(path):
        total = 0
        for size in _iterfiles(path, size_min_in_mb):
            total += size >> 20
        return total
    for root, dirs, files in os.walk(path):
        try:
            for directory in dirs:
                folder = os.path.join(root, directory)
                _directory_info = {}
                _directory_info["folder_name"] = folder
                _directory_info["folder_size"] = calc_total(folder)
                _directory.append(_directory_info)
        except:
            pass

    return _directory

def main(path, size_min_in_mb):
    try:
        folder_info = _iterdirs(path, size_min_in_mb)
        for folder in sorted(folder_info, key=itemgetter('folder_size'), reverse=True):
            folder_name = folder["folder_name"]
            size = folder["folder_size"]
            if float(size) >= 20.0:
                print('{}: {:.1f}MB'.format(folder_name, size))
    except Exception as Err:
        print("Error: {}".format(Err))


if __name__ == '__main__':
    if len(sys.argv) != 1 and len(sys.argv) != 0:
        main(sys.argv[1], 50)
    else:
        path = input('Search PATH: ')
        if path != '':
            main(path, 50)
        else:
            main(os.getcwd(), 50)