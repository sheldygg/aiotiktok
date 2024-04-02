class UrlUnavailable(Exception):
    def __init__(self, url: str):
        super().__init__(f"URL {url} is unavailable")


class VideoUnavailable(Exception):
    def __init__(self, video_id: str):
        super().__init__(f"Video {video_id} is unavailable")
