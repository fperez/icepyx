from icepyx import is2class as ipd
import pytest
import warnings

def test_lowercase_dataset():
    lcds = 'atl03'
    obs = ipd._validate_dataset(lcds)
    expected = 'ATL03'
    assert obs == expected
    
def test_old_version():
    wrng = "You are using an old version of this dataset"
    with pytest.warns(UserWarning, match=wrng):
        ipd.Icesat2Data('ATL06',[-64, 66, -55, 72],['2019-02-22','2019-02-28'], version='1')
#    pytest.warns(UserWarning, ipd.Icesat2Data('ATL06',[-64, 66, -55, 72],['2019-02-22','2019-02-28'], version='1'), match=wrng)
# results in Icesat2Data object is not callable TypeError

def test_date_range_order():
    ermsg = "Your date range is invalid"
    with pytest.raises(AssertionError, match=ermsg):
        ipd.Icesat2Data('ATL06',[-64, 66, -55, 72],['2019-03-22','2019-02-28'])

def test_bad_date_range():
    ermsg = "Your date range list is the wrong length. It should have start and end dates only."
    with pytest.raises(ValueError, match=ermsg):
        ipd.Icesat2Data('ATL06',[-64, 66, -55, 72],['2019-02-22'])
    
def test_time_defaults():
    reg_a = ipd.Icesat2Data('ATL06',[-64, 66, -55, 72],['2019-02-22','2019-02-28'])
    obs_start = reg_a.start_time
    obs_end = reg_a.end_time
    exp_start = '00:00:00'
    exp_end = '23:59:59'
    assert obs_start == exp_start
    assert obs_end == exp_end
    
def test_properties():
    reg_a = ipd.Icesat2Data('ATL06',[-64, 66, -55, 72],['2019-02-22','2019-02-28'],\
                            start_time='03:30:00', end_time='21:30:00', version='2')
    obs_list = [reg_a.dataset, reg_a.dates, reg_a.start_time, reg_a.end_time, reg_a.dataset_version, reg_a.spatial_extent]
    exp_list = ['ATL06',['2019-02-22', '2019-02-28'], '03:30:00', '21:30:00', '002', ['bounding box', [-64, 66, -55, 72]]]
    
    for obs, expected in zip(obs_list,exp_list):
        assert obs == expected
    

def test_CMRparams():
    reg_a = ipd.Icesat2Data('ATL06',[-64, 66, -55, 72],['2019-02-22','2019-02-28'])
    reg_a.build_CMR_params()
    obs_keys = reg_a.CMRparams.keys()
    exp_keys_all = ['short_name','version','temporal']
    exp_keys_any = ['bounding_box','polygon']
    
    assert all(keys in obs_keys for keys in exp_keys_all)
    assert any(key in obs_keys for key in exp_keys_any)
    
def test_reqconfig_params():
    reg_a = ipd.Icesat2Data('ATL06',[-64, 66, -55, 72],['2019-02-22','2019-02-28'])
    
    #test for search params
    reg_a.build_reqconfig_params('search')
    obs_keys = reg_a.reqparams.keys()
    exp_keys_all = ['page_size','page_num']    
    assert all(keys in obs_keys for keys in exp_keys_all)

    #test for download params
    reg_a.reqparams=None
    reg_a.build_reqconfig_params('download')
    reg_a.reqparams.update({'token':'','email':''})
    obs_keys = reg_a.reqparams.keys()
    exp_keys_all = ['page_size','page_num','request_mode','token','email','agent','include_meta']
    assert all(keys in obs_keys for keys in exp_keys_all)
    
#tests to add
#CMR temporal and spatial formats --> what's the best way to compare formatted text? character by character comparison of strings?
#check that search results are correct (spatially, temporally, match actually available data)
#check that downloaded data is subset