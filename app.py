import streamlit as st
import bcrypt
from supabase import create_client
from dotenv import load_dotenv
import os
import webbrowser

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

looker_url = "https://lookerstudio.google.com/reporting/1edc88d0-1c83-4b46-9f9b-a4672f0bd062"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.set_page_config(page_title="Dashboard Login", layout="centered")

def redirect(url):
    st.components.v1.html(
        f"""
        <script>
            window.location.replace("{url}");
        </script>
        """,
        height=0
    )
    st.stop()

def verify_password(input_password):
    response = supabase.table("bdm_auth") \
        .select("password") \
        .eq("is_active", True) \
        .execute()

    if not response.data:
        return False

    for row in response.data:
        if bcrypt.checkpw(
            input_password.encode(),
            row["password"].encode()
        ):
            return True
    return False

st.title("🔐 Login Dashboard")

password = st.text_input("Password", type="password")

if st.button("Login"):
    if verify_password(password):
        st.success("Login berhasil, mengalihkan ke dashboard...")
        webbrowser.open_new_tab(looker_url)
    else:
        st.error("Password salah")
