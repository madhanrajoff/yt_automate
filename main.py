import abc
import subprocess

from os import getcwd, mkdir
from os.path import exists


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


class Hoop:
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


class Mkdir:
    @staticmethod
    def create(dir_name):
        path = f'{getcwd()}/{dir_name}'
        if not exists(path):
            mkdir(path)
        return path
