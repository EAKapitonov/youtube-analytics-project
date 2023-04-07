# from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import os

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('youtube_api')

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)


class Vid_error(Exception):
    """
    Класс обработки исключения видео
    """
    pass


class Video:
    """
    Реализуйте инициализацию реальными данными следующих атрибутов экземпляра класса `Video`:
  - id видео
  - название видео
  - ссылка на видео
  - количество просмотров
  - количество лайков
    """

    def __init__(self, video_id):
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()
        try:
            if not video_response['items']:
                raise Vid_error
            else:

                self.video_id = video_id
                self.video_name = video_response["items"][0]["snippet"]["title"]
                self.video_url = f"https://youtu.be/{self.video_id}"
                self.view_count = video_response['items'][0]['statistics']['viewCount']
                self.like_count = video_response['items'][0]['statistics']['likeCount']

        except Vid_error:
            self.video_id = video_id
            self.video_name = None
            self.video_url = None
            self.view_count = None
            self.like_count = None


    def __str__(self):
        return self.video_name


class PLVideo(Video):
    """
    Создайте второй класс для видео `PLVideo`, который инициализируется 'id видео' и 'id плейлиста'
        > Видео может находиться в множестве плейлистов, поэтому непосредственно из видео через API информацию о плейлисте не получить.
         - Реализуйте инициализацию реальными данными следующих атрибутов экземпляра класса `PLVideo`:
         - id видео
         - название видео
         - ссылка на видео
         - количество просмотров
         - количество лайков
         - id плейлиста
    """

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
