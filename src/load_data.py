from pathlib import Path
import pandas as pd


def load_all_data(data_dir="data"):
    p = Path(data_dir)
    sessions_df  = pd.read_csv(p / "marketing_sessions.csv")
    leads_df     = pd.read_csv(p / "leads.csv")
    opps_df      = pd.read_csv(p / "opportunities.csv")
    revenue_df   = pd.read_csv(p / "revenue.csv")
    ad_spend_df  = pd.read_csv(p / "ad_spend.csv")
    return sessions_df, leads_df, opps_df, revenue_df, ad_spend_df


def build_funnel(sessions_df, leads_df, opps_df, revenue_df):
    sessions = sessions_df.copy()
    sessions["session_time"] = pd.to_datetime(sessions["session_time"])

    first_touch = (
        sessions.sort_values("session_time")
        .groupby("user_id", as_index=False)
        .first()[["user_id", "utm_source", "utm_medium", "utm_campaign", "country", "device_type"]]
        .rename(columns={
            "utm_source":   "first_touch_source",
            "utm_medium":   "first_touch_medium",
            "utm_campaign": "first_touch_campaign",
        })
    )

    funnel = leads_df.merge(first_touch, on="user_id", how="left")
    funnel = funnel.merge(opps_df,    on="lead_id",   how="left")
    funnel = funnel.merge(revenue_df, on="account_id", how="left")

    funnel["closed_won_flag"] = funnel["closed_won_flag"].fillna(0).astype(int)
    funnel["pipeline_value"]  = funnel["pipeline_value"].fillna(0)
    funnel["arr"]             = funnel["arr"].fillna(0)

    return funnel
