# This creates the page for displaying data visualizations.

import streamlit as st
import json
import pandas as pd
import os
import plotly.express as px




# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json


st.title("Candy Bar Visuals")

# PART 1: Load the JSON file and display it as a table

with open("data.json") as f:
    candy_data = json.load(f)

candy_df = pd.DataFrame(candy_data["candy_bars"])

st.dataframe(candy_df)




st.subheader("Calories by Candy Bar")
st.write("This chart shows calories for each candy bar.")

st.bar_chart(
    candy_df,
    x="name",
    y="calories"
)




st.subheader("Candy Bar Weight vs. Calories")
st.write("Choose a manufacturer to filter the chart.")

makers = ["All"] + sorted(
    candy_df["maker"].unique().tolist()
)

if "selected_maker" not in st.session_state:
    st.session_state.selected_maker = "All"

st.selectbox(
    "Select a Manufacturer",
    options=makers,
    key="selected_maker"
)

if st.session_state.selected_maker == "All":
    filtered_candy = candy_df
else:
    filtered_candy = candy_df[
        candy_df["maker"] == st.session_state.selected_maker
    ]

avg_cal = filtered_candy["calories"].mean()
med_cal = filtered_candy["calories"].median()

if "prev_avg" not in st.session_state:
    st.session_state["prev_avg"] = avg_cal
if "prev_med" not in st.session_state:
    st.session_state["prev_med"] = med_cal

col1, col2 = st.columns(2)
col1.metric("Mean Calories", round(avg_cal, 1),
            delta=round(avg_cal - st.session_state["prev_avg"], 1))
col2.metric("Median Calories", round(med_cal, 1),
            delta=round(med_cal - st.session_state["prev_med"], 1))

st.session_state["prev_avg"] = avg_cal
st.session_state["prev_med"] = med_cal

scatter_chart = px.scatter(
    filtered_candy,
    x="grams",
    y="calories",
    color="maker",
    hover_name="name",
    title="Candy Bar Weight vs. Calories",
    labels={
        "grams": "Weight (grams)",
        "calories": "Calories",
        "maker": "Manufacturer"
    }
)

st.plotly_chart(scatter_chart, use_container_width=True)




# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---





st.header("🍬Candy Bar Survey Results🍬")


if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:

    survey_df = pd.read_csv("data.csv")
    survey_df["Category"] = survey_df["Category"].str.strip().str.title()
    survey_df["Value"] = pd.to_numeric(
        survey_df["Value"], errors="coerce"
    )

    survey_df = survey_df.dropna(
        subset=["Category", "Value"]
    )

    survey_df = survey_df[
        survey_df["Value"].between(1, 10)
    ]

    if not survey_df.empty:


        st.subheader("Average Rating by Candy Bar")
        st.write(
            "This chart shows the average rating "
            "for each candy bar."
        )

        average_ratings = (
            survey_df.groupby("Category", as_index=False)["Value"]
            .mean()
        )

        st.bar_chart(
            average_ratings,
            x="Category",
            y="Value",
            x_label="Candy Bar",
            y_label="Average Rating (1-10)"
        )

        
        st.subheader("Candy Bar Rating Distribution")
        st.write(
            "Choose which candy bars to include "
            "in the pie chart."
        )

        candy_options = sorted(
            survey_df["Category"].unique().tolist()
        )

           
        if "csv_selected_candies" not in st.session_state:
            st.session_state.csv_selected_candies = candy_options

        st.session_state.csv_selected_candies = [
            candy for candy in st.session_state.csv_selected_candies
            if candy in candy_options
        ]

        st.multiselect(
            "Select Candy Bars",
            options=candy_options,
            key="csv_selected_candies"
        )

        filtered_df = survey_df[
            survey_df["Category"].isin(
                st.session_state.csv_selected_candies
            )
        ]

        if not filtered_df.empty:

            counts = (
                filtered_df["Category"]
                .value_counts()
                .reset_index()
            )

            counts.columns = ["Candy Bar", "Responses"]


            pie_chart = px.pie(
                counts,
                names="Candy Bar",
                values="Responses",
                title="Survey Responses by Candy Bar"
            )

            st.plotly_chart(
                pie_chart,
                use_container_width=True
            )

        else:
            st.info("Select at least one candy bar.")

    else:
        st.warning("No valid survey ratings found.")

else:
    st.info("Submit survey responses to see the charts.")
