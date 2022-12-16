import requests

from abc import ABC
from os import getcwd, mkdir
from os.path import exists
from unittest import TestCase

from main import OutBound, Hoop
from mapper import Mapper


class PEXELS(OutBound, ABC):
    from pexelsapi.pexels import Pexels

    API_KEY = "563492ad6f917000010000016276cad7b7e145bbb5344f4080dcb7a5"
    PEXELS = Pexels(API_KEY)

    def __init__(self, attr, path_to_download=getcwd()):
        self.attr, self.path_to_download = attr, path_to_download
        super(PEXELS, self).__init__()

    def search(self):
        return self.PEXELS.search_videos

    def finder(self, obj, thr_db=False):
        find = False
        for o in obj:
            filename = o['url'].split('/')[-2] + '.mp4'
            path = f'{self.path_to_download}/{filename}'
            if thr_db:
                mapper = Mapper()
                q_res = mapper.get('video', filename)
                print('video q_res - ', q_res)
                if not q_res:
                    mapper.insert('video', filename)
                    find = True
            else:
                if not exists(path):
                    find = True

            if find:
                o['filename'] = filename
                o['filepath'] = path
                return o

    def download(self):
        page = 1
        per_page = 80  # MAX
        search = self.search()
        search_videos = search(self.attr, page=page, per_page=per_page)
        finder = self.finder(search_videos['videos'], thr_db=True)

        while not finder:
            page += 1
            search_videos = search(self.attr, page=page, per_page=per_page)
            finder = self.finder(search_videos['videos'], thr_db=True)

        path = f"{self.path_to_download}/{finder['filename']}"
        url_video = 'https://www.pexels.com/video/' + str(finder['id']) + '/download'
        r = requests.get(url_video)
        with open(path, 'wb') as outfile:
            outfile.write(r.content)

        l_path = f"{self.path_to_download}/{'l-' + finder['filename']}"
        Hoop.loop(finder['duration'], path, l_path)

        finder['path'], finder['l_path'] = path, l_path
        return 'Downloaded!', finder


class PEXELSTest(TestCase):

    def setUp(self):
        path = getcwd() + '/vid'
        if not exists(path):
            mkdir(path)

        self.PEXELS = PEXELS('meditation', path)

    def test(self):
        test, _ = self.PEXELS.download()
        self.assertEqual(test, 'Downloaded!')
