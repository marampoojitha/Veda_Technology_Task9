from pathlib import Path
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "iris.csv"

st.set_page_config(page_title="Task 9 | Iris Statistics", page_icon="🌸", layout="wide")
st.title("🌸 Task 9 — Iris Descriptive Statistics")
st.caption("Python • Pandas • Excel | Mean, median, mode, standard deviation and percentiles")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

try:
    df = load_data()
except Exception as exc:
    st.error("Could not load data/iris.csv. Make sure the included CSV remains in the data folder.")
    st.exception(exc)
    st.stop()

numeric = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
c1, c2, c3 = st.columns(3)
c1.metric("Observations", f"{len(df):,}")
c2.metric("Species", str(df["species"].nunique()))
c3.metric("Missing cells", f"{int(df.isna().sum().sum()):,}")

st.subheader("Summary statistics")
selected = st.multiselect("Choose measurements", numeric, default=numeric)
if selected:
    rows = []
    for col in selected:
        s = df[col].dropna()
        modes = s.mode()
        rows.append({
            "Column": col.replace("_", " ").title(), "Count": int(s.count()),
            "Missing": int(df[col].isna().sum()), "Mean": s.mean(),
            "Median": s.median(), "Mode": ", ".join(f"{x:g}" for x in modes.tolist()),
            "Standard deviation": s.std(), "Min": s.min(),
            "25th percentile": s.quantile(.25), "50th percentile": s.quantile(.5),
            "75th percentile": s.quantile(.75), "Max": s.max(),
            "IQR": s.quantile(.75) - s.quantile(.25),
        })
    st.dataframe(pd.DataFrame(rows).round(3), use_container_width=True, hide_index=True)

left, right = st.columns(2)
with left:
    st.subheader("Measurement distribution")
    col = st.selectbox("Select a measurement", numeric)
    fig, ax = plt.subplots()
    ax.hist(df[col].dropna(), bins=15, edgecolor="black")
    ax.set_xlabel(col.replace("_", " ").title() + " (cm)")
    ax.set_ylabel("Count")
    ax.set_title("Distribution of " + col.replace("_", " ").title())
    st.pyplot(fig)
    plt.close(fig)
with right:
    st.subheader("Average measurements by species")
    col2 = st.selectbox("Measurement to compare", numeric, index=2)
    means = df.groupby("species")[col2].mean()
    fig, ax = plt.subplots()
    means.plot(kind="bar", ax=ax)
    ax.set_xlabel("Species")
    ax.set_ylabel("Average (cm)")
    ax.set_title(col2.replace("_", " ").title() + " by species")
    ax.tick_params(axis="x", rotation=15)
    st.pyplot(fig)
    plt.close(fig)

st.subheader("Species-wise summary")
st.dataframe(df.groupby("species")[numeric].agg(["mean", "median", "std"]).round(3), use_container_width=True)
st.subheader("Dataset preview")
st.dataframe(df.head(15), use_container_width=True)
st.info("Compare mean with median to look for possible skew. Standard deviation measures spread, and the 25th–75th percentile interval contains the middle 50% of observations.")
