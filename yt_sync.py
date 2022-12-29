import pickle
import os
import sys

from datetime import datetime as dt
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

from paraphraser import Paraphraser


class Sync:

    def __init__(self):
        self.client_secret_file = 'web_client_secrets.json'
        self.api_name = 'youtube'
        self.api_version = 'v3'
        self.scopes = ['https://www.googleapis.com/auth/youtube.upload']

        self.default = {
            'des': 'Watching this video and listening to the water drips can help you unwind.',
            'tags': ['meditationmusic', 'meditation', 'relaxingmusic', 'yogamusic', 'relax', 'sleepmusic',
                     'calmmusic', 'healingmusic', 'nature', 'relaxation', 'mindfulness', 'soundhealing']}

    def service(self):
        cred = None
        pickle_file = f'token_{self.api_name}_{self.api_version}.pickle'

        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as token:
                cred = pickle.load(token)

        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.client_secret_file, self.scopes)
                cred = flow.run_local_server()

            with open(pickle_file, 'wb') as token:
                pickle.dump(cred, token)

        try:
            service = build(self.api_name, self.api_version, credentials=cred)
            print(self.api_name, 'service created successfully')
            return service
        except Exception as e:
            print('Unable to connect.')
            print(e)
            return None

    def upload(self, file_p='', file_n=''):
        now = dt.now()
        upload_date_time = dt(now.year, now.month, now.day, now.hour, now.minute,
                              int(now.second)).isoformat() + '.000Z'

        request_body = {
            'snippet': {
                'categoryId': 23,
                'title': file_n,
                'description': self.default['des'],
                'tags': self.default['tags']
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False,
            },
            'notifySubscribers': False
        }

        media_file = MediaFileUpload(file_p, chunksize=-1, resumable=True)
        g_api = self.service()
        # response_upload = g_api.videos().insert(
        #     part='snippet,status',
        #     body=request_body,
        #     media_body=media_file
        # ).execute()

        """
        g_api.thumbnails().set(
            videoId=response_upload.get('id'),
            media_body=MediaFileUpload('thumbnail.png')
        ).execute()
        """

        return "Upload Successful!"


if __name__ == "__main__":
    arg = sys.argv
    sync = Sync()
    f_name = 'landscape-nature-sunset-man-4441007.mp4'
    f_path = os.getcwd() + f'/blend/{f_name}'
    upload_name = Paraphraser(phrase=f_name).rephrase()
    sync.upload(f_path, upload_name)
    # sync.upload(arg[0], arg[1])
