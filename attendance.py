import streamlit as st
import pandas as pd
from database import supabase
from auth import login

if not login():
    st.stop()

st.title("Weekly Meeting Attendance")
st.write(f"Logged in as: {st.session_state.username}")
if st.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
year = st.selectbox(
    "Select year",
    options=["- - -", "2026", "2027", "2028", "2029", "2030"]
)

month = st.selectbox(
    "Select month",
    options=[
        "- - -",
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]
)

type_ = st.selectbox(
    "Select type",
    options=["- - -", "Midweek", "Weekend"]
)

week = st.selectbox(
    "Select week",
    options=["- - -",1,2,3,4,5]
)

attendance = st.number_input("Enter attendance", min_value=0, step=1)
attendance = int(attendance)

submit_button = st.button("Submit")

if submit_button:
    if year != "- - -" and month != "- - -" and type != "- - -" and week != "- - -":
        supabase.table("Attendance") \
            .delete() \
            .eq("user_id", st.session_state.user_id)\
            .eq("year", int(year)) \
            .eq("month", month) \
            .eq("type", type_) \
            .eq("week", int(week)) \
            .execute()
        
        try:
            supabase.table("Attendance").upsert(
                {
                    "user_id": st.session_state.user_id,
                    "year": int(year),
                    "month": month,
                    "type": type_,
                    "week": int(week),
                    "attendance": int(attendance)    
                },
                on_conflict="user_id,year,month,week,type"
            ).execute()
            st.success("Attendance saved successfully!")
        except Exception:
            st.error("Something went wrong while saving attendance.")

st.header("View Attendance")

display_year = st.selectbox("Select year to view", ["- - -", "2026", "2027", "2028", "2029", "2030"], key="view_year")
display_month = st.selectbox(
    "Select month to view",
    [
        "- - -",
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ],
    key="view_month"
)

display_button = st.button("Show Attendance")

if display_button:
    if display_year != "- - -" and display_month != "- - -":
        response = supabase.table("Attendance")\
            .select("*")\
            .eq("user_id", st.session_state.user_id)\
            .eq("year", int(display_year))\
            .eq("month", display_month)\
            .execute()
        
        data = response.data
        if data:
            df = pd.DataFrame(data)
            pivot_df = df.pivot(index="type", columns="week", values="attendance").reindex(["Midweek", "Weekend"])
            pivot_df = pivot_df.reindex(columns=[1, 2, 3, 4, 5])
            pivot_df.columns = [f"Week {c}" for c in pivot_df.columns]
            calc_df = pivot_df.fillna(0).apply(pd.to_numeric, errors='coerce')
            pivot_df = pivot_df.fillna(0).astype(int)
            pivot_df["Total"] = calc_df.sum(axis=1).astype(int)
            pivot_df["Average"] = calc_df.replace(0, pd.NA).mean(axis=1).round().fillna(0).astype(int)
            st.subheader(f"Attendance for {display_month} {display_year}")
            st.dataframe(pivot_df.fillna("-"))
        else:
            st.info("No attendance for this month yet.")