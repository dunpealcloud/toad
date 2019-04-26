import pytest
import numpy as np
import pandas as pd

from toad import IV, WOE, gini, gini_cond, entropy_cond, quality, KS_bucket
from toad.stats import _IV, VIF
from toad.utils import feature_splits

np.random.seed(1)

feature = np.random.rand(500)
target = np.random.randint(2, size = 500)
A = np.random.randint(100, size = 500)
B = np.random.randint(100, size = 500)
mask = np.random.randint(8, size = 500)

df = pd.DataFrame({
    'feature': feature,
    'target': target,
    'A': A,
    'B': B,
})


def test_woe():
    value = WOE(0.2, 0.3)
    assert value == -0.4054651081081643

def test_iv_priv():
    value = _IV(df['feature'], df['target'])
    assert value == 0.010385942643745353

def test_iv():
    value = IV(df['feature'], df['target'])
    assert value == 0.5313391779453922

def test_iv_frame():
    res = IV(df, 'target')
    assert res.loc[0, 'A'] == 0.3427835694491965

def test_gini():
    value = gini(df['target'])
    assert value == 0.499352

def test_feature_splits():
    value = feature_splits(df['feature'], df['target'])
    assert len(value) == 243

def test_gini_cond():
    value = gini_cond(df['feature'], df['target'])
    assert value == 0.4970162601626016

def test_entropy_cond():
    value = entropy_cond(df['feature'], df['target'])
    assert value == 0.6924990371522171

def test_quality():
    result = quality(df, 'target')
    assert result.loc['feature', 'iv'] == 0.5313391779453922
    assert result.loc['A', 'gini'] == 0.49284164671885444
    assert result.loc['B', 'entropy'] == 0.6924956879070063
    assert result.loc['feature', 'unique'] == 500

def test_quality_iv_only():
    result = quality(df, 'target', iv_only = True)
    assert result.loc['feature', 'gini'] == '--'

def test_quality_object_type_array_with_nan():
    feature = np.array([np.nan, 'A', 'B', 'C', 'D', 'E', 'F', 'G'], dtype = 'O')[mask]

    df = pd.DataFrame({
        'feature': feature,
        'target': target,
    })
    result = quality(df)
    assert result.loc['feature', 'iv'] == 0.01637933818053033

def test_KS_bucket():
    result = KS_bucket(feature, target)
    assert result.loc[4, 'ks'] == 0.028036335090276976

def test_KS_bucket_use_step():
    result = KS_bucket(feature, target, method = 'step', clip_q = 0.01)
    assert result.loc[4, 'ks'] == 0.0422147102645028

def test_KS_bucket_for_all_score():
    result = KS_bucket(feature, target, bucket = False)
    assert len(result) == 500

def test_vif():
    vif = VIF(df)
    assert vif['A'] == 2.9693364426401105
