import os
from itertools import product


class FilePairs:

    def __init__(self, fpairs):
        self.pairs = None
        self.flist = None
        self.tuple_indices = None
        self._validate_pairs(fpairs)

        if fpairs is not None and len(fpairs) > 0:
            self.pairs = fpairs
            self.generate_unique_strings_and_indices()

    @staticmethod
    def _validate_pairs(pairs):
        """
        Validates the pairs attribute.

        Args:
            pairs (list): A list of tuples containing strings.

        Raises:
            TypeError: If pairs is not a list.
            ValueError: If pairs contains invalid elements.
        """
        if not isinstance(pairs, list):
            raise TypeError("pairs must be a list.")
        for item in pairs:
            if not isinstance(item, tuple) or not all(isinstance(sub_item, str) for sub_item in item):
                raise ValueError("pairs must contain only tuples of strings.")

    def generate_unique_strings_and_indices(self):
        if not self.pairs:
            raise ValueError("fpath_list must be a list of tuples of strings to generate indices.")
        self.flist = sorted(list(set(s for tup in self.pairs for s in tup)))

        self.tuple_indices = [tuple(self.flist.index(s) for s in tup) for tup in self.pairs]

    def save_to_files(self, save_dir, flist_path='flist.txt', indices_path='indices.txt'):
        flist_full_path = os.path.join(save_dir, flist_path)
        indices_full_path = os.path.join(save_dir, indices_path)

        with open(flist_full_path, 'w') as f:
            f.write('\n'.join(self.flist))

        with open(indices_full_path, 'w') as f:
            for indices in self.tuple_indices:
                f.write(','.join(map(str, indices)) + '\n')

    def load(self, load_dir, flist_path='flist.txt', indices_path='indices.txt'):

        flist_full_path = os.path.join(load_dir, flist_path)
        with open(flist_full_path, 'r') as f:
            self.flist = f.read().splitlines()

        indices_full_path = os.path.join(load_dir, indices_path)
        if os.path.isfile(indices_full_path):
            with open(indices_full_path, 'r') as f:
                self.tuple_indices = [tuple(map(int, line.split(','))) for line in f]

        else:
            numels = len(self.flist)
            self.tuple_indices = sorted(list(product(range(numels), repeat=2)))

        self.pairs = [tuple(self.flist[i] for i in indices) for indices in self.tuple_indices]
