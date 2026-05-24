import pandas as pd
from src.metrics import channel_summary, calculate_ltv_cac, calculate_ad_efficiency


def _funnel():
    return pd.DataFrame({
        'user_id':            [1, 2, 3],
        'lead_id':            [9001, 9002, 9003],
        'opportunity_id':     ['7001', '7002', None],
        'first_touch_source': ['google', 'organic', 'linkedin'],
        'closed_won_flag':    [1, 1, 0],
        'arr':                [48000.0, 36000.0, 0.0],
        'pipeline_value':     [50000.0, 38000.0, 25000.0],
        'retention_months':   [24.0, 12.0, 0.0],
    })


def _sessions():
    return pd.DataFrame({
        'user_id':    [1, 2, 3],
        'utm_source': ['google', 'organic', 'linkedin'],
    })


def _spend():
    return pd.DataFrame({
        'channel':     ['google', 'linkedin'],
        'spend':       [10000.0, 5000.0],
        'clicks':      [500, 200],
        'impressions': [50000, 20000],
    })


def test_channel_summary_has_cac_and_ltv_columns():
    result = channel_summary(_sessions(), _funnel(), _spend())
    assert 'cac' in result.columns
    assert 'avg_ltv' in result.columns
    assert 'ltv_cac_ratio' in result.columns


def test_calculate_ltv_cac_ltv_formula():
    # google: arr=48000, retention=24 → LTV = 48000 * 24 / 12 = 96000
    result = calculate_ltv_cac(_funnel(), _spend())
    google = result[result['channel'] == 'google'].iloc[0]
    assert google['avg_ltv'] == 96000.0


def test_calculate_ltv_cac_cac_formula():
    # google: spend=10000, won_customers=1 → CAC = 10000
    result = calculate_ltv_cac(_funnel(), _spend())
    google = result[result['channel'] == 'google'].iloc[0]
    assert google['cac'] == 10000.0


def test_calculate_ad_efficiency_cpc():
    # google: spend=10000, clicks=500 → CPC = 20.0
    result = calculate_ad_efficiency(_spend())
    google = result[result['channel'] == 'google'].iloc[0]
    assert google['cpc'] == 20.0


def test_calculate_ad_efficiency_ctr():
    # google: clicks=500, impressions=50000 → CTR = 0.01
    result = calculate_ad_efficiency(_spend())
    google = result[result['channel'] == 'google'].iloc[0]
    assert google['ctr'] == 0.01
