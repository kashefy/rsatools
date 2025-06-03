from nose.tools import assert_equal, assert_raises, assert_true
import os
import tempfile
import shutil
from rsa.fpairs.file_pairs_from_list import FilePairsFromList
from rsa.fpairs.test_file_pairs import TestFilePairs

class TestFilePairsFromList(TestFilePairs):

    def setup(self):
        self.flist = ["file1", "file2", "file3"]
        self.fpairs = [("file1", "file2"),
                       ("file1", "file3"),
                       ("file2", "file3")]
        self.file_pairs = FilePairsFromList(self.flist)

    def test_initialization(self):
        assert_equal(self.file_pairs.pairs, self.fpairs)

        flist = sorted(self.flist)

        assert_equal(self.file_pairs.flist, flist)
        assert_equal(self.file_pairs.tuple_indices, [(0, 1),
                                                     (0, 2),
                                                     (1, 2)])