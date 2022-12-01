import subprocess

from abc import ABC
from os import getcwd, mkdir, remove
from os.path import exists
from unittest import TestCase
from youtubesearchpython import VideosSearch
from pytube import YouTube as PyTube
from datetime import datetime

from main import OutBound, Hoop

# TODO:
from pytube.exceptions import LiveStreamError


class YouTube(OutBound, ABC):
    def __init__(self, attr, path_to_download=getcwd(), only_audio=False, resolution='low'):
        self.attr, self.path_to_download, self.only_audio, self.resolution = attr, path_to_download, \
                                                                        only_audio, resolution
        super(YouTube, self).__init__()

    def search(self):
        return VideosSearch(self.attr)

    def finder(self, obj):
        for o in obj:
            filename = o['title'] + '.mp4'
            path = f'{self.path_to_download}/{filename}'
            if not exists(path):
                o['filename'] = filename
                o['filepath'] = path
                return o

    def download(self):
        search = self.search()
        finder = self.finder(search.result()['result'])
        while not finder:
            search.next()
            finder = self.finder(search.result()['result'])

        video = PyTube(finder['link'])
        if self.only_audio:  # To download audio use: only_audio=True
            stream = video.streams.get_audio_only()
        else:  # To download high resolution video use: adaptive=True, file_extension='mp4'
            stream = video.streams.get_highest_resolution() if self.resolution == 'high' else \
                video.streams.get_lowest_resolution()

        stream.download(filename=finder['filename'], output_path=self.path_to_download)
        path = f"{self.path_to_download}/{finder['title']}.mp3"
        if self.only_audio:  # mp3 converter
            cmd = f"ffmpeg -i '{finder['filepath']}' -vn '{path}'"
            subprocess.run(cmd, shell=True)

            remove(finder['filepath'])  # delete .mp4 format

        l_path = f"{self.path_to_download}/l-{finder['title']}.mp3"
        dur = finder['duration']
        dur_c = dur.count(":")
        duration = datetime.strptime(dur, '%H:%M:%S' if dur_c > 1 else '%M:%S')
        Hoop.loop(duration.minute, path, l_path)
        return 'Downloaded!', l_path


class YouTubeTest(TestCase):

    def setUp(self):
        self.path = getcwd() + '/aud'
        if not exists(self.path):
            mkdir(self.path)

        self.search = 'pacha illai song'

    def test_video(self):  # pass resolution='high' for high resolution vidoes
        test, path = YouTube(self.search, path_to_download=self.path).download()
        self.assertEqual(test, 'Downloaded!')

    def test_audio(self):
        test, path = YouTube(self.search, path_to_download=self.path, only_audio=True).download()
        self.assertEqual(test, 'Downloaded!')