from st_aggrid import AgGrid, GridOptionsBuilder
import streamlit as st

def render_interactive_table(df):
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False)
    gridOptions = gb.build()
    
    AgGrid(
        df,
        gridOptions=gridOptions,
        theme='alpine', # Premium dark theme available: 'alpine-dark'
        height=500,
        fit_columns_on_grid_load=True
    )
