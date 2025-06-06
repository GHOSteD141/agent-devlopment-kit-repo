class State(dict):
    def __init__(self):
        super().__init__()

    def set(self, key: str, value: any):
        self[key] = value

    def get(self, key: str) -> any:
        return super().get(key, None)

    def remove(self, key: str):
        if key in self:
            del self[key]

    def clear(self):
        super().clear()

    def exists(self, key: str) -> bool:
        return key in self

    def update(self, updates: dict):
        super().update(updates)

    def __repr__(self):
        return f'State({dict(self)})'