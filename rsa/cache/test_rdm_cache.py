# Python
import unittest
import tempfile
import os
import yaml
from rsa.cache.rdm_cache import RDMCache

class TestRDMCacheVersion250605(unittest.TestCase):

    def setUp(self):
        self.cache = RDMCache()

    def test_load_version_250605(self):
        # Prepare cache data for version 250605
        cache_data = {
            "version": 250605,
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

class TestRDMCacheNoVersion(unittest.TestCase):

    def setUp(self):
        self.cache = RDMCache()

    def test_load_no_version(self):
        # Prepare cache data without version
        cache_data = {
            "cache": {"key1": 42, "key2": 84}
        }

        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
            fp = temp_file.name
            yaml.dump(cache_data, temp_file)

        try:
            self.cache.load_from_file(fp)
            self.assertEqual(self.cache.get("key1", None, None), 42)
            self.assertEqual(self.cache.get("key2", None, None), 84)
        finally:
            os.remove(fp)

if __name__ == "__main__":
    unittest.main()