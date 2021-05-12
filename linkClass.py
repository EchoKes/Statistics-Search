class Link:
    def __init__(self, link, num):
        self.link = link
        self.num = num

    def serialize(self):
        return {
            "link" : self.link,
            "num" : self.num,
        }