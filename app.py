import time

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Watchlist Explorer", layout="wide")
st.title("Watchlist Explorer")
st.caption("Six tech stocks, weekly, 2018-2019. Indexed to 1.00 on 2018-01-01.")


@st.cache_data
def load_data():
    time.sleep(2)
    wide = px.data.stocks()
    wide["date"] = pd.to_datetime(wide["date"])
    long = wide.melt(id_vars="date", var_name="ticker", value_name="price")
    long = long.sort_values(["ticker", "date"]).reset_index(drop=True)
    long["indexed"] = long.groupby("ticker")["price"].transform(
        lambda s: s / s.iloc[0]
    )
    return long


df = load_data()

st.subheader("Performance indexed to 1.00")
fig = px.line(
    df,
    x="date",
    y="indexed",
    color="ticker",
    title="Indexed stock performance",
)
fig.update_yaxes(title="Indexed value")
fig.update_xaxes(title="Date")
st.plotly_chart(fig, use_container_width=True)

st.dataframe(df.head(10))
