import pandas as pd


def last_touch(sessions_df, leads_df):
    """Return the last utm_source per user at or before their lead_created_at date."""
    sessions = sessions_df[["user_id", "session_time", "utm_source"]].copy()
    sessions["session_time"] = pd.to_datetime(sessions["session_time"])

    leads = leads_df[["user_id", "lead_created_at"]].copy()
    leads["lead_created_at"] = pd.to_datetime(leads["lead_created_at"])

    merged = sessions.merge(leads, on="user_id", how="inner")
    pre_lead = merged[merged["session_time"] <= merged["lead_created_at"]]

    result = (
        pre_lead.sort_values("session_time")
        .groupby("user_id", as_index=False)
        .last()[["user_id", "utm_source"]]
        .rename(columns={"utm_source": "last_touch_source"})
    )
    return result


def attribution_paths(funnel_df):
    """Group won deals by (first_touch_source, last_touch_source) pair.

    funnel_df must have a last_touch_source column (add via last_touch() merge).
    Returns DataFrame with: first_touch, last_touch, won_deals, arr.
    """
    won = funnel_df[funnel_df["closed_won_flag"] == 1].copy()
    paths = (
        won.groupby(["first_touch_source", "last_touch_source"], as_index=False)
        .agg(won_deals=("opportunity_id", "nunique"), arr=("arr", "sum"))
        .rename(columns={
            "first_touch_source": "first_touch",
            "last_touch_source":  "last_touch",
        })
        .sort_values("arr", ascending=False)
        .reset_index(drop=True)
    )
    return paths


def same_source_rate(paths_df):
    """Return the share of won ARR where first_touch == last_touch."""
    total = paths_df["arr"].sum()
    if total == 0:
        return 0.0
    same = paths_df.loc[paths_df["first_touch"] == paths_df["last_touch"], "arr"].sum()
    return float(same / total)
