import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="EDA + Analytics Dashboard", layout="wide")
st.title("🎬 Movie Analytics Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload your CSV dataset", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("Dataset uploaded successfully!")

    # --- Descriptive Analysis ---
    st.header("📊 Descriptive Analysis (What happened?)")
    st.write("Dataset Preview")
    st.write(df.head())

    st.write("Summary Statistics")
    st.write(df.describe(include="all"))

    if "genre" in df.columns:
        st.write("Genre Distribution")
        st.bar_chart(df["genre"].value_counts())

    # --- Diagnostic Analysis ---
    st.header("🔍 Diagnostic Analysis (Why did it happen?)")
    st.write("Correlation Heatmap")
    fig, ax = plt.subplots()
    sns.heatmap(df.select_dtypes(include=["number"]).corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    if "genre" in df.columns and "rating" in df.columns:
        st.write("Ratings by Genre")
        fig, ax = plt.subplots()
        sns.boxplot(x="genre", y="rating", data=df, ax=ax)
        plt.xticks(rotation=90)
        st.pyplot(fig)

    # --- Predictive Analysis ---
    st.header("🔮 Predictive Analysis (What will happen?)")
    if "budget" in df.columns and "revenue" in df.columns:
        X = df[["budget"]].fillna(0)
        y = df["revenue"].fillna(0)

        if not X.empty and not y.empty:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = LinearRegression()
            model.fit(X_train, y_train)

            budget_input = st.number_input("Enter Budget (USD)", min_value=0, step=1000000)
            if budget_input > 0:
                predicted_revenue = model.predict([[budget_input]])[0]
                st.success(f"Predicted Revenue: ${predicted_revenue:,.0f}")
    else:
        st.warning("Dataset must contain 'budget' and 'revenue' columns for prediction.")

    # --- Prescriptive Analysis ---
    st.header("🎯 Prescriptive Analysis (What should we do?)")
    required_cols = {"budget", "revenue"}
    if required_cols.issubset(df.columns):
        df = df[df["budget"] > 0].copy()
        df["ROI"] = df["revenue"] / df["budget"]

        if not df["ROI"].empty:
            if "genre" in df.columns:
                best_genre = df.groupby("genre")["ROI"].mean().idxmax()
                st.write(f"✅ Recommended Genre for Investment: **{best_genre}**")

            if "year" in df.columns:
                df["decade"] = (df["year"] // 10) * 10
                best_decade = df.groupby("decade")["ROI"].mean().idxmax()
                st.write(f"💡 Suggested Decade with Best ROI: **{best_decade}s**")

            st.write("🏆 Top 5 Movies by ROI")
            if "title" in df.columns:
                st.write(df[["title", "ROI"]].sort_values(by="ROI", ascending=False).head())
            else:
                st.write(df[["ROI"]].sort_values(by="ROI", ascending=False).head())
        else:
            st.warning("ROI values could not be calculated — check your budget/revenue data.")
    else:
        st.warning("Dataset must contain 'budget' and 'revenue' columns for prescriptive analysis.")

else:
    st.info("Please upload a CSV file to begin analysis.")
