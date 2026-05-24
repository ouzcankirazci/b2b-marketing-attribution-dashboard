import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

from src.load_data import load_all_data, build_funnel
from src.metrics import calculate_kpis, channel_summary, calculate_ltv_cac, calculate_ad_efficiency, calculate_executive_insights
from src.attribution import last_touch, attribution_paths, same_source_rate
from src import charts

st.set_page_config(
    page_title='Executive Marketing Performance',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded',
)

st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,500;12..96,600;12..96,700;12..96,800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&display=swap');

/* ── Design tokens ── */
:root {
    --brand-dark:  #05393D;
    --brand-mid:   #036B70;
    --brand-light: #2A9EA6;
    --brand-pale:  #C8E9EB;
    --bg-main:     #F2F0EB;
    --bg-card:     #FFFFFF;
    --text-primary:#12201F;
    --text-muted:  #7A7770;
    --border:      #E0DCD6;
    --sidebar-bg:  #0E1A1B;
}

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
[data-testid="stSidebarCollapsedControl"],
[data-testid="stSidebarCollapseButton"] {
    visibility: visible !important;
    opacity: 1 !important;
    z-index: 999999 !important;
}

/* ── Main background ── */
.stApp { background-color: var(--bg-main); }

/* ── Sidebar shell ── */
[data-testid="stSidebar"] {
    background: var(--sidebar-bg) !important;
    border-right: 1px solid rgba(255,255,255,0.05) !important;
}
[data-testid="stSidebar"] * { color: #B8D4D6 !important; }

/* Sidebar title */
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] strong,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2 {
    color: #FFFFFF !important;
    font-family: 'Bricolage Grotesque', sans-serif !important;
    letter-spacing: -0.2px;
}

/* Nav items */
[data-testid="stSidebar"] .stRadio label {
    background: transparent;
    border: none;
    border-left: 2px solid transparent;
    border-radius: 0 6px 6px 0;
    padding: 9px 14px;
    margin-bottom: 1px;
    display: block;
    font-size: 13.5px;
    font-weight: 400;
    color: #96B8BA !important;
    transition: all 0.15s ease;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255,255,255,0.05) !important;
    color: #FFFFFF !important;
    border-left-color: var(--brand-light) !important;
}
[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: rgba(42,158,166,0.14) !important;
    color: #FFFFFF !important;
    border-left-color: var(--brand-light) !important;
    font-weight: 500 !important;
}

/* Sidebar filters */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMarkdown p {
    font-size: 10.5px !important;
    text-transform: uppercase;
    letter-spacing: 0.7px;
    opacity: 0.6;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 6px !important;
    font-size: 13px !important;
}
[data-testid="stSidebar"] hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.07) !important;
    margin: 14px 0 !important;
}

/* ── Typography ── */
h1 {
    font-family: 'Bricolage Grotesque', sans-serif !important;
    font-size: 30px !important;
    font-weight: 700 !important;
    color: var(--brand-dark) !important;
    letter-spacing: -0.8px !important;
    line-height: 1.1 !important;
    margin-bottom: 2px !important;
}
h2 {
    font-family: 'Bricolage Grotesque', sans-serif !important;
    font-size: 17px !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.3px !important;
    margin-top: 6px !important;
}
h3 {
    font-family: 'Bricolage Grotesque', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.2px !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: var(--bg-card);
    border-radius: 10px;
    padding: 16px 20px !important;
    border: 1px solid var(--border);
    border-top: 3px solid var(--brand-mid);
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    transition: box-shadow 0.2s, transform 0.2s;
}
[data-testid="stMetric"]:hover {
    box-shadow: 0 4px 18px rgba(3,107,112,0.1);
    transform: translateY(-1px);
}
[data-testid="stMetricLabel"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 10px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 1.1px;
    color: var(--text-muted) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Bricolage Grotesque', sans-serif !important;
    font-size: 26px !important;
    font-weight: 700 !important;
    color: var(--brand-dark) !important;
    letter-spacing: -0.6px;
    line-height: 1.15;
}

/* ── Plotly chart cards ── */
[data-testid="stPlotlyChart"] {
    background: var(--bg-card);
    border-radius: 12px;
    padding: 8px;
    border: 1px solid var(--border);
    box-shadow: 0 1px 2px rgba(0,0,0,0.03);
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 10px !important;
    overflow: hidden;
    border: 1px solid var(--border) !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    border-radius: 8px !important;
    border-left-width: 3px !important;
    font-size: 13.5px !important;
}

/* ── Dividers ── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 28px 0 !important;
}

/* ── Captions ── */
[data-testid="stCaptionContainer"] p {
    color: var(--text-muted) !important;
    font-size: 12.5px !important;
    line-height: 1.55 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-main); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--brand-light); }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    sessions_df, leads_df, opps_df, revenue_df, ad_spend_df = load_all_data()
    funnel_df = build_funnel(sessions_df, leads_df, opps_df, revenue_df)
    return sessions_df, leads_df, opps_df, revenue_df, ad_spend_df, funnel_df

sessions_df, leads_df, opps_df, revenue_df, ad_spend_df, funnel_df = load_data()

st.sidebar.title('📊 Marketing Performance')
st.sidebar.markdown('---')

pages = [
    '🏠 Executive Summary',
    '📊 Funnel',
    '📣 Channel Attribution',
    '💰 Revenue & ARR',
    '🏢 Segmentation',
    '📈 Ad Spend ROI',
    '🔄 Retention',
    '🌍 Region & Device',
]

page = st.sidebar.radio('Navigate', pages, label_visibility='collapsed')

st.sidebar.markdown('---')
st.sidebar.markdown('**🔽 Filters**')

all_industries = ['All'] + sorted(funnel_df['industry'].dropna().unique().tolist())
all_regions    = ['All'] + sorted(funnel_df['region'].dropna().unique().tolist())
all_sources    = ['All'] + sorted(funnel_df['first_touch_source'].dropna().unique().tolist())

sel_industry = st.sidebar.selectbox('Industry', all_industries)
sel_region   = st.sidebar.selectbox('Region',   all_regions)
sel_source   = st.sidebar.selectbox('Channel',  all_sources)

fdf = funnel_df.copy()
if sel_industry != 'All': fdf = fdf[fdf['industry'] == sel_industry]
if sel_region   != 'All': fdf = fdf[fdf['region']   == sel_region]
if sel_source   != 'All': fdf = fdf[fdf['first_touch_source'] == sel_source]

kpis = calculate_kpis(sessions_df, fdf, ad_spend_df)
total_sessions = kpis['sessions']
total_leads    = kpis['leads']
total_won      = kpis['won_deals']
total_revenue  = kpis['revenue']
total_spend    = kpis['spend']
roi            = round(kpis['roi'], 2)
lead_to_win    = round(kpis['lead_to_win_rate'] * 100, 1)

# ── PAGE ROUTER ──────────────────────────────────────────────────────────────
if page == '🏠 Executive Summary':
    st.title('Executive Marketing Performance')
    st.caption('Filtered view · ' + datetime.now().strftime('%d %b %Y, %H:%M'))

    # KPI Row
    k1,k2,k3,k4,k5,k6 = st.columns(6)
    k1.metric('Sessions',      f'{total_sessions:,}')
    k2.metric('Leads',         f'{total_leads:,}')
    k3.metric('Won Deals',     f'{total_won:,}')
    k4.metric('Revenue (ARR)', f'${total_revenue:,.0f}')
    k5.metric('ROI',           f'{roi:.2f}x')
    k6.metric('Lead-to-Win',   f'{lead_to_win}%')
    st.markdown('---')

    st.subheader('🔍 Key Insights')
    ins = calculate_executive_insights(fdf, ad_spend_df)
    top_channel      = ins['top_channel']
    top_channel_arr  = ins['top_channel_arr']
    top_industry     = ins['top_industry']
    top_industry_rate = ins['top_industry_rate']
    avg_retention    = ins['avg_retention']
    churn_risk       = ins['churn_risk']
    best_roi_ch      = ins['best_roi_ch']
    best_roi_val     = ins['best_roi_val']

    # Insight cards
    i1, i2, i3, i4 = st.columns(4)

    def _card(label, value, sub, accent):
        return (
            f'<div style="background:#FFFFFF;border-radius:10px;padding:18px 20px 16px;'
            f'border:1px solid #E0DCD6;border-top:3px solid {accent};'
            f'box-shadow:0 1px 2px rgba(0,0,0,0.03)">'
            f'<div style="font-size:10px;font-weight:600;text-transform:uppercase;'
            f'letter-spacing:1.1px;color:#7A7770;margin-bottom:8px;'
            f'font-family:\'DM Sans\',sans-serif">{label}</div>'
            f'<div style="font-size:23px;font-weight:700;color:#05393D;'
            f'letter-spacing:-0.5px;line-height:1.15;'
            f'font-family:\'Bricolage Grotesque\',sans-serif">{value}</div>'
            f'<div style="font-size:12px;color:#7A7770;margin-top:5px;'
            f'font-family:\'DM Sans\',sans-serif">{sub}</div>'
            f'</div>'
        )

    with i1:
        st.markdown(_card('Top Revenue Channel', top_channel, f'${top_channel_arr:,.0f} ARR', '#036B70'), unsafe_allow_html=True)
    with i2:
        st.markdown(_card('Best Converting Industry', top_industry, f'{top_industry_rate:.1f}% win rate', '#2A9EA6'), unsafe_allow_html=True)
    with i3:
        st.markdown(_card('Avg Retention', f'{avg_retention:.1f} mo', f'{churn_risk} at churn risk', '#D4602A'), unsafe_allow_html=True)
    with i4:
        st.markdown(_card('Best Pipeline ROI', best_roi_ch, f'{best_roi_val:.1f}× pipeline ROI', '#7A39BB'), unsafe_allow_html=True)

    st.markdown('---')

    # Mini funnel
    st.subheader('📊 Funnel Snapshot')
    f_stages = ['Sessions', 'Leads', 'Opportunities', 'Closed-Won', 'Revenue Events']
    f_values = [len(sessions_df), len(fdf), len(fdf[fdf['opportunity_id'].notna()]), total_won, len(revenue_df)]
    st.plotly_chart(
        charts.plot_funnel_chart(f_stages, f_values, height=340),
        use_container_width=True, config={'displayModeBar': False},
    )

elif page == '📊 Funnel':
    st.title('📊 Lead-to-Revenue Funnel')

    funnel_stages = ['Sessions', 'Leads', 'Opportunities', 'Closed-Won', 'Revenue Events']
    funnel_values = [
        len(sessions_df),
        len(fdf),
        len(fdf[fdf['opportunity_id'].notna()]),
        total_won,
        len(revenue_df),
    ]
    fig_funnel = charts.plot_funnel_chart(funnel_stages, funnel_values, height=420)

    col_f, col_s = st.columns([3,1])

    with col_f:
        st.plotly_chart(fig_funnel, use_container_width=True, config={'displayModeBar': False})

    with col_s:
        st.markdown(
            '<div style="font-family:\'Bricolage Grotesque\',sans-serif;'
            'font-size:14px;font-weight:600;color:#12201F;'
            'letter-spacing:-0.2px;margin-bottom:14px">Conversion Rates</div>',
            unsafe_allow_html=True,
        )
        pairs = [
            ('Session → Lead',       funnel_values[1] / funnel_values[0]  if funnel_values[0] > 0 else 0),
            ('Lead → Opportunity',   funnel_values[2] / funnel_values[1]  if funnel_values[1] > 0 else 0),
            ('Opp → Closed-Won',     funnel_values[3] / funnel_values[2]  if funnel_values[2] > 0 else 0),
            ('Lead → Win (overall)', funnel_values[3] / funnel_values[1]  if funnel_values[1] > 0 else 0),
        ]
        for label, rate in pairs:
            if rate >= 0.20:
                color, bg = '#036B70', 'rgba(3,107,112,0.06)'
            elif rate >= 0.10:
                color, bg = '#D4602A', 'rgba(212,96,42,0.06)'
            else:
                color, bg = '#9B3A3A', 'rgba(155,58,58,0.06)'
            st.markdown(
                f'<div style="margin-bottom:10px;padding:11px 14px;'
                f'background:{bg};border-radius:8px;border-left:2px solid {color}">'
                f'<div style="font-size:10.5px;font-family:\'DM Sans\',sans-serif;'
                f'color:#7A7770;text-transform:uppercase;letter-spacing:0.7px;'
                f'margin-bottom:4px">{label}</div>'
                f'<div style="font-size:22px;font-weight:700;color:{color};'
                f'font-family:\'Bricolage Grotesque\',sans-serif;'
                f'font-variant-numeric:tabular-nums;letter-spacing:-0.5px">'
                f'{rate*100:.1f}%</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

elif page == '📣 Channel Attribution':
    st.title('📣 Channel Attribution')

    lt_df = last_touch(sessions_df, leads_df)
    funnel_with_last = fdf.merge(lt_df, on='user_id', how='left')

    first_arr = (
        fdf[fdf['closed_won_flag'] == 1]
        .groupby('first_touch_source', as_index=False)['arr']
        .sum()
        .rename(columns={'first_touch_source': 'channel'})
    )
    last_arr = (
        funnel_with_last[funnel_with_last['closed_won_flag'] == 1]
        .groupby('last_touch_source', as_index=False)['arr']
        .sum()
        .rename(columns={'last_touch_source': 'channel'})
    )

    paths_df = attribution_paths(funnel_with_last)
    ssrate   = same_source_rate(paths_df)

    st.subheader('First Touch vs Last Touch ARR by Channel')
    st.plotly_chart(
        charts.plot_attribution_comparison(first_arr, last_arr),
        use_container_width=True, config={'displayModeBar': False},
    )
    st.markdown('---')

    col_h, col_s = st.columns([3, 1])
    with col_h:
        st.subheader('Attribution Paths  (First → Last Touch)')
        st.plotly_chart(
            charts.plot_attribution_heatmap(paths_df),
            use_container_width=True, config={'displayModeBar': False},
        )
    with col_s:
        st.metric('Same-Source Rate', f'{ssrate:.1%}')
        st.caption(
            'Share of won ARR where the first and last touch are the same channel. '
            'High = channel both creates and captures demand. '
            'Low = buyer journeys span multiple channels.'
        )

    st.markdown('---')
    st.caption(
        'Channels with high first-touch but lower last-touch ARR are **demand-creation** channels — '
        'they introduce the buyer but the deal closes through a different source. '
        'Evaluate these channels on pipeline influence, not last-touch revenue alone.'
    )

elif page == '💰 Revenue & ARR':
    st.title('💰 Revenue & ARR')

    ch_sum = channel_summary(sessions_df, fdf, ad_spend_df)

    pipeline_by_ch = (
        fdf.groupby('first_touch_source', as_index=False)['pipeline_value']
        .sum()
        .rename(columns={'first_touch_source': 'channel', 'pipeline_value': 'pipeline'})
    )
    arr_by_ch = (
        fdf[fdf['closed_won_flag'] == 1]
        .groupby('first_touch_source', as_index=False)['arr']
        .sum()
        .rename(columns={'first_touch_source': 'channel', 'arr': 'closed_arr'})
    )
    coverage_df = pipeline_by_ch.merge(arr_by_ch, on='channel', how='left').fillna(0)

    plan_df = (
        fdf[fdf['closed_won_flag'] == 1]
        .groupby('plan_type', as_index=False)['arr']
        .sum()
        .dropna(subset=['plan_type'])
    )

    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader('ARR by Channel')
        st.plotly_chart(
            charts.plot_arr_by_channel(ch_sum[['channel', 'revenue']]),
            use_container_width=True, config={'displayModeBar': False},
        )
    with col_r:
        st.subheader('ARR by Plan Type')
        st.plotly_chart(
            charts.plot_arr_by_plan(plan_df),
            use_container_width=True, config={'displayModeBar': False},
        )

    st.markdown('---')
    st.subheader('Pipeline Coverage vs Closed ARR')
    st.plotly_chart(
        charts.plot_pipeline_coverage(coverage_df),
        use_container_width=True, config={'displayModeBar': False},
    )
    st.caption(
        'Pipeline coverage shows total pipeline value entered by first-touch channel '
        'compared to what actually closed. A large gap may indicate conversion '
        'drop-off or long sales cycles in that channel.'
    )

elif page == '🏢 Segmentation':
    st.title('🏢 Segmentation')

    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader('Win Rate by Industry')
        st.plotly_chart(
            charts.plot_win_rate_by_industry(fdf),
            use_container_width=True, config={'displayModeBar': False},
        )
    with col_r:
        st.subheader('ARR by Company Size')
        st.plotly_chart(
            charts.plot_arr_by_company_size(fdf),
            use_container_width=True, config={'displayModeBar': False},
        )

    st.markdown('---')
    st.subheader('Lead Volume by Lifecycle Stage')
    st.plotly_chart(
        charts.plot_leads_by_lifecycle(fdf),
        use_container_width=True, config={'displayModeBar': False},
    )
    st.caption(
        'Lifecycle stage distribution shows the quality mix of leads entering the funnel. '
        'A high proportion of MQLs relative to SQLs may indicate a qualification gap '
        'between marketing and sales handoff.'
    )

elif page == '📈 Ad Spend ROI':
    st.title('📈 Ad Spend ROI')

    ltv_cac_df = calculate_ltv_cac(fdf, ad_spend_df)
    efficiency = calculate_ad_efficiency(ad_spend_df)

    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader('LTV:CAC Ratio by Channel')
        st.plotly_chart(
            charts.plot_ltv_cac_ratio(ltv_cac_df),
            use_container_width=True, config={'displayModeBar': False},
        )
    with col_r:
        st.subheader('Avg LTV vs CAC by Channel')
        st.plotly_chart(
            charts.plot_ltv_cac(ltv_cac_df),
            use_container_width=True, config={'displayModeBar': False},
        )

    st.markdown('---')
    st.subheader('Ad Efficiency by Channel')
    eff_display = efficiency.copy()
    eff_display['cpc'] = eff_display['cpc'].map(lambda v: f'${v:.2f}')
    eff_display['ctr'] = eff_display['ctr'].map(lambda v: f'{v:.2%}')
    eff_display['cpm'] = eff_display['cpm'].map(lambda v: f'${v:.2f}')
    eff_display = eff_display.rename(columns={
        'channel':           'Channel',
        'total_spend':       'Total Spend',
        'total_clicks':      'Clicks',
        'total_impressions': 'Impressions',
        'cpc':               'CPC',
        'ctr':               'CTR',
        'cpm':               'CPM',
    })
    st.dataframe(eff_display, use_container_width=True)
    st.caption(
        'LTV:CAC above 3x is the standard benchmark for sustainable SaaS growth. '
        'Channels below 3x may need spend optimisation or better lead qualification. '
        'CPC and CTR are only available for paid channels (organic has no ad spend).'
    )

elif page == '🔄 Retention':
    st.title('🔄 Retention')

    won_df        = fdf[fdf['closed_won_flag'] == 1]
    avg_retention = won_df['retention_months'].mean() if len(won_df) > 0 else 0
    churn_risk    = int((won_df['retention_months'] <= 3).sum())
    retention_by_plan = (
        won_df.groupby('plan_type', as_index=False)['retention_months']
        .mean()
        .dropna(subset=['plan_type'])
        .sort_values('retention_months', ascending=False)
    )

    k1, k2, k3 = st.columns(3)
    k1.metric('Avg Retention',      f'{avg_retention:.1f} months')
    k2.metric('Churn Risk (≤3 mo)', str(churn_risk))
    k3.metric('Won Customers',      str(len(won_df)))

    st.markdown('---')
    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader('Avg Retention by Channel')
        st.plotly_chart(
            charts.plot_retention_by_channel(fdf),
            use_container_width=True, config={'displayModeBar': False},
        )
    with col_r:
        st.subheader('Retention Distribution')
        st.plotly_chart(
            charts.plot_retention_distribution(fdf),
            use_container_width=True, config={'displayModeBar': False},
        )

    st.markdown('---')
    st.subheader('Avg Retention by Plan Type')
    st.dataframe(
        retention_by_plan.rename(columns={
            'plan_type':        'Plan',
            'retention_months': 'Avg Retention (months)',
        }),
        use_container_width=True,
    )
    st.caption(
        'Retention months is used as a proxy for customer lifetime. '
        'Customers with ≤3 months are flagged as churn risk. '
        'Channels that source long-retention customers have higher true LTV regardless of upfront ARR.'
    )

elif page == '🌍 Region & Device':
    st.title('🌍 Region & Device')

    col_l, col_r = st.columns(2)
    with col_l:
        st.subheader('Leads & Won Deals by Region')
        st.plotly_chart(
            charts.plot_funnel_by_region(fdf),
            use_container_width=True, config={'displayModeBar': False},
        )
    with col_r:
        st.subheader('Win Rate by Region')
        st.plotly_chart(
            charts.plot_win_rate_by_region(fdf),
            use_container_width=True, config={'displayModeBar': False},
        )

    st.markdown('---')
    st.subheader('Session Device Split')
    col_d, col_t = st.columns([1, 2])
    with col_d:
        st.plotly_chart(
            charts.plot_device_split(sessions_df),
            use_container_width=True, config={'displayModeBar': False},
        )
    with col_t:
        device_counts = (
            sessions_df['device_type']
            .value_counts()
            .reset_index()
            .rename(columns={'device_type': 'Device', 'count': 'Sessions'})
        )
        st.dataframe(device_counts, use_container_width=True)
    st.caption(
        'Region data is derived from lead records. '
        'Device split is from raw session data — useful for optimising landing page '
        'and ad creative by device.'
    )

# ── FOOTER ───────────────────────────────────────────────────────────────────
st.sidebar.markdown('---')
st.sidebar.markdown(
    '<small style="color:#bab9b4;">Oğuzcan Kirazcı<br>'
    'Senior Marketing Analyst Portfolio<br>'
    + datetime.now().strftime('%d %b %Y') + '</small>',
    unsafe_allow_html=True,
)
