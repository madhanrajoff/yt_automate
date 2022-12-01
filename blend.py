# TODO:
# import ffmpeg
# input_video = ffmpeg.input('healthy-man-relaxation-fitness-4327208.mp4')
# input_audio = ffmpeg.input('Love Today - Ennai Vittu Lyric  @Pradeep Ranganathan   Yuvan Shankar Raja  AGS.3gpp')
# ffmpeg.concat(input_video, input_audio, v=1, a=1).output('finished_video.mp4').run()

import ffmpeg
import subprocess

from os import getcwd, mkdir
from os.path import exists
from unittest import TestCase

from vid import PEXELS
from aud import YouTube


class Blend:
    def __init__(self, attr, path_to_download=getcwd()):
        self.attr, self.path_to_download = attr, path_to_download

    def stir(self):
        _vid, v_path = PEXELS(self.attr, path_to_download=getcwd() + f'/vid').download()
        _aud, a_path = YouTube(self.attr, path_to_download=getcwd() + f'/aud', only_audio=True).download()

        cmd = f"ffmpeg -i {v_path} -i {a_path} -c:v copy -c:a aac {self.path_to_download}/output.mp4"
        subprocess.run(cmd, shell=True)

        # vid = ffmpeg.input(v_path)
        # aud = ffmpeg.input(a_path)
        # ffmpeg.concat(vid, aud, v=1, a=1).output(self.path_to_download+'/finished_video.mp4').run()
        return 'Blended!'


class BlendTest(TestCase):
    def setUp(self):
        path = getcwd() + '/blend'
        if not exists(path):
            mkdir(path)

        self.Blend = Blend('water sound', path)

    def test_stir(self):
        blend = self.Blend.stir()
        self.assertEqual(blend, 'Blended!')
