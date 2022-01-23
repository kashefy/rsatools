import multiprocessing as mp
import tqdm
import numpy as np
from scipy.stats import spearmanr
import rsa.mat_utils as mutils
from rsa.input_rdm_utils import get_input_rdm_flat_from_file

ENTRY_EMPTY = -999


def calc_spearman_rank_corr_from_files(fpath_in_i, fpath_in_j, i, j, idx):
    rdm_i = get_input_rdm_flat_from_file(fpath_in_i)
    rdm_j = get_input_rdm_flat_from_file(fpath_in_j)
    return idx, i, j, spearmanr(rdm_i, rdm_j)


def calc_model_rdm(fpath_in_rdms_all_1,
                   fpath_in_rdms_all_2,
                   processes=1,
                   do_disable_tqdm=False):
    if fpath_in_rdms_all_1 == fpath_in_rdms_all_2:
        model_rdm = calc_model_rdm_symmetric(fpath_in_rdms_all_1,
                                             processes=processes,
                                             do_disable_tqdm=do_disable_tqdm)
    else:
        raise NotImplementedError
    return model_rdm


def calc_model_rdm_symmetric(fpath_in_all, processes=1, do_disable_tqdm=False):
    # if processes < 2:
    #     model_rdm = _calc_model_rdm_symmetric_sequential(fpath_in_all)
    # else:
    model_rdm = _calc_model_rdm_symmetric_parallel(fpath_in_all,
                                                   processes,
                                                   do_disable_tqdm=do_disable_tqdm)
    return model_rdm


def _calc_model_rdm_symmetric_sequential(fpath_in_all):
    nrows = len(fpath_in_all)
    ncols = nrows
    model_rdm = np.zeros((nrows, ncols)) + ENTRY_EMPTY

    for r, fpath_in_rdm_1 in enumerate(fpath_in_all):
        in_rdm_1 = get_input_rdm_flat_from_file(fpath_in_rdm_1)  # .flatten()
        for c, fpath_in_rdm_2 in enumerate(fpath_in_all):
            if r == c:
                # dissimilarity with itself is zero
                model_rdm[r, c] = 0.
            elif model_rdm[r, c] == ENTRY_EMPTY:
                in_rdm_2 = get_input_rdm_flat_from_file(fpath_in_rdm_2)  # .flatten()
                # assumes symmetry, essentially list 1 == list 2...
                model_rdm[r, c] = model_rdm[c, r] = 1 - spearmanr(in_rdm_1, in_rdm_2)[0]
    return model_rdm


def _calc_model_rdm_symmetric_parallel(fpath_in_all, processes, do_disable_tqdm=False):
    nrows = len(fpath_in_all)
    triu_rows, triu_cols = np.triu_indices(nrows, k=1)
    with mp.Pool(processes=processes) as pool:
        result = pool.starmap(calc_spearman_rank_corr_from_files,
                              tqdm.tqdm(
                                  [(fpath_in_all[row],
                                    fpath_in_all[col], row, col, idx)
                                   for idx, (row, col) in enumerate(zip(triu_rows, triu_cols))], total=len(triu_rows),
                                  disable=do_disable_tqdm),
                              chunksize=10,
                              )
    model_rdm_triu = np.zeros((triu_rows.size,)) + ENTRY_EMPTY
    # for r in range(nrows):
    #     model_rdm[r, r] = 0.  # set diagonal to zero dissimilarity
    for idx, r, c, result_spearman in result:
        # model_rdm[r, c] = model_rdm[c, r] = 1 - result_spearman.correlation
        model_rdm_triu[idx] = 1 - result_spearman.correlation
    return model_rdm_triu

