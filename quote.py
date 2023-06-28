from collections import UserDict


class Quote(UserDict):

    def __init__(self, tags=None, author=None, quote=None):
        super().__init__()
        self.data["tags"] = tags or []
        self.data["author"] = author
        self.data["quote"] = quote
