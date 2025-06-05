import unittest
import tempfile
import os
import yaml
from rsa.cache.rdm_cache import RDMCache


class TestRDMCache(unittest.TestCase):

    def setUp(self):
        self.cache = RDMCache()

    def test_add_and_get(self):
        # Test adding and retrieving a value with file path-like strings
        self.cache.add("/path/to/file1", "/path/to/file2", 42)
        self.assertEqual(self.cache.get("/path/to/file1", "/path/to/file2", None), 42)
        self.assertEqual(self.cache.get("/path/to/file2", "/path/to/file1", None), 42)  # Ensure symmetry
        self.assertEqual(self.cache.get("/path/to/unknown", "/path/to/file2", "default"),
                         "default")  # Test default value

    def test_save_to_file(self):
        # Test saving cache to a file
        self.cache.add("/path/to/file1", "/path/to/file2", 42)
        self.cache.add("/path/to/file3", "/path/to/file4", 84)

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            fp = temp_file.name

        try:
            self.cache.save_to_file(fp)
            with open(fp, 'r') as f:
                data = yaml.safe_load(f)
                self.assertIn("cache", data)
                self.assertIn("flist", data)
                self.assertIn("separator", data)
        finally:
            os.remove(fp)

    def test_load_from_file(self):
        # Test loading cache from a file
        cache_data = {
            "cache": {"0__-__1": 42, "2__-__3": 84},
            "flist": ["/path/to/file1", "/path/to/file2", "/path/to/file3", "/path/to/file4"],
            "separator": "__-__"
        }

        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
            fp = temp_file.name
            yaml.dump(cache_data, temp_file)

        try:
            self.cache.load_from_file(fp)
            self.assertEqual(self.cache.get("/path/to/file1", "/path/to/file2", None), 42)
            self.assertEqual(self.cache.get("/path/to/file3", "/path/to/file4", None), 84)
        finally:
            os.remove(fp)

    def test_save_and_load(self):
        # Test saving and loading cache
        self.cache.add("/path/to/file1", "/path/to/file2", 42)
        self.cache.add("/path/to/file3", "/path/to/file4", 84)

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            fp = temp_file.name

        try:
            self.cache.save_to_file(fp)
            new_cache = RDMCache()
            new_cache.load_from_file(fp)
            self.assertEqual(new_cache.get("/path/to/file1", "/path/to/file2", None), 42)
            self.assertEqual(new_cache.get("/path/to/file3", "/path/to/file4", None), 84)
        finally:
            os.remove(fp)


if __name__ == "__main__":
    unittest.main()
