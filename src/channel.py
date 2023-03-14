import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

import isodate

# YT_API_KEY скопирован из гугла и вставлен в переменные окружения
api_key: str = os.getenv('youtube_api')

# создать специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self._channel_id = channel_id
        self.title = channel["items"][0]["snippet"]["title"]
        self.description = channel["items"][0]["snippet"]["description"]
        self.url = f"https://www.youtube.com/channel/{channel_id}"
        self.subscriberCount = channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = channel["items"][0]["statistics"]["videoCount"]
        self.viewCount = channel["items"][0]["statistics"]["viewCount"]

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @property
    def channel_id(self):
        """ чтобы id нельзя было поменять из вне"""
        return self._channel_id

    @classmethod
    def get_service():
        """ получить объект для работы с API вне класса"""
        import src
        return src.channel.youtube


    def to_json(self, name: str):
        """создаем файл 'file' c данными по каналу"""
        with open(f"{name}", 'w+') as outfile:
            channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
            json.dump(channel, outfile)


