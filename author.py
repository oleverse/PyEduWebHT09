import json
from collections import UserDict


class Author(UserDict):

    def __init__(self, fullname=None, born_date=None, born_location=None, description=None):
        super().__init__()
        self.data["fullname"] = fullname
        self.data["born_date"] = born_date
        self.data["born_location"] = born_location
        self.data["description"] = description
