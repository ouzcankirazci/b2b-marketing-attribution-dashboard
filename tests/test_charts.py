import pandas as pd
import plotly.graph_objects as go
from src import charts


def test_plot_stage_bar_chart_returns_figure():
    df = pd.DataFrame({'stage': ['Leads', 'Opps', 'Won'], 'count': [100, 50, 20]})
    assert isinstance(charts.plot_stage_bar_chart(df), go.Figure)


def test_plot_attribution_comparison_returns_figure():
    first = pd.DataFrame({'channel': ['google', 'organic'], 'arr': [50000, 30000]})
    last  = pd.DataFrame({'channel': ['google', 'organic'], 'arr': [45000, 35000]})
    assert isinstance(charts.plot_attribution_comparison(first, last), go.Figure)


def test_plot_attribution_heatmap_returns_figure():
    paths = pd.DataFrame({
        'first_touch': ['google', 'organic'],
        'last_touch':  ['google', 'google'],
        'arr':         [50000, 20000],
        'won_deals':   [2, 1],
    })
    assert isinstance(charts.plot_attribution_heatmap(paths), go.Figure)


def test_plot_arr_by_channel_returns_figure():
    df = pd.DataFrame({'channel': ['google', 'organic'], 'revenue': [50000, 30000]})
    assert isinstance(charts.plot_arr_by_channel(df), go.Figure)


def test_plot_arr_by_plan_returns_figure():
    df = pd.DataFrame({'plan_type': ['Enterprise', 'Growth'], 'arr': [80000, 40000]})
    assert isinstance(charts.plot_arr_by_plan(df), go.Figure)


def test_plot_pipeline_coverage_returns_figure():
    df = pd.DataFrame({
        'channel':    ['google', 'organic'],
        'pipeline':   [100000, 60000],
        'closed_arr': [50000, 30000],
    })
    assert isinstance(charts.plot_pipeline_coverage(df), go.Figure)


def test_plot_win_rate_by_industry_returns_figure():
    funnel = pd.DataFrame({
        'industry':        ['SaaS', 'SaaS', 'Healthcare'],
        'closed_won_flag': [1, 0, 1],
    })
    assert isinstance(charts.plot_win_rate_by_industry(funnel), go.Figure)


def test_plot_arr_by_company_size_returns_figure():
    funnel = pd.DataFrame({
        'company_size':    ['SMB', 'Enterprise'],
        'arr':             [20000, 80000],
        'closed_won_flag': [1, 1],
    })
    assert isinstance(charts.plot_arr_by_company_size(funnel), go.Figure)


def test_plot_leads_by_lifecycle_returns_figure():
    funnel = pd.DataFrame({
        'lifecycle_stage': ['MQL', 'SQL', 'Lead'],
        'lead_id':         [9001, 9002, 9003],
    })
    assert isinstance(charts.plot_leads_by_lifecycle(funnel), go.Figure)


def test_plot_ltv_cac_returns_figure():
    df = pd.DataFrame({
        'channel': ['google', 'organic'],
        'avg_ltv': [96000, 36000],
        'cac':     [10000, 5000],
    })
    assert isinstance(charts.plot_ltv_cac(df), go.Figure)


def test_plot_ltv_cac_ratio_returns_figure():
    df = pd.DataFrame({
        'channel':       ['google', 'organic'],
        'ltv_cac_ratio': [9.6, 7.2],
    })
    assert isinstance(charts.plot_ltv_cac_ratio(df), go.Figure)


def test_plot_retention_by_channel_returns_figure():
    funnel = pd.DataFrame({
        'first_touch_source': ['google', 'organic'],
        'retention_months':   [24, 12],
        'closed_won_flag':    [1, 1],
    })
    assert isinstance(charts.plot_retention_by_channel(funnel), go.Figure)


def test_plot_retention_distribution_returns_figure():
    funnel = pd.DataFrame({
        'retention_months': [6, 12, 24, 36],
        'closed_won_flag':  [1, 1, 1, 1],
    })
    assert isinstance(charts.plot_retention_distribution(funnel), go.Figure)


def test_plot_funnel_by_region_returns_figure():
    funnel = pd.DataFrame({
        'region':          ['AMER', 'EMEA', 'AMER'],
        'lead_id':         [9001, 9002, 9003],
        'opportunity_id':  ['7001', '7002', None],
        'closed_won_flag': [1, 1, 0],
    })
    assert isinstance(charts.plot_funnel_by_region(funnel), go.Figure)


def test_plot_device_split_returns_figure():
    sessions = pd.DataFrame({'device_type': ['desktop', 'mobile', 'desktop']})
    assert isinstance(charts.plot_device_split(sessions), go.Figure)


def test_plot_win_rate_by_region_returns_figure():
    funnel = pd.DataFrame({
        'region':          ['AMER', 'EMEA', 'AMER'],
        'closed_won_flag': [1, 0, 1],
    })
    assert isinstance(charts.plot_win_rate_by_region(funnel), go.Figure)
