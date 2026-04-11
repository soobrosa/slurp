import altair as alt
import pandas as pd
import streamlit as st

DATA_URL = "https://github.com/soobrosa/slurp/raw/main/outputs/paparazzi.csv"
METRICS = {
    "Stars": "stargazers_count",
    "Forks": "forks_count",
    "Open issues": "open_issues_count",
    "Watchers": "subscribers_count",
}


@st.cache_data(ttl=3600)
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_URL)
    df["date"] = pd.to_datetime(df["date"])
    df = df.drop_duplicates(subset=["name", "date"], keep="last")
    return df.sort_values(["name", "date"]).reset_index(drop=True)


def pivot(df: pd.DataFrame, col: str) -> pd.DataFrame:
    return df.pivot_table(index="date", columns="name", values=col).sort_index()


def delta(series: pd.Series, days: int):
    s = series.dropna()
    if len(s) < 2:
        return None
    cutoff = s.index.max() - pd.Timedelta(days=days)
    prior = s[s.index <= cutoff]
    if prior.empty:
        return None
    return int(s.iloc[-1] - prior.iloc[-1])


def detect_anomalies(
    stars_wide: pd.DataFrame,
    window: int = 30,
    k: float = 5.0,
    min_gain: int = 25,
) -> pd.DataFrame:
    """Flag days where daily star gain breaks out of its rolling baseline.

    Uses rolling median + k * MAD — robust to the long tail of viral days
    that would otherwise inflate a mean/std baseline.
    """
    daily = stars_wide.diff()
    events = []
    for repo in daily.columns:
        s = daily[repo].dropna()
        if s.empty:
            continue
        med = s.rolling(window, min_periods=7).median().shift(1)
        mad = (s - med).abs().rolling(window, min_periods=7).median().shift(1)
        threshold = med + k * mad.replace(0, 1)
        flagged = s[(s > threshold) & (s >= min_gain)]
        for d, v in flagged.items():
            events.append(
                {
                    "repo": repo,
                    "date": d,
                    "stars_added": int(v),
                    "baseline": float(med.loc[d]) if pd.notna(med.loc[d]) else 0.0,
                }
            )
    return pd.DataFrame(events)


def collapse_bursts(events: pd.DataFrame, gap_days: int = 3) -> pd.DataFrame:
    if events.empty:
        return events
    bursts = []
    for repo, g in events.sort_values("date").groupby("repo"):
        current = None
        for _, row in g.iterrows():
            if current and (row["date"] - current["end"]).days <= gap_days:
                current["end"] = row["date"]
                current["stars_added"] += row["stars_added"]
                current["peak"] = max(current["peak"], row["stars_added"])
            else:
                if current:
                    bursts.append(current)
                current = {
                    "repo": repo,
                    "start": row["date"],
                    "end": row["date"],
                    "peak": int(row["stars_added"]),
                    "stars_added": int(row["stars_added"]),
                }
        if current:
            bursts.append(current)
    out = pd.DataFrame(bursts)
    out["days"] = (out["end"] - out["start"]).dt.days + 1
    return out.sort_values("start", ascending=False).reset_index(drop=True)


st.set_page_config(page_title="Modern Data Stack — Vanity Check", layout="wide")
st.title("Modern Data Stack — GitHub Vanity Check")

df = load_data()
stars = pivot(df, "stargazers_count")
latest = stars.index.max()
st.caption(f"Latest snapshot: **{latest.date()}** · {stars.shape[1]} repos · {len(stars)} days tracked")

# ---------- Leaderboard ----------
st.subheader("Leaderboard")

spark_window = stars.tail(90)
rows = []
def _latest(r):
    s = stars[r].dropna()
    return float(s.iloc[-1]) if len(s) else 0.0

for repo in sorted(stars.columns, key=lambda r: -_latest(r)):
    col = stars[repo]
    rows.append(
        {
            "repo": repo,
            "stars": int(col.iloc[-1]),
            "Δ 7d": delta(col, 7),
            "Δ 30d": delta(col, 30),
            "Δ 90d": delta(col, 90),
            "trend (90d)": spark_window[repo].dropna().tolist(),
        }
    )
board = pd.DataFrame(rows)

st.dataframe(
    board,
    hide_index=True,
    use_container_width=True,
    column_config={
        "stars": st.column_config.NumberColumn("stars", format="%d"),
        "Δ 7d": st.column_config.NumberColumn(format="%+d"),
        "Δ 30d": st.column_config.NumberColumn(format="%+d"),
        "Δ 90d": st.column_config.NumberColumn(format="%+d"),
        "trend (90d)": st.column_config.LineChartColumn("trend (90d)"),
    },
)

# ---------- Anomalies ----------
st.subheader("Anomalies — viral-spike days")
st.caption(
    "Detected with a rolling median + k·MAD baseline on daily star gains. "
    "Consecutive flagged days are collapsed into bursts."
)
c1, c2, c3 = st.columns(3)
with c1:
    sensitivity = st.slider("k (lower = more events)", 2.0, 10.0, 5.0, 0.5)
with c2:
    min_gain = st.slider("min daily stars", 5, 200, 25, 5)
with c3:
    window = st.slider("baseline window (days)", 14, 90, 30, 1)

events = detect_anomalies(stars, window=window, k=sensitivity, min_gain=min_gain)
bursts = collapse_bursts(events)

if bursts.empty:
    st.info("No anomalies at this sensitivity. Lower k or min daily stars.")
else:
    st.dataframe(
        bursts.head(50),
        hide_index=True,
        use_container_width=True,
        column_config={
            "start": st.column_config.DateColumn(format="YYYY-MM-DD"),
            "end": st.column_config.DateColumn(format="YYYY-MM-DD"),
            "peak": st.column_config.NumberColumn("peak/day", format="%d"),
            "stars_added": st.column_config.NumberColumn("total gained", format="%d"),
            "days": st.column_config.NumberColumn(format="%d"),
        },
    )

    daily = stars.diff().reset_index().melt("date", var_name="repo", value_name="daily_stars")
    base = alt.Chart(daily).mark_line(opacity=0.6).encode(
        x="date:T",
        y=alt.Y("daily_stars:Q", title="stars added / day"),
        color="repo:N",
    )
    marks_df = bursts.assign(mid=bursts["start"] + (bursts["end"] - bursts["start"]) / 2)
    marks = alt.Chart(marks_df).mark_point(size=120, filled=True, shape="triangle-down").encode(
        x="mid:T",
        y=alt.Y("peak:Q"),
        color="repo:N",
        tooltip=["repo", "start", "end", "peak", "stars_added"],
    )
    st.altair_chart((base + marks).properties(height=260), use_container_width=True)

# ---------- Explorer ----------
st.subheader("Explorer")
e1, e2, e3, e4 = st.columns([2, 2, 1, 1])
with e1:
    metric_label = st.selectbox("metric", list(METRICS.keys()))
with e2:
    repos = st.multiselect("repos", sorted(stars.columns), default=sorted(stars.columns))
with e3:
    log_scale = st.checkbox("log scale")
with e4:
    normalize = st.checkbox("normalize")

if repos:
    series = pivot(df, METRICS[metric_label])[repos]
    if normalize:
        first = series.apply(lambda s: s.dropna().iloc[0] if s.dropna().size else pd.NA)
        series = series.divide(first)
        y_title = f"{metric_label} (× day-one)"
    else:
        y_title = metric_label

    long = series.reset_index().melt("date", var_name="repo", value_name="value").dropna()
    y = alt.Y(
        "value:Q",
        title=y_title,
        scale=alt.Scale(type="log") if log_scale else alt.Scale(type="linear"),
    )
    chart = (
        alt.Chart(long)
        .mark_line()
        .encode(
            x=alt.X("date:T", title=None),
            y=y,
            color="repo:N",
            tooltip=["date:T", "repo:N", alt.Tooltip("value:Q", format=",.0f")],
        )
        .properties(height=380)
        .interactive()
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("Pick at least one repo.")
