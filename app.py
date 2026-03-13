##-----  app.py

import streamlit as st
from lib.supabase_client import get_supabase

st.set_page_config(
    page_title="Lutine AV Requisition",
    layout="wide"
)

sb = get_supabase()

st.title("Lutine AV Requisition")

st.markdown(
    """
    This tool supports AV requests, inventory allocation,
    shipping, returns, and maintenance for Lutine-managed meetings.
    """
)

# --- Auth sanity check (mirrors calendar behavior) ---
user = sb.auth.get_user()

if not user:
    st.warning("Please log in to continue.")
    st.stop()

st.success(f"Logged in as {user.user.email}")

# --- Placeholder navigation ---
st.markdown("Use the navigation on the left to request or manage AV.")
