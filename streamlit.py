import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

slurp = pd.read_csv(
    "https://github.com/soobrosa/slurp/raw/main/outputs/paparazzi.csv"
)

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
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="light",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection


slurp = pd.read_csv(
    "https://github.com/soobrosa/slurp/raw/main/outputs/paparazzi.csv"
)

selection = aggrid_interactive_table(df=slurp)

if selection:
    st.write("You selected:")
    st.json(selection["selected_rows"])
