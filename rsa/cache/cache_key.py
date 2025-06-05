
class CacheKey:

    def __init__(self, separator='__-__'):

        self.separator = separator

    def join(self, x, y):
        pair = sorted([x, y])
        key = self.separator.join(pair)
        return key

    def split(self, key):
        x, y = key.split(self.separator)
        return x, y