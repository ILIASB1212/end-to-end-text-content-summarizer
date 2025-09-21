from typing import Any, List, Dict
from langchain.document_loaders.base import BaseLoader
from langchain.schema import Document
from langchain_community.document_loaders.youtube import _parse_video_id

class YoutubeLoaderDL(BaseLoader):
    def __init__(
        self,
        video_id: str,
        add_video_info: bool = False,
        
    ):
        """Initialize with YouTube video ID."""
        self.video_id = video_id
        self._metadata = {"source": video_id}
        self.add_video_info = add_video_info


    @staticmethod
    def extract_video_id(youtube_url: str) -> str:
        """Extract video ID from common YouTube URLs."""
        video_id = _parse_video_id(youtube_url)
        if not video_id:
            raise ValueError(
                f'Could not determine the video ID for the URL "{youtube_url}".'
            )
        return video_id
    
    @classmethod
    def from_youtube_url(cls, youtube_url: str, **kwargs: Any) -> "YoutubeLoaderDL":
        """Given a YouTube URL, construct a loader.
        See `YoutubeLoader()` constructor for a list of keyword arguments.
        """
        video_id = cls.extract_video_id(youtube_url)
        return cls(video_id, **kwargs)

    def load(self) -> List[Document]:
        """Load YouTube transcripts into 'Document' objects."""
        
        if self.add_video_info:
            video_info = self._get_video_info()
            self._metadata.update(video_info)
        
        return [Document(page_content=" ",metadata=self._metadata)]
            
    def _get_video_info(self) -> Dict:
        """Get important video information.

        Components include:
            - title
            - description
            - thumbnail URL,
            - publish_date
            - channel author
            - and more.
        """
        try:
            from yt_dlp import YoutubeDL

        except ImportError:
            raise ImportError(
                'Could not import "yt_dlp" Python package. '
                "Please install it with `pip install yt_dlp`."
            )
        
        ydl_opts = {"quiet": True, "no_warnings": True, "skip_download": True}
        with YoutubeDL(ydl_opts) as ydl:
            yt = ydl.extract_info(
                f"https://www.youtube.com/watch?v={self.video_id}", download=False
            )
            publish_date = yt.get("upload_date")
            if publish_date:
                try:
                    from datetime import datetime

                    date_obj = datetime.strptime(publish_date, "%Y%m%d")
                    publish_date = date_obj.strftime("%Y-%m-%d")
                except (ValueError, TypeError):
                    publish_date = "Unknown"
        video_info = {
            "title": yt.get("title", "Unknown"),
            "description": yt.get("description", "Unknown"),
            "view_count": yt.get("view_count", 0),
            "publish_date": publish_date,
            "length": yt.get("duration", 0),
            "author": yt.get("uploader", "Unknown"),
            "channel_id": yt.get("channel_id", "Unknown"),
            "webpage_url": yt.get("webpage_url", "Unknown"),
        }
        return video_info