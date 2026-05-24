import pandas as pd


def calculate_kpis(sessions_df, funnel_df, ad_spend_df):
    total_sessions = len(sessions_df)
    total_leads    = funnel_df["lead_id"].nunique()

    won_mask    = funnel_df["closed_won_flag"] == 1
    won_deals   = funnel_df.loc[won_mask, "opportunity_id"].nunique()
    total_rev   = funnel_df.loc[won_mask, "arr"].fillna(0).sum()
    total_spend = ad_spend_df["spend"].sum()

    roi         = total_rev / total_spend if total_spend else 0
    lead_to_win = won_deals / total_leads if total_leads else 0

    return {
        "sessions":         int(total_sessions),
        "leads":            int(total_leads),
        "won_deals":        int(won_deals),
        "revenue":          float(total_rev),
        "spend":            float(total_spend),
        "roi":              float(roi),
        "lead_to_win_rate": float(lead_to_win),
    }


def channel_summary(sessions_df, funnel_df, ad_spend_df):
    sessions_by_ch = (
        sessions_df.groupby("utm_source", as_index=False)
        .size()
        .rename(columns={"utm_source": "channel", "size": "sessions"})
    )

    leads_by_ch = (
        funnel_df.groupby("first_touch_source", as_index=False)["lead_id"]
        .nunique()
        .rename(columns={"first_touch_source": "channel", "lead_id": "leads"})
    )

    won = funnel_df[funnel_df["closed_won_flag"] == 1]

    won_by_ch = (
        won.groupby("first_touch_source", as_index=False)["opportunity_id"]
        .nunique()
        .rename(columns={"first_touch_source": "channel", "opportunity_id": "won_deals"})
    )

    rev_by_ch = (
        won.groupby("first_touch_source", as_index=False)["arr"]
        .sum()
        .rename(columns={"first_touch_source": "channel", "arr": "revenue"})
    )

    spend_by_ch = ad_spend_df.groupby("channel", as_index=False)["spend"].sum()

    ltv_by_ch = (
        won.assign(ltv=lambda x: x["arr"] * x["retention_months"].fillna(0) / 12)
        .groupby("first_touch_source", as_index=False)["ltv"]
        .mean()
        .rename(columns={"first_touch_source": "channel", "ltv": "avg_ltv"})
    )

    df = (
        sessions_by_ch
        .merge(leads_by_ch,  on="channel", how="outer")
        .merge(won_by_ch,    on="channel", how="outer")
        .merge(rev_by_ch,    on="channel", how="outer")
        .merge(spend_by_ch,  on="channel", how="outer")
        .merge(ltv_by_ch,    on="channel", how="outer")
    )

    for col in ["sessions", "leads", "won_deals", "revenue", "spend", "avg_ltv"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["sessions"]  = df["sessions"].astype(int)
    df["leads"]     = df["leads"].astype(int)
    df["won_deals"] = df["won_deals"].astype(int)

    df["lead_rate"]     = df["leads"]     / df["sessions"].replace(0, pd.NA)
    df["win_rate"]      = df["won_deals"] / df["leads"].replace(0, pd.NA)
    df["roi"]           = df["revenue"]   / df["spend"].replace(0, pd.NA)
    df["cac"]           = df["spend"]     / df["won_deals"].replace(0, pd.NA)
    df["ltv_cac_ratio"] = df["avg_ltv"]   / df["cac"].replace(0, pd.NA)

    return df.fillna(0).sort_values("revenue", ascending=False).reset_index(drop=True)


def calculate_ltv_cac(funnel_df, ad_spend_df):
    won = funnel_df[funnel_df["closed_won_flag"] == 1].copy()
    won["ltv"] = won["arr"] * won["retention_months"].fillna(0) / 12

    ltv_by_ch = (
        won.groupby("first_touch_source", as_index=False)
        .agg(avg_ltv=("ltv", "mean"), won_customers=("opportunity_id", "nunique"))
        .rename(columns={"first_touch_source": "channel"})
    )

    spend_by_ch = ad_spend_df.groupby("channel", as_index=False)["spend"].sum()

    df = ltv_by_ch.merge(spend_by_ch, on="channel", how="left").fillna(0)
    df["cac"]           = df["spend"]   / df["won_customers"].replace(0, pd.NA)
    df["ltv_cac_ratio"] = df["avg_ltv"] / df["cac"].replace(0, pd.NA)

    return df.fillna(0).sort_values("ltv_cac_ratio", ascending=False).reset_index(drop=True)


def calculate_ad_efficiency(ad_spend_df):
    df = (
        ad_spend_df.groupby("channel", as_index=False)
        .agg(
            total_spend=("spend", "sum"),
            total_clicks=("clicks", "sum"),
            total_impressions=("impressions", "sum"),
        )
    )
    df["cpc"] = df["total_spend"]  / df["total_clicks"].replace(0, pd.NA)
    df["ctr"] = df["total_clicks"] / df["total_impressions"].replace(0, pd.NA)
    df["cpm"] = df["total_spend"]  / (df["total_impressions"] / 1000).replace(0, pd.NA)

    return df.fillna(0).reset_index(drop=True)


def calculate_executive_insights(funnel_df, ad_spend_df):
    won = funnel_df[funnel_df["closed_won_flag"] == 1]

    src_arr     = funnel_df.groupby("first_touch_source")["arr"].sum()
    top_channel     = src_arr.idxmax() if len(won) > 0 else "N/A"
    top_channel_arr = float(src_arr.max()) if len(won) > 0 else 0.0

    ind_rate         = funnel_df.groupby("industry")["closed_won_flag"].mean()
    top_industry      = ind_rate.idxmax() if len(won) > 0 else "N/A"
    top_industry_rate = float(ind_rate.max() * 100) if len(won) > 0 else 0.0

    avg_retention = float(won["retention_months"].mean()) if len(won) > 0 else 0.0
    churn_risk    = int((won["retention_months"] <= 3).sum())

    spend_by_ch        = ad_spend_df.groupby("channel")["spend"].sum().reset_index()
    pipe_by_ch         = funnel_df.groupby("first_touch_source")["pipeline_value"].sum().reset_index()
    pipe_by_ch.columns = ["channel", "pipeline_value"]
    roi_ch             = pd.merge(spend_by_ch, pipe_by_ch, on="channel", how="left").fillna(0)
    roi_ch["roi"]      = roi_ch["pipeline_value"] / roi_ch["spend"].replace(0, pd.NA)
    best_roi_ch  = roi_ch.loc[roi_ch["roi"].idxmax(), "channel"] if len(roi_ch) > 0 else "N/A"
    best_roi_val = float(roi_ch["roi"].max()) if len(roi_ch) > 0 else 0.0

    return {
        "top_channel":      top_channel,
        "top_channel_arr":  top_channel_arr,
        "top_industry":     top_industry,
        "top_industry_rate": top_industry_rate,
        "avg_retention":    avg_retention,
        "churn_risk":       churn_risk,
        "best_roi_ch":      best_roi_ch,
        "best_roi_val":     best_roi_val,
    }
