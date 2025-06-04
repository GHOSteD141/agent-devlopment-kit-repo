class State:
    def __init__(self):
        self.data = {}
    
    def set(self, key: str, value: any):
        self.data[key] = value
    
    def get(self, key: str) -> any:
        return self.data.get(key, None)
    
    def remove(self, key: str):
        if key in self.data:
            del self.data[key]
    
    def clear(self):
        self.data.clear()
    
    def exists(self, key: str) -> bool:
        return key in self.data

    def update(self, updates: dict):
        self.data.update(updates)

    def __repr__(self):
        return f'State({self.data})'