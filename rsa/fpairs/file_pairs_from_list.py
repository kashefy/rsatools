from itertools import product
import numpy as np
from rsa.fpairs.file_pairs import FilePairs


class FilePairsFromList(FilePairs):
    def __init__(self, flist):
        """
        Initializes the CrossFilePairs class with pairs constructed
        between two lists of files, excluding pairs from the same list.

        Args:
            list1 (list): First list of file names.
            list2 (list): Second list of file names.
        """
        if not isinstance(flist, list):
            raise TypeError("Input must be a list.")

        if not all(isinstance(item, str) for item in flist):
            raise ValueError("List must contain only strings.")

        # Generate pairs between the two lists
        num_rows = len(flist)
        triu_rows, triu_cols = np.triu_indices(num_rows, k=1)
        fpairs = sorted([(flist[r], flist[c]) for r, c in zip(triu_rows, triu_cols)])
        # print('fpairs', fpairs)
        super().__init__(fpairs)
