import multiprocessing as mp
import errno
from pathlib import Path
import os
from tqdm import tqdm
import numpy as np
from rsa.model_rdm_utils import calc_spearman_rank_corr_from_files, ENTRY_EMPTY
from rsa.rdm_loader import RDMLoaderNPY
from rsa.model_rdm import ModelRDM
import rsa.mat_utils as mutils
from rsa.fpairs.file_pairs_utils import create_file_pairs


class ModelRDMPaired(ModelRDM):

    def __init__(self, fpath_list):
        self.pairs = create_file_pairs(fpath_list) if fpath_list else None
        super().__init__(self.pairs.flist if self.pairs else None)

    def set_pairs(self, pairs):
        self.pairs = pairs
        self.fp_list = self.pairs.flist

    def _init_model_rdm_triu(self):
        self.numels = len(self.pairs) if self.pairs else 0
        self.model_rdm_triu = np.zeros((self.numels,)) + ENTRY_EMPTY

    def dissimilarity(self, fp_row, fp_col, idx):

        if self.model_rdm_triu[idx] == ENTRY_EMPTY:
            idx, _, _, spearman = calc_spearman_rank_corr_from_files(fp_row, fp_col, -1, -1, idx, loader=self.loader)
            return idx, 1 - spearman.correlation

    def apply(self, processes=1, chunksize=10, do_disable_tqdm=False):

        self._init_model_rdm_triu()

        with mp.get_context("spawn").Pool(processes=processes) as pool:
            result = pool.starmap(self.dissimilarity,
                                  tqdm(
                                      [(self.pairs.get(idx)[0],
                                        self.pairs.get(idx)[1], idx)
                                       for idx in range(self.numels)],
                                      total=self.numels,
                                      disable=do_disable_tqdm),
                                  chunksize=chunksize,
                                  )

        for idx, dissimilarity in result:
            self.model_rdm_triu[idx] = dissimilarity
        return self.model_rdm_triu

