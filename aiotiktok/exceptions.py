class UrlUnavailable(Exception):
    def __init__(self, url: str):
        super().__init__(f"URL {url} is unavailable")