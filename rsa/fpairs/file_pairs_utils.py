from rsa.fpairs.file_pairs import FilePairs                     # pairs already provided
from rsa.fpairs.file_pairs_cross_list import FilePairsCrossList # pairs from two lists
from rsa.fpairs.file_pairs_from_list import FilePairsFromList   # all pairs from one list

def create_file_pairs(flist1, flist2=None):
    """
    Create file pairs based on the provided lists.

    Args:
        flist1 (list): First list of file names or a list of tuples of strings.
        flist2 (list, optional): Second list of file names.

    Returns:
        FilePairs: An instance of FilePairsCrossList, FilePairsFromList, or FilePairs.
    """
    if flist1 is not None and flist2 is not None:
        # both lists provided
        return FilePairsCrossList(flist1, flist2)
    elif flist1 is not None:
        # only one list provided
        if isinstance(flist1, list):
            # Check if flist1 is a list of tuples of strings or a list of strings
            if all(isinstance(item, tuple) and all(isinstance(sub_item, str) for sub_item in item) for item in flist1):
                return FilePairs(flist1)
            return FilePairsFromList(flist1)
        else:
            raise TypeError("flist1 must be a list.")
    else:
        raise ValueError("At least one file list must be provided.")
