# Python
import unittest
from rsa.cache.cache_key import CacheKey

class TestCacheKey(unittest.TestCase):

    def setUp(self):
        self.cache_key = CacheKey(separator="__-__")

    def test_join_creates_key(self):
        key = self.cache_key.join("file1", "file2")
        self.assertEqual(key, "file1__-__file2", "The key should be correctly joined with the separator.")

    def test_join_is_order_independent(self):
        key1 = self.cache_key.join("file1", "file2")
        key2 = self.cache_key.join("file2", "file1")
        self.assertEqual(key1, key2, "The key should be the same regardless of the order of x and y.")

    def test_split_key(self):
        key = "file1__-__file2"
        x, y = self.cache_key.split(key)
        self.assertEqual(x, "file1", "The first element should be correctly split from the key.")
        self.assertEqual(y, "file2", "The second element should be correctly split from the key.")

    def test_split_and_join_consistency(self):
        key = self.cache_key.join("file1", "file2")
        x, y = self.cache_key.split(key)
        self.assertEqual(key, self.cache_key.join(x, y), "Splitting and rejoining the key should result in the same key.")

if __name__ == "__main__":
    unittest.main()