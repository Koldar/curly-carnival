from typing import Any


class MigrationContext(object):

    def __init__(self):
        self.d = {}

    def __getattr__(self, item: str) -> Any:
        return self.d[item]

    def __setattr__(self, key: str, value: Any):
        self.d[key] = value

    def __contains__(self, item):
        return item in self.d

    def __len__(self) -> int:
        return len(self.d)
