# https://github.com/streamlit/example-app-csv-wrangler

import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode


def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.

    Args:
        df (pd.DataFrame]): Source dataframe

    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        gridOptions=options.build(),
        theme="light",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection


slurp = pd.read_csv(
    "https://github.com/soobrosa/slurp/raw/main/outputs/paparazzi.csv"
)
slurp["date"] = pd.to_datetime(slurp["date"])
slurp = slurp.drop_duplicates(subset=["name", "date"], keep="last")

st.title("Modern Data Stack - GitHub Stars Over Time")

stars = slurp.pivot_table(
    index="date", columns="name", values="stargazers_count"
).dropna()
st.line_chart(stars)

metric = st.selectbox(
    "Explore another metric",
    ["forks_count", "open_issues_count", "subscribers_count"],
)
pivot = slurp.pivot_table(
    index="date", columns="name", values=metric
).dropna()
st.line_chart(pivot)

st.subheader("Snapshot table")
dates = sorted(slurp["date"].unique(), reverse=True)
selected_date = st.selectbox("Select date", dates)
filtered = slurp[slurp["date"] == selected_date].reset_index(drop=True)

selection = aggrid_interactive_table(df=filtered)

if selection and selection["selected_rows"] is not None:
    selected = selection["selected_rows"]
    if isinstance(selected, pd.DataFrame):
        selected = selected.to_dict(orient="records")
    if selected:
        st.write("You selected:")
        st.json(selected)
