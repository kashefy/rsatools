import numpy as np


def get_triu_off_diag_flat(mat):
    return mat[np.triu_indices(mat.shape[0], k=1)]


def num_mat_rows(num_triu1_elements):
    nf = 0.5 * (1 + np.sqrt(8 * num_triu1_elements + 1))
    n = int(nf)
    assert (nf == float(n))
    return n


def triu_off_diag_to_mat(triu1vec):
    n = num_mat_rows(triu1vec.size)
    mat = np.zeros((n, n))
    idx = 0
    for r in range(n):
        num_cols = n-r-1
        mat[r, r+1:n] = triu1vec[idx:idx+num_cols]
        idx += num_cols
    return mat
