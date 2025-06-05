import yaml
from rsa.cache.cache_key import CacheKey


class RDMCache:

    def __init__(self):
        self.cache_dict = {}
        self.key_handler = CacheKey()

    def load_from_file(self, fp_cache):
        with open(fp_cache, 'r') as h:
            data = yaml.safe_load(h)

            version = data.get('version', None)

            if version is None:
                self.cache_dict = data

            elif version == 250605:

                if 'cache' in data and 'flist' in data:
                    flist = data['flist']
                    cache_dict_mapped = data['cache']
                    separator = data.get('separator', self.key_handler.separator)
                    # update separator
                    self.key_handler.separator = separator
                    for k, v in data['cache'].items():
                        xi, yi = self.key_handler.split(k)
                        x = flist[int(xi)]
                        y = flist[int(yi)]
                        k_new = self.key_handler.join(x, y)
                        self.cache_dict[k_new] = v
                else:
                    raise KeyError("Cache file does not contain 'cache' or 'flist' keys.")

    def save_to_file(self, fp_dst):
        with open(fp_dst, 'w') as h:

            keys = list(self.cache_dict.keys())
            flist = set()
            for k in keys:
                x, y = self.key_handler.split(k)
                flist.add(x)
                flist.add(y)
            flist = sorted(list(flist))
            self.cache_dict['flist'] = flist

            cache_dict_mapped = {}
            for k, v in self.cache_dict.items():
                x, y = self.key_handler.split(k)
                xi = flist.index(x)
                yi = flist.index(y)
                k_new = self.key_handler.join(xi, yi)
                cache_dict_mapped[k_new] = v

            h.write(yaml.dump({
                'version': 250605,  # Add version information
                'cache': cache_dict_mapped,
                'flist': list(flist),
                'separator': self.key_handler.separator
            }))

    # def is_in(self, x, y):
    #
    #     key = self._get_key(x, y)
    #     return key in self.cache_dict

    def add(self, x, y, value):
        key = self.key_handler.join(x, y)
        self.cache_dict[key] = value

    def get(self, x, y, default_value):
        """
        Retrieves a cached value for a pair of elements.

        Args:
            x (str): First element.
            y (str): Second element.
            default_value: Value to return if the pair is not in the cache.

        Returns:
            Cached value or the default value.
        """
        key = self.key_handler.join(x, y)
        return self.cache_dict.get(key, default_value)
