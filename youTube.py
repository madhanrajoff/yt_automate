import datetime
import pickle
import os

from datetime import datetime as dt
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request


class Sync:

    def Create_Service(self, client_secret_file, api_name, api_version, *scopes):
        CLIENT_SECRET_FILE = client_secret_file
        API_SERVICE_NAME = api_name
        API_VERSION = api_version
        SCOPES = [scope for scope in scopes[0]]
        print(SCOPES)

        cred = None

        pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
        # print(pickle_file)

        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as token:
                cred = pickle.load(token)

        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
                cred = flow.run_local_server()

            with open(pickle_file, 'wb') as token:
                pickle.dump(cred, token)

        try:
            service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
            print(API_SERVICE_NAME, 'service created successfully')
            return service
        except Exception as e:
            print('Unable to connect.')
            print(e)
            return None

    # setup_google.py allows user to log into
    def initiate(self):
        CLIENT_SECRET_FILE = 'client_secret.json'
        API_NAME = 'youtube'
        API_VERSION = 'v3'
        SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
        service = self.Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        return service

    def uploadYtvid(self, VIDEO_FILE_NAME='',
                    title='Intro Video!',
                    description=':) ',
                    tags=[],
                    googleAPI=None):
        now = dt.now()
        upload_date_time = dt(now.year, now.month, now.day, now.hour, now.minute,
                                             int(now.second)).isoformat() + '.000Z'

        request_body = {
            'snippet': {
                'categoryId': 23,
                'title': title,
                'description': description,
                'tags': tags
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False,
            },
            'notifySubscribers': False
        }

        mediaFile = MediaFileUpload(VIDEO_FILE_NAME, chunksize=-1, resumable=True)
        googleAPI = self.initiate()
        response_upload = googleAPI.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=mediaFile
        ).execute()

        """
        googleAPI.thumbnails().set(
            videoId=response_upload.get('id'),
            media_body=MediaFileUpload('thumbnail.png')
        ).execute()
        """

        print("Upload Successful!")


if __name__ == "__main__":
    sync = Sync()
    sync.uploadYtvid(VIDEO_FILE_NAME='./aud/Love Today - Pacha Elai Lyric | @Pradeep Ranganathan  | Yuvan Shankar Raja | AGS.mp4')