# Python
import unittest
import tempfile
import os
import yaml
from rsa.cache.rdm_cache import RDMCache


class TestRDMCacheAddAndGet(unittest.TestCase):

    def setUp(self):
        self.cache = RDMCache()

    def test_add_and_get(self):
        # Add a pair to the cache
        self.cache.add("file1.txt", "file2.txt", 42)

        # Retrieve the value for the added pair
        value = self.cache.get("file1.txt", "file2.txt", None)
        self.assertEqual(value, 42, "The value retrieved from the cache should match the added value.")

    def test_get_default_value(self):
        # Attempt to retrieve a value for a pair not in the cache
        default_value = self.cache.get("file3.txt", "file4.txt", -1)
        self.assertEqual(default_value, -1, "The default value should be returned for a missing pair.")
        default_value = self.cache.get("file3.txt", "file4.txt", -2)
        self.assertEqual(default_value, -2, "The default value should be returned for a missing pair.")

    def test_overwrite_existing_value(self):
        # Add a pair to the cache
        self.cache.add("file1.txt", "file2.txt", 42)

        # Overwrite the value for the same pair
        self.cache.add("file1.txt", "file2.txt", 84)

        # Retrieve the updated value
        updated_value = self.cache.get("file1.txt", "file2.txt", None)
        self.assertEqual(updated_value, 84, "The value should be updated when the pair is added again.")


class TestRDMCacheSerializationVersion250605(unittest.TestCase):

    def setUp(self):
        self.cache = RDMCache()

    def test_load_version_250605(self):
        # Prepare cache data for version 250605
        data = {
            "version": 250605,
            "cache": {"0__-__1": 42, "2__-__3": 84},
            "flist": ["/path/to/file1", "/path/to/file2", "/path/to/file3", "/path/to/file4"],
            "separator": "__-__"
        }

        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
            fp = temp_file.name
            yaml.dump(data, temp_file)

        try:
            self.cache.load_from_file(fp)
            self.assertEqual(self.cache.get("/path/to/file1", "/path/to/file2", None), 42)
            self.assertEqual(self.cache.get("/path/to/file3", "/path/to/file4", None), 84)
        finally:
            os.remove(fp)


class TestRDMCacheSerializationNoVersion(unittest.TestCase):

    def setUp(self):
        self.cache = RDMCache()

    def test_load_no_version(self):
        # Prepare cache data without version
        cache_data = {"0__-__1": 42, "2__-__3": 84}

        # avoid using save_to_file and write to yaml directly
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
            fp = temp_file.name
            yaml.dump(cache_data, temp_file)

        try:
            self.cache.load_from_file(fp)
            self.assertEqual(self.cache.get("0", "1", None), 42)
            self.assertEqual(self.cache.get("2", "3", None), 84)
        finally:
            os.remove(fp)


if __name__ == "__main__":
    unittest.main()
