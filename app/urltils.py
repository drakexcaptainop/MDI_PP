class PartialUrl():
    def __init__(self, url):
        self.url: str = url
    
    def query(self):
        self.url.split('?')
        
        