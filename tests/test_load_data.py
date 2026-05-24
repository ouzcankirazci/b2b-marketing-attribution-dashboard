import pandas as pd
from src.load_data import build_funnel


def _sessions():
    return pd.DataFrame({
        'user_id':      [1, 1, 2],
        'session_time': ['2026-01-01', '2026-01-10', '2026-01-05'],
        'utm_source':   ['google', 'organic', 'linkedin'],
        'utm_medium':   ['cpc', 'organic', 'cpc'],
        'utm_campaign': ['q1', 'q1', 'q1'],
        'country':      ['US', 'US', 'UK'],
        'device_type':  ['desktop', 'mobile', 'desktop'],
    })


def _leads():
    return pd.DataFrame({
        'user_id':         [1, 2],
        'lead_id':         [9001, 9002],
        'lead_created_at': ['2026-01-15', '2026-01-10'],
        'company_name':    ['Co A', 'Co B'],
        'company_size':    ['SMB', 'Mid-Market'],
        'industry':        ['SaaS', 'Healthcare'],
        'region':          ['AMER', 'EMEA'],
        'lifecycle_stage': ['MQL', 'SQL'],
    })


def _opps():
    return pd.DataFrame({
        'opportunity_id':  [7001],
        'lead_id':         [9001],
        'account_id':      [3001],
        'created_at':      ['2026-02-01'],
        'stage':           ['Closed Won'],
        'pipeline_value':  [50000],
        'close_date':      ['2026-03-01'],
        'closed_won_flag': [1],
    })


def _revenue():
    return pd.DataFrame({
        'account_id':       [3001],
        'booking_date':     ['2026-03-01'],
        'arr':              [48000],
        'plan_type':        ['Enterprise'],
        'retention_months': [24],
    })


def test_build_funnel_has_expected_columns():
    funnel = build_funnel(_sessions(), _leads(), _opps(), _revenue())
    for col in ['first_touch_source', 'arr', 'closed_won_flag', 'pipeline_value']:
        assert col in funnel.columns, f"missing column: {col}"


def test_build_funnel_first_touch_is_earliest_session():
    # user 1 has sessions on 2026-01-01 (google) and 2026-01-10 (organic) — earliest = google
    funnel = build_funnel(_sessions(), _leads(), _opps(), _revenue())
    row = funnel[funnel['user_id'] == 1].iloc[0]
    assert row['first_touch_source'] == 'google'


def test_build_funnel_fills_nulls():
    funnel = build_funnel(_sessions(), _leads(), _opps(), _revenue())
    assert funnel['closed_won_flag'].isna().sum() == 0
    assert funnel['arr'].isna().sum() == 0
    assert funnel['pipeline_value'].isna().sum() == 0
