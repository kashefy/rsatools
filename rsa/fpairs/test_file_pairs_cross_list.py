from nose.tools import assert_equal, assert_raises, assert_true
import os
import tempfile
import shutil
from rsa.fpairs.file_pairs_cross_list import FilePairsCrossList
from rsa.fpairs.test_file_pairs import TestFilePairs


class TestFilePairsCrossList(TestFilePairs):

    def setup(self):
        self.flist1 = ["file1", "file2", "file3"]
        self.flist2 = ["file4", "file5", "file6"]
        self.fpairs = [("file1", "file4"),
                       ("file1", "file5"),
                       ("file1", "file6"),
                       ("file2", "file4"),
                       ("file2", "file5"),
                       ("file2", "file6"),
                       ("file3", "file4"),
                       ("file3", "file5"),
                       ("file3", "file6")]
        self.file_pairs = FilePairsCrossList(self.flist1, self.flist2)

    def test_initialization(self):
        assert_equal(self.file_pairs.pairs, self.fpairs)

        flist = sorted(self.flist1 + self.flist2)

        assert_equal(self.file_pairs.flist, flist)
        assert_equal(self.file_pairs.tuple_indices, [(0, 3),
                                                     (0, 4),
                                                     (0, 5),
                                                     (1, 3),
                                                     (1, 4),
                                                     (1, 5),
                                                     (2, 3),
                                                     (2, 4),
                                                     (2, 5)])

    def test_validate_pairs(self):
        with assert_raises(TypeError):
            FilePairsCrossList._validate_pairs("invalid")
        with assert_raises(ValueError):
            FilePairsCrossList._validate_pairs([("file1", 123)])

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
        new_file_pairs = FilePairsCrossList([], [])
        new_file_pairs.load(self.test_dir)

        assert_equal(new_file_pairs.flist, self.file_pairs.flist)
        assert_equal(new_file_pairs.tuple_indices, self.file_pairs.tuple_indices)


class TestFilePairsCrossListWithDuplicates(TestFilePairs):

    def setup(self):
        self.flist1 = ["file1", "file2", "file3"]
        self.flist2 = ["file1", "file4", "file5"]
        self.fpairs = [("file1", "file4"),
                       ("file1", "file5"),
                       ("file2", "file1"),
                       ("file2", "file4"),
                       ("file2", "file5"),
                       ("file3", "file1"),
                       ("file3", "file4"),
                       ("file3", "file5")]
        self.file_pairs = FilePairsCrossList(self.flist1, self.flist2)

    def test_initialization(self):
        assert_equal(self.file_pairs.pairs, self.fpairs)

        flist = self.flist1 + self.flist2
        flist = sorted(set(flist))  # Remove duplicates

        assert_equal(self.file_pairs.flist, flist)
        assert_equal(self.file_pairs.tuple_indices, [(0, 3),
                                                     (0, 4),
                                                     (1, 0),
                                                     (1, 3),
                                                     (1, 4),
                                                     (2, 0),
                                                     (2, 3),
                                                     (2, 4)])

    def test_validate_pairs(self):
        with assert_raises(TypeError):
            FilePairsCrossList._validate_pairs("invalid")
        with assert_raises(ValueError):
            FilePairsCrossList._validate_pairs([("file1", 123)])

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
        new_file_pairs = FilePairsCrossList([], [])
        new_file_pairs.load(self.test_dir)

        assert_equal(new_file_pairs.flist, self.file_pairs.flist)
        assert_equal(new_file_pairs.tuple_indices, self.file_pairs.tuple_indices)
