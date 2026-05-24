import pandas as pd
from src.attribution import last_touch, attribution_paths, same_source_rate


def test_last_touch_picks_latest_session_before_lead():
    # user 1: sessions on 2026-01-01 (google) and 2026-01-12 (organic), lead on 2026-01-15
    # latest session before lead_created_at = organic (2026-01-12)
    sessions = pd.DataFrame({
        'user_id':      [1, 1],
        'session_time': ['2026-01-01', '2026-01-12'],
        'utm_source':   ['google', 'organic'],
    })
    leads = pd.DataFrame({
        'user_id':         [1],
        'lead_id':         [9001],
        'lead_created_at': ['2026-01-15'],
    })
    result = last_touch(sessions, leads)
    assert result[result['user_id'] == 1]['last_touch_source'].iloc[0] == 'organic'


def test_last_touch_excludes_sessions_after_lead():
    # session on 2026-01-20 is AFTER lead_created_at (2026-01-15) — must be ignored
    sessions = pd.DataFrame({
        'user_id':      [1, 1, 1],
        'session_time': ['2026-01-01', '2026-01-12', '2026-01-20'],
        'utm_source':   ['google', 'organic', 'brand'],
    })
    leads = pd.DataFrame({
        'user_id':         [1],
        'lead_id':         [9001],
        'lead_created_at': ['2026-01-15'],
    })
    result = last_touch(sessions, leads)
    assert result[result['user_id'] == 1]['last_touch_source'].iloc[0] == 'organic'


def test_attribution_paths_groups_won_deals_by_source_pair():
    funnel = pd.DataFrame({
        'user_id':            [1, 2, 3],
        'opportunity_id':     ['7001', '7002', '7003'],
        'first_touch_source': ['google', 'organic', 'organic'],
        'last_touch_source':  ['organic', 'organic', 'organic'],
        'closed_won_flag':    [1, 1, 1],
        'arr':                [50000.0, 30000.0, 20000.0],
    })
    paths = attribution_paths(funnel)
    # organic→organic path should aggregate 2 deals and $50k ARR
    same = paths[(paths['first_touch'] == 'organic') & (paths['last_touch'] == 'organic')]
    assert same['arr'].iloc[0] == 50000.0
    assert same['won_deals'].iloc[0] == 2


def test_same_source_rate_calculates_share_of_arr():
    paths = pd.DataFrame({
        'first_touch': ['google', 'organic'],
        'last_touch':  ['google', 'linkedin'],
        'arr':         [60000.0, 40000.0],
        'won_deals':   [3, 2],
    })
    # same-source: google→google = 60000 / 100000 = 0.6
    assert same_source_rate(paths) == 0.6
