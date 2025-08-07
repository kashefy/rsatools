from nose import tools
from nose.tools import assert_equal, \
    assert_true, assert_false, \
    assert_raises, assert_list_equal
import shutil
import tempfile
import os
import yaml

from rsa.cache.rdm_cache import RDMCache
from rsa.model_rdm_cached import ModelRDMCached

from rsa.test_model_rdm import TestModelRDMInput2DMat, \
    TestModelRDMInput2DMatNPZ, \
    TestModelRDMInput2DMaInMemory


def helper_compare_mrdm_cache(flist, mrdm, cache):
    assert_equal(len(cache.cache_dict.keys()), mrdm.size)

    idx = 0
    for row in range(len(flist)):
        for col in range(row + 1, len(flist)):
            fp_row = flist[row]
            fp_col = flist[col]
            assert_equal(cache.get(fp_row, fp_col, 123), mrdm[idx])
            idx += 1


def helper_calc_model_rdm_with_cache(flist, fp_cache):
    with open(fp_cache, 'w') as h:
        h.write(yaml.dump({}))

    m = ModelRDMCached(flist, fp_cache)
    mrdm = m.apply(do_disable_tqdm=True)

    with open(fp_cache, 'r') as h:
        cache_dict = yaml.safe_load(h)

    helper_compare_mrdm_cache(flist, mrdm, m.cache)

    return mrdm


class TestModelRDMCachedInput2DMatEmptyCache(TestModelRDMInput2DMat):

    def helper_calc_model_rdm(self, flist):
        fp_cache = os.path.join(self.dir_tmp, 'my_cache.yml')
        mrdm = helper_calc_model_rdm_with_cache(flist, fp_cache)

        return mrdm


class TestModelRDMCachedInput2DMatNPZEmptyCache(TestModelRDMInput2DMatNPZ):

    def helper_calc_model_rdm(self, flist):
        fp_cache = os.path.join(self.dir_tmp, 'my_cache.yml')
        mrdm = helper_calc_model_rdm_with_cache(flist, fp_cache)

        return mrdm


class TestModelRDMCachedInput2DMaInMemoryEmptyCache(TestModelRDMInput2DMaInMemory):

    def helper_calc_model_rdm(self, flist):
        fp_cache = os.path.join(self.dir_tmp, 'my_cache.yml')
        mrdm = helper_calc_model_rdm_with_cache(flist, fp_cache)

        return mrdm


class TestModelRDMCachedCacheHits:

    @classmethod
    def setup_class(cls):
        cls.dir_tmp = tempfile.mkdtemp()

    @classmethod
    def teardown_class(cls):
        shutil.rmtree(cls.dir_tmp)
        pass

    def test_cache_hits_cache_hits_all(self):
            flist = [os.path.join(self.dir_tmp, fp) for fp in ['a.npy', 'b.npy', 'c.npy']]

            data = {
                "version": 250605,
                "cache": {"0__-__1": 0.1, "0__-__2": 0.2, "1__-__2": 0.12},
                "flist": flist,
                "separator": "__-__"
            }
            cache = RDMCache()
            cache.load_from_dict(data)

            fp_cache = os.path.join(self.dir_tmp, 'my_cache.yml')
            cache.save_to_file(fp_cache)

            m = ModelRDMCached(flist, fp_cache)
            m.apply(do_disable_tqdm=True)
            assert_equal(m.get_cache_hits(), 3)