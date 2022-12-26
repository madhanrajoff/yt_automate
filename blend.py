import subprocess

from os import getcwd
from unittest import TestCase

from vid import PEXELS
from aud import YouTube
from yt_sync import Sync
from paraphraser import Paraphraser
from main import FileHandler


class Blend:
    def __init__(self, v_attr, path_to_download=None, thr_db=False):
        self.v_attr = v_attr
        self.thr_db = thr_db
        self.path_to_download = path_to_download if path_to_download else FileHandler.mkdir('blend')

    def create_vid(self):
        _vid, vid = PEXELS(self.v_attr, path_to_download=getcwd() + f'/vid').download()
        return vid['filename'], vid['l_path']

    @staticmethod
    def create_aud(vid_title, specific=''):
        # To download any specific audio pass title as specific argument
        _aud, aud = YouTube(vid_title + 'music', path_to_download=getcwd() + f'/aud',
                            only_audio=True, specific=specific).download()
        return aud['l_path']

    def stir(self, **f):  # f - file arguments, create vid and aud files if create one_exists in f
        if f.get('create_one'):
            f['v_name'], f['v_p'] = self.create_vid()
            # To download any specific audio pass title as specific argument
            f['a_p'] = self.create_aud(f['v_name'] + 'music')

        print(f['v_p'])
        print(f['a_p'])
        cmd = f"ffmpeg -i '{f['v_p']}' -i '{f['a_p']}' -c:v copy -c:a aac " \
              f"'{self.path_to_download}/{f['v_name']}'"
        print(cmd)
        subprocess.run(cmd, shell=True)

        sync = Sync()
        f_path = f"{self.path_to_download}/{f['v_name']}"
        # sync.upload(f_path, Paraphraser(f['v_name']).rephrase())
        return 'Blended!'


class BlendTest(TestCase):
    def setUp(self):
        self.Blend = Blend('water', thr_db=True)

    def test_stir(self):
        blend = self.Blend.stir(create_one=True)
        self.assertEqual(blend, 'Blended!')

        # to delete the uploaded files
        dir_name = ['audio', 'video', 'blend']
        for dir_ in dir_name:
            FileHandler.delete(f'{getcwd()}/{dir_}')
