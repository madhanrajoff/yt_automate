import subprocess

from abc import ABC
from os import remove
from os.path import exists
from unittest import TestCase
from youtubesearchpython import VideosSearch
from pytube import YouTube as PyTube
from datetime import datetime
from pprint import pprint as pp

from main import OutBound, Hoop, Mkdir
from mapper import Mapper

# TODO:
from pytube.exceptions import LiveStreamError


class YouTube(OutBound, ABC):
    def __init__(self, attr, path_to_download=None, only_audio=False, resolution='low', thr_db=False, specific=''):
        self.attr, self.path_to_download = attr, path_to_download
        self.only_audio, self.resolution = only_audio, resolution

        self.thr_db = thr_db
        self.view_count, self.specific = 1, specific

        self.path_to_download = path_to_download if path_to_download else Mkdir.create('aud')

        super(YouTube, self).__init__()


    def search(self):
        attr = self.attr if not self.specific else self.specific
        return VideosSearch(attr)

    def finder(self, obj):
        find = False
        for o in obj:
            filename = o['title'] + '.mp4'
            c_filename = filename.replace('.mp4', '.mp3')
            path = f'{self.path_to_download}/{filename}'
            if self.thr_db:
                mapper = Mapper()
                q_res = mapper.get('audio', c_filename)
                print('audio q_res - ', q_res)
                if not q_res:
                    mapper.insert('audio', c_filename)
                    find = True
            else:
                if not exists(path.replace('.mp4', '.mp3')):  # to check converted .mp3 file
                    find = True

            if find:
                video = PyTube(o['link'])
                if video.views > self.view_count:
                    o['filename'] = filename
                    o['filepath'] = path
                    o['video_stream'] = video
                    return o

    def download(self):
        search = self.search()
        finder = self.finder(search.result()['result'])
        while not finder:
            search.next()
            finder = self.finder(search.result()['result'])

        video = finder['video_stream']
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

        finder['path'], finder['l_path'] = path, l_path
        return 'Downloaded!', finder


class YouTubeTest(TestCase):

    def setUp(self):
        self.search = 'Motorboat Traveling Across A Body Of Water music'

    def test_video(self):  # pass resolution='high' for high resolution vidoes
        test, _ = YouTube(self.search).download()
        self.assertEqual(test, 'Downloaded!')

    def test_audio(self):
        test, _ = YouTube(self.search, only_audio=True).download()
        self.assertEqual(test, 'Downloaded!')
