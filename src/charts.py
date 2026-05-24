import pandas as pd
import plotly.graph_objects as go

# ── Design tokens ─────────────────────────────────────────────────────────────
_TEAL      = '#036B70'
_TEAL_MID  = '#2A9EA6'
_TEAL_LITE = '#5DC5CC'
_TEAL_PALE = '#A8E0E3'
_ORANGE    = '#D4602A'

_FONT      = 'DM Sans, sans-serif'
_FONT_DISP = 'Bricolage Grotesque, sans-serif'
_TEXT      = '#12201F'
_MUTED     = '#7A7770'
_BORDER    = 'rgba(0,0,0,0.05)'

# Base layout shared by all charts
_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family=_FONT, size=12.5, color=_TEXT),
    margin=dict(t=36, b=24, l=44, r=24),
    showlegend=False,
    # Dark branded hover tooltip
    hoverlabel=dict(
        bgcolor='#0E1A1B',
        font_color='#C8E9EB',
        font_family=_FONT,
        font_size=12,
        bordercolor='rgba(0,0,0,0)',
    ),
)

# Axis base styles
_AXIS_BASE = dict(
    showline=False,
    zeroline=False,
    ticks='',
    tickfont=dict(family=_FONT, size=11.5, color=_MUTED),
    title_font=dict(family=_FONT, size=12, color=_MUTED),
)
# Axis with subtle gridlines (for value axes)
_AXIS_GRID = dict(**_AXIS_BASE, showgrid=True,  gridcolor=_BORDER, gridwidth=1)
# Axis with no gridlines (for category axes)
_AXIS_NONE = dict(**_AXIS_BASE, showgrid=False)


def _layout(**overrides) -> dict:
    return {**_LAYOUT, **overrides}


def _seq(n: int) -> list:
    """Return n-step dark→light teal gradient. Index 0 = darkest (#036B70)."""
    if n <= 1:
        return [_TEAL]
    result = []
    for i in range(n):
        t = i / (n - 1)
        r = round(3   + t * (168 - 3))
        g = round(107 + t * (224 - 107))
        b = round(112 + t * (227 - 112))
        result.append(f'rgb({r},{g},{b})')
    return result


def _legend(**overrides) -> dict:
    base = dict(
        orientation='h', x=0.5, y=-0.18, xanchor='center',
        font=dict(family=_FONT, size=11.5, color=_MUTED),
        bgcolor='rgba(0,0,0,0)', borderwidth=0,
    )
    return {**base, **overrides}


def _label_font(size: int = 11.5) -> dict:
    return dict(family=_FONT, size=size, color=_TEXT)


# ── Funnel stages bar (legacy, kept for compatibility) ────────────────────────

def plot_stage_bar_chart(funnel_summary) -> go.Figure:
    n   = len(funnel_summary)
    colors = list(reversed(_seq(n)))  # ascending → lightest first, top = darkest
    fig = go.Figure(go.Bar(
        x=funnel_summary['count'],
        y=funnel_summary['stage'],
        orientation='h',
        text=funnel_summary['count'].map(lambda v: f'{v:,}'),
        textposition='outside',
        textfont=_label_font(),
        marker=dict(color=colors, line_width=0),
        hovertemplate='<b>%{y}</b><br>%{x:,}<extra></extra>',
    ))
    fig.update_layout(**_layout(
        xaxis=dict(**_AXIS_GRID),
        yaxis=dict(**_AXIS_NONE),
        margin=dict(l=20, r=80, t=40, b=20),
    ))
    fig.update_yaxes(categoryorder='array',
                     categoryarray=['Closed Won', 'Opportunities', 'Leads'])
    return fig


# ── Attribution ───────────────────────────────────────────────────────────────

def plot_attribution_comparison(first_df: pd.DataFrame, last_df: pd.DataFrame) -> go.Figure:
    """Side-by-side ARR bar. Both DataFrames: channel, arr."""
    channels  = sorted(set(first_df['channel'].tolist() + last_df['channel'].tolist()))
    first_map = dict(zip(first_df['channel'], first_df['arr']))
    last_map  = dict(zip(last_df['channel'],  last_df['arr']))

    fig = go.Figure([
        go.Bar(
            name='First Touch',
            x=channels,
            y=[first_map.get(c, 0) for c in channels],
            marker=dict(color=_TEAL, line_width=0, opacity=0.92),
            textfont=_label_font(),
            hovertemplate='<b>%{x}</b><br>First Touch ARR: $%{y:,.0f}<extra></extra>',
        ),
        go.Bar(
            name='Last Touch',
            x=channels,
            y=[last_map.get(c, 0) for c in channels],
            marker=dict(color=_TEAL_LITE, line_width=0, opacity=0.85),
            textfont=_label_font(),
            hovertemplate='<b>%{x}</b><br>Last Touch ARR: $%{y:,.0f}<extra></extra>',
        ),
    ])
    fig.update_layout(**_layout(
        barmode='group',
        bargap=0.25, bargroupgap=0.05,
        showlegend=True,
        legend=_legend(),
        xaxis=dict(**_AXIS_NONE),
        yaxis=dict(**_AXIS_GRID, tickprefix='$', tickformat=',.0f'),
    ))
    return fig


def plot_attribution_heatmap(paths_df: pd.DataFrame) -> go.Figure:
    """Heatmap of first→last touch ARR. paths_df: first_touch, last_touch, arr."""
    pivot = paths_df.pivot_table(
        index='first_touch', columns='last_touch',
        values='arr', aggfunc='sum', fill_value=0,
    )
    # Brand-matched colorscale: near-white → deep teal
    colorscale = [
        [0.0,  '#F2F0EB'],
        [0.25, '#C8E9EB'],
        [0.6,  '#2A9EA6'],
        [1.0,  '#036B70'],
    ]
    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=list(pivot.columns),
        y=list(pivot.index),
        colorscale=colorscale,
        text=[[f'${v:,.0f}' for v in row] for row in pivot.values],
        texttemplate='<b>%{text}</b>',
        textfont=dict(family=_FONT, size=11.5),
        showscale=True,
        colorbar=dict(
            tickfont=dict(family=_FONT, size=11, color=_MUTED),
            tickprefix='$',
            tickformat=',.0f',
            outlinewidth=0,
            thickness=12,
        ),
        hovertemplate='First: <b>%{y}</b><br>Last: <b>%{x}</b><br>ARR: $%{z:,.0f}<extra></extra>',
    ))
    fig.update_layout(**_layout(
        xaxis=dict(**_AXIS_NONE, title='Last Touch'),
        yaxis=dict(**_AXIS_NONE, title='First Touch'),
        margin=dict(t=20, b=60, l=90, r=20),
    ))
    return fig


# ── Revenue ───────────────────────────────────────────────────────────────────

def plot_arr_by_channel(df: pd.DataFrame) -> go.Figure:
    """Horizontal bar of ARR by channel. df: channel, revenue."""
    df = df.sort_values('revenue')  # ascending → highest at top
    n  = len(df)
    colors = list(reversed(_seq(n)))  # light→dark so top (highest) = darkest

    fig = go.Figure(go.Bar(
        x=df['revenue'], y=df['channel'], orientation='h',
        text=df['revenue'].map(lambda v: f'${v:,.0f}'),
        textposition='outside',
        textfont=_label_font(),
        marker=dict(color=colors, line_width=0),
        hovertemplate='<b>%{y}</b><br>ARR: $%{x:,.0f}<extra></extra>',
    ))
    fig.update_layout(**_layout(
        xaxis=dict(**_AXIS_GRID, tickprefix='$', tickformat=',.0f'),
        yaxis=dict(**_AXIS_NONE),
        margin=dict(t=16, b=24, l=20, r=100),
    ))
    return fig


def plot_arr_by_plan(df: pd.DataFrame) -> go.Figure:
    """Donut chart of ARR by plan type. df: plan_type, arr."""
    total = df['arr'].sum()
    colors = [_TEAL, _TEAL_MID, _TEAL_PALE]

    fig = go.Figure(go.Pie(
        labels=df['plan_type'],
        values=df['arr'],
        hole=0.58,
        marker=dict(colors=colors[:len(df)], line=dict(color='white', width=2)),
        textinfo='label+percent',
        textfont=_label_font(11.5),
        pull=[0.04] + [0] * (len(df) - 1),  # slight pull on largest
        hovertemplate='<b>%{label}</b><br>ARR: $%{value:,.0f}<br>Share: %{percent}<extra></extra>',
        direction='clockwise',
        sort=True,
    ))
    # Centre annotation: total ARR
    fig.add_annotation(
        text=f'<b>${total/1000:.0f}k</b><br><span style="font-size:10px">Total ARR</span>',
        x=0.5, y=0.5, showarrow=False, align='center',
        font=dict(family=_FONT_DISP, size=16, color='#05393D'),
        xref='paper', yref='paper',
    )
    fig.update_layout(**_layout(
        showlegend=True, legend=_legend(y=-0.08),
        margin=dict(t=16, b=50, l=20, r=20),
    ))
    return fig


def plot_pipeline_coverage(df: pd.DataFrame) -> go.Figure:
    """Grouped bar: pipeline vs closed ARR. df: channel, pipeline, closed_arr."""
    df = df.sort_values('pipeline', ascending=False)

    fig = go.Figure([
        go.Bar(
            name='Pipeline',
            x=df['channel'], y=df['pipeline'],
            marker=dict(color=_TEAL_LITE, line_width=0, opacity=0.85),
            hovertemplate='<b>%{x}</b><br>Pipeline: $%{y:,.0f}<extra></extra>',
        ),
        go.Bar(
            name='Closed ARR',
            x=df['channel'], y=df['closed_arr'],
            marker=dict(color=_TEAL, line_width=0),
            hovertemplate='<b>%{x}</b><br>Closed ARR: $%{y:,.0f}<extra></extra>',
        ),
    ])
    fig.update_layout(**_layout(
        barmode='group',
        bargap=0.25, bargroupgap=0.05,
        showlegend=True, legend=_legend(),
        xaxis=dict(**_AXIS_NONE),
        yaxis=dict(**_AXIS_GRID, tickprefix='$', tickformat=',.0f'),
    ))
    return fig


# ── Segmentation ──────────────────────────────────────────────────────────────

def plot_win_rate_by_industry(funnel_df: pd.DataFrame) -> go.Figure:
    """Bar chart of win rate per industry."""
    df = (
        funnel_df.groupby('industry')['closed_won_flag']
        .mean().reset_index()
        .rename(columns={'closed_won_flag': 'win_rate'})
        .sort_values('win_rate', ascending=False)
    )
    n = len(df)
    fig = go.Figure(go.Bar(
        x=df['industry'], y=df['win_rate'],
        text=df['win_rate'].map(lambda v: f'{v:.1%}'),
        textposition='outside',
        textfont=_label_font(),
        marker=dict(color=_seq(n), line_width=0),
        hovertemplate='<b>%{x}</b><br>Win Rate: %{customdata:.1%}<extra></extra>',
        customdata=df['win_rate'],
    ))
    fig.update_layout(**_layout(
        xaxis=dict(**_AXIS_NONE),
        yaxis=dict(**_AXIS_GRID, tickformat='.0%', range=[0, df['win_rate'].max() * 1.25]),
    ))
    return fig


def plot_arr_by_company_size(funnel_df: pd.DataFrame) -> go.Figure:
    """Bar chart of won ARR by company size."""
    df = (
        funnel_df[funnel_df['closed_won_flag'] == 1]
        .groupby('company_size', as_index=False)['arr']
        .sum().sort_values('arr', ascending=False)
    )
    n = len(df)
    fig = go.Figure(go.Bar(
        x=df['company_size'], y=df['arr'],
        text=df['arr'].map(lambda v: f'${v:,.0f}'),
        textposition='outside',
        textfont=_label_font(),
        marker=dict(color=_seq(n), line_width=0),
        hovertemplate='<b>%{x}</b><br>ARR: $%{y:,.0f}<extra></extra>',
    ))
    fig.update_layout(**_layout(
        xaxis=dict(**_AXIS_NONE),
        yaxis=dict(**_AXIS_GRID, tickprefix='$', tickformat=',.0f'),
    ))
    return fig


def plot_leads_by_lifecycle(funnel_df: pd.DataFrame) -> go.Figure:
    """Bar chart of lead volume by lifecycle stage."""
    df = (
        funnel_df.groupby('lifecycle_stage', as_index=False)['lead_id']
        .nunique().rename(columns={'lead_id': 'leads'})
        .sort_values('leads', ascending=False)
    )
    n = len(df)
    fig = go.Figure(go.Bar(
        x=df['lifecycle_stage'], y=df['leads'],
        text=df['leads'].map(lambda v: f'{v:,}'),
        textposition='outside',
        textfont=_label_font(),
        marker=dict(color=_seq(n), line_width=0),
        hovertemplate='<b>%{x}</b><br>Leads: %{y:,}<extra></extra>',
    ))
    fig.update_layout(**_layout(
        xaxis=dict(**_AXIS_NONE),
        yaxis=dict(**_AXIS_GRID),
    ))
    return fig


# ── Ad Spend ROI ──────────────────────────────────────────────────────────────

def plot_ltv_cac(df: pd.DataFrame) -> go.Figure:
    """Grouped bar of avg LTV and CAC per channel. df: channel, avg_ltv, cac."""
    df = df.sort_values('avg_ltv', ascending=False)

    fig = go.Figure([
        go.Bar(
            name='Avg LTV',
            x=df['channel'], y=df['avg_ltv'],
            marker=dict(color=_TEAL, line_width=0),
            hovertemplate='<b>%{x}</b><br>Avg LTV: $%{y:,.0f}<extra></extra>',
        ),
        go.Bar(
            name='CAC',
            x=df['channel'], y=df['cac'],
            marker=dict(color=_ORANGE, line_width=0, opacity=0.9),
            hovertemplate='<b>%{x}</b><br>CAC: $%{y:,.0f}<extra></extra>',
        ),
    ])
    fig.update_layout(**_layout(
        barmode='group',
        bargap=0.25, bargroupgap=0.05,
        showlegend=True, legend=_legend(),
        xaxis=dict(**_AXIS_NONE),
        yaxis=dict(**_AXIS_GRID, tickprefix='$', tickformat=',.0f'),
    ))
    return fig


def plot_ltv_cac_ratio(df: pd.DataFrame) -> go.Figure:
    """Bar of LTV:CAC ratio with a 3× benchmark. df: channel, ltv_cac_ratio."""
    df = df.sort_values('ltv_cac_ratio', ascending=False)
    n  = len(df)
    # Colour bars green-teal if above 3x, muted if below
    colors = [_TEAL if v >= 3 else '#B0C8CA' for v in df['ltv_cac_ratio']]

    fig = go.Figure(go.Bar(
        x=df['channel'], y=df['ltv_cac_ratio'],
        text=df['ltv_cac_ratio'].map(lambda v: f'{v:.1f}×'),
        textposition='outside',
        textfont=_label_font(),
        marker=dict(color=colors, line_width=0),
        hovertemplate='<b>%{x}</b><br>LTV:CAC: %{y:.1f}×<extra></extra>',
    ))
    fig.add_hline(
        y=3,
        line=dict(dash='dot', color=_ORANGE, width=1.5),
        annotation_text='3× benchmark',
        annotation_position='top right',
        annotation_font=dict(family=_FONT, size=11, color=_ORANGE),
    )
    fig.update_layout(**_layout(
        xaxis=dict(**_AXIS_NONE),
        yaxis=dict(**_AXIS_GRID, range=[0, max(df['ltv_cac_ratio'].max() * 1.2, 4)]),
        margin=dict(t=36, b=24, l=44, r=90),
    ))
    return fig


# ── Retention ─────────────────────────────────────────────────────────────────

def plot_retention_by_channel(funnel_df: pd.DataFrame) -> go.Figure:
    """Bar of avg retention months per first-touch channel (won deals only)."""
    df = (
        funnel_df[funnel_df['closed_won_flag'] == 1]
        .groupby('first_touch_source', as_index=False)['retention_months']
        .mean().rename(columns={'first_touch_source': 'channel'})
        .sort_values('retention_months', ascending=False)
    )
    n = len(df)
    fig = go.Figure(go.Bar(
        x=df['channel'], y=df['retention_months'],
        text=df['retention_months'].map(lambda v: f'{v:.1f} mo'),
        textposition='outside',
        textfont=_label_font(),
        marker=dict(color=_seq(n), line_width=0),
        hovertemplate='<b>%{x}</b><br>Avg Retention: %{y:.1f} months<extra></extra>',
    ))
    fig.update_layout(**_layout(
        xaxis=dict(**_AXIS_NONE),
        yaxis=dict(**_AXIS_GRID, ticksuffix=' mo'),
    ))
    return fig


def plot_retention_distribution(funnel_df: pd.DataFrame) -> go.Figure:
    """Histogram of retention months for won customers."""
    won = funnel_df[funnel_df['closed_won_flag'] == 1]['retention_months'].dropna()

    fig = go.Figure(go.Histogram(
        x=won, nbinsx=10,
        marker=dict(
            color=_TEAL_MID,
            line=dict(width=1.5, color='white'),
            opacity=0.88,
        ),
        hovertemplate='%{x:.0f}–%{x:.0f} months<br>Count: %{y}<extra></extra>',
    ))
    # Mean line
    mean_val = won.mean()
    fig.add_vline(
        x=mean_val,
        line=dict(dash='dot', color=_ORANGE, width=1.5),
        annotation_text=f'Avg {mean_val:.1f} mo',
        annotation_position='top right',
        annotation_font=dict(family=_FONT, size=11, color=_ORANGE),
    )
    fig.update_layout(**_layout(
        xaxis=dict(**_AXIS_NONE, title='Retention (months)'),
        yaxis=dict(**_AXIS_GRID, title='Customers'),
        bargap=0.08,
    ))
    return fig


# ── Region & Device ───────────────────────────────────────────────────────────

def plot_funnel_by_region(funnel_df: pd.DataFrame) -> go.Figure:
    """Grouped bar: leads and won deals by region."""
    leads_by_r = (
        funnel_df.groupby('region', as_index=False)['lead_id']
        .nunique().rename(columns={'lead_id': 'leads'})
    )
    won_by_r = (
        funnel_df[funnel_df['closed_won_flag'] == 1]
        .groupby('region', as_index=False)['opportunity_id']
        .nunique().rename(columns={'opportunity_id': 'won_deals'})
    )
    df = leads_by_r.merge(won_by_r, on='region', how='left').fillna(0)
    df = df.sort_values('leads', ascending=False)

    fig = go.Figure([
        go.Bar(
            name='Leads',
            x=df['region'], y=df['leads'],
            marker=dict(color=_TEAL_LITE, line_width=0, opacity=0.85),
            hovertemplate='<b>%{x}</b><br>Leads: %{y:,}<extra></extra>',
        ),
        go.Bar(
            name='Won Deals',
            x=df['region'], y=df['won_deals'],
            marker=dict(color=_TEAL, line_width=0),
            hovertemplate='<b>%{x}</b><br>Won Deals: %{y:,}<extra></extra>',
        ),
    ])
    fig.update_layout(**_layout(
        barmode='group',
        bargap=0.3, bargroupgap=0.06,
        showlegend=True, legend=_legend(),
        xaxis=dict(**_AXIS_NONE),
        yaxis=dict(**_AXIS_GRID),
    ))
    return fig


def plot_device_split(sessions_df: pd.DataFrame) -> go.Figure:
    """Donut chart of session share by device type."""
    df = sessions_df['device_type'].value_counts().reset_index()
    df.columns = ['device_type', 'count']
    total = df['count'].sum()

    fig = go.Figure(go.Pie(
        labels=df['device_type'],
        values=df['count'],
        hole=0.58,
        marker=dict(colors=[_TEAL, _TEAL_LITE], line=dict(color='white', width=2)),
        textinfo='label+percent',
        textfont=_label_font(11.5),
        pull=[0.04, 0],
        hovertemplate='<b>%{label}</b><br>Sessions: %{value:,}<br>Share: %{percent}<extra></extra>',
        direction='clockwise',
        sort=True,
    ))
    fig.add_annotation(
        text=f'<b>{total:,}</b><br><span style="font-size:10px">Sessions</span>',
        x=0.5, y=0.5, showarrow=False, align='center',
        font=dict(family=_FONT_DISP, size=16, color='#05393D'),
        xref='paper', yref='paper',
    )
    fig.update_layout(**_layout(
        showlegend=True, legend=_legend(y=-0.08),
        margin=dict(t=16, b=50, l=20, r=20),
    ))
    return fig


def plot_win_rate_by_region(funnel_df: pd.DataFrame) -> go.Figure:
    """Bar chart of win rate by region."""
    df = (
        funnel_df.groupby('region')['closed_won_flag']
        .mean().reset_index()
        .rename(columns={'closed_won_flag': 'win_rate'})
        .sort_values('win_rate', ascending=False)
    )
    n = len(df)
    fig = go.Figure(go.Bar(
        x=df['region'], y=df['win_rate'],
        text=df['win_rate'].map(lambda v: f'{v:.1%}'),
        textposition='outside',
        textfont=_label_font(),
        marker=dict(color=_seq(n), line_width=0),
        hovertemplate='<b>%{x}</b><br>Win Rate: %{customdata:.1%}<extra></extra>',
        customdata=df['win_rate'],
    ))
    fig.update_layout(**_layout(
        xaxis=dict(**_AXIS_NONE),
        yaxis=dict(**_AXIS_GRID, tickformat='.0%', range=[0, df['win_rate'].max() * 1.25]),
    ))
    return fig


# ── Funnel chart ──────────────────────────────────────────────────────────────

def plot_funnel_chart(stages: list, values: list, height: int = 420) -> go.Figure:
    """Plotly funnel chart. stages and values are parallel lists."""
    n      = len(stages)
    colors = _seq(n)  # dark at top (first stage), light at bottom

    # Shorter text for narrow mid/bottom bars to avoid clipping
    conv_text = []
    for i, v in enumerate(values):
        if i == 0:
            conv_text.append(f'{v:,}')
        else:
            pct = values[i] / values[i - 1] * 100 if values[i - 1] > 0 else 0
            conv_text.append(f'{v:,}  ({pct:.0f}%)')

    fig = go.Figure(go.Funnel(
        y=stages, x=values,
        textinfo='text', text=conv_text,
        # 'auto' pushes labels outside when a bar is too narrow to fit text inside
        textposition='auto',
        textfont=dict(family=_FONT, size=12.5, color='white'),
        insidetextanchor='middle',
        marker=dict(
            color=colors,
            line=dict(width=2, color='white'),
        ),
        connector=dict(line=dict(color='rgba(3,107,112,0.10)', width=1)),
        hovertemplate='<b>%{y}</b><br>Count: %{x:,}<extra></extra>',
        opacity=0.95,
    ))
    fig.update_layout(
        height=height,
        # Left margin sized to give stage labels breathing room
        margin=dict(t=16, b=16, l=170, r=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family=_FONT, size=13, color=_TEXT),
        # Stage label styling: dark, using display font for weight
        yaxis=dict(
            tickfont=dict(
                family=_FONT_DISP,
                size=13,
                color='#12201F',
            ),
            showgrid=False,
            showline=False,
            ticks='',
        ),
        hoverlabel=dict(
            bgcolor='#0E1A1B',
            font_color='#C8E9EB',
            font_family=_FONT,
            font_size=12,
            bordercolor='rgba(0,0,0,0)',
        ),
    )
    return fig
