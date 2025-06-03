from nose.tools import assert_equal, assert_raises, assert_true
import os
import tempfile
import shutil
from rsa.fpairs.file_pairs import FilePairs


class TestFilePairs:

    @classmethod
    def setup_class(cls):
        cls.test_dir = tempfile.mkdtemp()

    @classmethod
    def teardown_class(cls):
        shutil.rmtree(cls.test_dir)

    def setup(self):
        self.fpairs = [("file1", "file2"), ("file3", "file4"), ("file1", "file3")]
        self.file_pairs = FilePairs(self.fpairs)

    def test_initialization(self):
        assert_equal(self.file_pairs.pairs, self.fpairs)
        assert_equal(self.file_pairs.flist, ["file1", "file2", "file3", "file4"])
        assert_equal(self.file_pairs.tuple_indices, [(0, 1), (2, 3), (0, 2)])

    def test_validate_pairs(self):
        with assert_raises(TypeError):
            FilePairs._validate_pairs("invalid")
        with assert_raises(ValueError):
            FilePairs._validate_pairs([("file1", 123)])

    def test_save_to_files(self):
        self.file_pairs.save_to_files(self.test_dir)
        flist_path = os.path.join(self.test_dir, "flist.txt")
        indices_path = os.path.join(self.test_dir, "indices.txt")

        assert_true(os.path.exists(flist_path))
        assert_true(os.path.exists(indices_path))

        with open(flist_path, "r") as f:
            assert_equal(f.read().splitlines(), self.file_pairs.flist)

        with open(indices_path, "r") as f:
            assert_equal(
                [tuple(map(int, line.split(","))) for line in f],
                self.file_pairs.tuple_indices,
            )

    def test_load(self):
        self.file_pairs.save_to_files(self.test_dir)
        new_file_pairs = FilePairs([])
        new_file_pairs.load(self.test_dir)

        assert_equal(new_file_pairs.flist, self.file_pairs.flist)
        assert_equal(new_file_pairs.tuple_indices, self.file_pairs.tuple_indices)

