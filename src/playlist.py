from src.video import Video
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

import isodate

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('youtube_api')

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    """
    - Реализуйте класс `PlayList`, который инициализируется _id_ плейлиста и имеет следующие публичные атрибуты:
  - название плейлиста
  - ссылку на плейлист
    """

    def __init__(self, id_playlist):
        self.id = id_playlist
        self.playlist_videos = youtube.playlistItems().list(playlistId=self.id,
                                                            part='contentDetails,snippet',
                                                            maxResults=50,
                                                            ).execute()
        self.url = "https://www.youtube.com/playlist?list=" + self.id
        playlists = playlist_videos = youtube.playlists().list(id=id_playlist,
                                           part='snippet',
                                           maxResults=50,
                                           ).execute()
        self.title = playlists['items'][0]["snippet"]["title"]

    @property
    def total_duration(self):
        """
        total_duration` возвращает объект класса `datetime.timedelta` с суммарной длительность плейлиста
        (обращение как к свойству, использовать `@property`)
        """
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        x = isodate.parse_duration("PT00M00S")
        for duration in video_response['items']:
            x = x + isodate.parse_duration(duration['contentDetails']['duration'])
        return x

    def show_best_video(self):
        """
        Show_best_video()` возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        best_video_id = ""
        best_video_like_count = 0
        for video in video_ids:
            vid = Video(video)
            if int(vid.like_count) >= best_video_like_count:
                best_video_id = vid.video_id
        best_video = Video(best_video_id)
        return best_video.video_url


