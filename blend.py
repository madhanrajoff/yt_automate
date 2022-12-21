import subprocess

from os import getcwd
from unittest import TestCase

from vid import PEXELS
from aud import YouTube
from yt_sync import Sync
from paraphraser import Paraphraser
from main import Mkdir


class Blend:
    def __init__(self, v_attr, specific_aud, path_to_download=None):
        self.v_attr, self.specific_aud = v_attr, specific_aud

        self.path_to_download = path_to_download if path_to_download else Mkdir.create('blend')

    def stir(self):
        _vid, vid = PEXELS(self.v_attr, path_to_download=getcwd() + f'/vid').download()

        # rephrase
        f_name = Paraphraser(vid['filename']).rephrase()
        f_name_with_ext = f_name + '.mp4'

        # To download any specific audio pass title as specific argument
        _aud, aud = YouTube(f_name + ' music', path_to_download=getcwd() + f'/aud', only_audio=True,
                            specific=self.specific_aud).download()

        # vid, aud = {}, {}
        # f_name = 'motorboat travelling on a body of water'
        # f_name_with_ext = 'motorboat travelling on a body of water.mp4'
        # vid['l_path'] = '/Users/apple/Documents/PycharmProjects/yt_automate/vid/l-motorboat-traveling-across-a-body-of-water-2711213.mp4'
        # aud['l_path'] = '/Users/apple/Documents/PycharmProjects/yt_automate/aud/l-Boat No Copyright Videos With No Copyright Music - Stock Footage - FreeCinematics.mp3'

        cmd = f"ffmpeg -i '{vid['l_path']}' -i '{aud['l_path']}' -c:v copy -c:a aac " \
              f"'{self.path_to_download}/{f_name_with_ext}'"
        subprocess.run(cmd, shell=True)

        sync = Sync()
        f_path = f'{self.path_to_download}/{f_name_with_ext}'
        print('video', vid['l_path'])
        print('audio', aud['l_path'])
        print('blend', f_path)
        sync.upload(f_path, f_name, self.v_attr)

        return 'Blended!'


class BlendTest(TestCase):
    def setUp(self):
        self.Blend = Blend('water', 'water music')

    def test_stir(self):
        blend = self.Blend.stir()
        self.assertEqual(blend, 'Blended!')
