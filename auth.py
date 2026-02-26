import streamlit as st
from database import supabase

def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:

        st.title("Weekly Meeting Attendance")
        
        st.divider()
        
        st.text("Welcome to this website. Please note that it is a non-commercial, private platform, and account registration is not available to the public. All user accounts are created directly by the site owner. If you wish to access the services offered here, you must contact the owner to request an account. This website is intended solely for the use of the owner and trusted individuals known personally by the owner. This is an unofficial tool created by an individual and is not affiliated with or endorsed by an organization.")

        st.divider()

        st.header("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        login_button = st.button("Login")

        if login_button:

            response = supabase.table("Users") \
                .select("*") \
                .eq("username", username) \
                .eq("password", password) \
                .execute()

            if response.data:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.user_id = response.data[0]["id"]
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid username or password")

        return False

    return True