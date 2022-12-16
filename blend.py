import subprocess

from os import getcwd, mkdir
from os.path import exists
from unittest import TestCase

from vid import PEXELS
from aud import YouTube
from yt_sync import Sync
from paraphraser import Paraphraser


class Blend:
    def __init__(self, v_attr, path_to_download=getcwd()):
        self.v_attr, self.path_to_download = v_attr, path_to_download

    def stir(self):
        _vid, vid = PEXELS(self.v_attr, path_to_download=getcwd() + f'/vid').download()

        # rephrase
        f_name = Paraphraser(vid['filename']).rephrase() + '.mp4'

        _aud, aud = YouTube(f_name, path_to_download=getcwd() + f'/aud', only_audio=True).download()

        # vid, aud = {}, {}
        # vid['filename'] = 'soft-waves-lapping-on-sandy-shores-2335977.mp4'
        # vid['l_path'] = '/Users/apple/Documents/PycharmProjects/yt_automate/vid/' \
        #                 'l-soft-waves-lapping-on-sandy-shores-2335977.mp4'
        # aud['l_path'] = '/Users/apple/Documents/PycharmProjects/yt_automate/aud/' \
        #                 'l-Water Sounds for Sleep or Focus | White Noise Stream 10 Hours.mp3'

        cmd = f"ffmpeg -i '{vid['l_path']}' -i '{aud['l_path']}' -c:v copy -c:a aac " \
              f"'{self.path_to_download}/{f_name}'"
        subprocess.run(cmd, shell=True)

        sync = Sync()
        f_path = f'{self.path_to_download}/{f_name}'
        sync.upload(f_path, f_name.replace('.mp4', ''), self.v_attr)

        return 'Blended!'


class BlendTest(TestCase):
    def setUp(self):
        path = getcwd() + '/blend'
        if not exists(path):
            mkdir(path)

        self.Blend = Blend('water', path)

    def test_stir(self):
        blend = self.Blend.stir()
        self.assertEqual(blend, 'Blended!')
