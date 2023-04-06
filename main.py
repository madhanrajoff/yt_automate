import abc
import subprocess

from os import getcwd, mkdir, remove, listdir
from os.path import exists, isfile, isdir


class Assistance:
    pass


class OutBound(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'search') and
                callable(subclass.search) and
                hasattr(subclass, 'download') and
                callable(subclass.download) or
                NotImplemented)

    @abc.abstractmethod
    def search(self):
        raise NotImplementedError

    @abc.abstractmethod
    def download(self):
        raise NotImplementedError


class Hooper:
    @classmethod
    def loop(cls, duration, path, l_path):
        cmd = ''
        dur, start, end = 900, '00:00:00', '00:15:00'  # 15 MIN MAX

        if duration < dur:
            cmd += f"ffmpeg -stream_loop -1 -i '{path}' -c copy -t 900 '{l_path}'"
        else:
            cmd += f"ffmpeg -i '{path}' -ss {start} -t {end} -c:v copy -c:a copy '{l_path}'"

        if cmd:
            subprocess.run(cmd, shell=True)


class FileHandler:
    @staticmethod
    def mkdir(*dir_names):
        for dir_name in dir_names:
            path = f'{getcwd()}/{dir_name}'
            if not exists(path):
                mkdir(path)

    @staticmethod
    def delete(path):
        try:
            if isfile(path):
                remove(path)
            elif isdir(path):
                l_dir = listdir(path)
                for p in l_dir:
                    remove(p)
        except OSError as error:
            print(f"File path can not be removed, for detailed info - {error}")
