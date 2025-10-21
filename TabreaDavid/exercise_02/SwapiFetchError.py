class SwapiFetchError(Exception):
    def __init__(self, url: str, message: str, status_code: int | None = None):
        super().__init__(message)
        self.url = url
        self.message = message
        self.status_code = status_code

    def as_dict(self) -> dict:
        return {
            "url": self.url,
            "message": self.message,
            "status_code": self.status_code,
        }