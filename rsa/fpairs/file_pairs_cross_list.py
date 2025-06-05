# Python
from itertools import product
from rsa.fpairs.file_pairs import FilePairs


class FilePairsCrossList(FilePairs):
    def __init__(self, flist1, flist2):
        """
        Initializes the CrossFilePairs class with pairs constructed
        between two lists of files, excluding pairs from the same list.

        Args:
            list1 (list): First list of file names.
            list2 (list): Second list of file names.
        """
        if not isinstance(flist1, list) or not isinstance(flist2, list):
            raise TypeError("Both inputs must be lists.")

        if not all(isinstance(item, str) for item in flist1 + flist2):
            raise ValueError("Both lists must contain only strings.")

        # Generate pairs between the two lists
        fpairs = list(product(flist1, flist2))
        fpairs = sorted([(a, b) for a, b in fpairs if a != b]) # remove duplicates
        super().__init__(fpairs)
