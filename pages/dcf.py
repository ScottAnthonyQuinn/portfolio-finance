import streamlit as st
from components.DCF import render_dcf_tool

st.session_state["visited_tool"] = True

render_dcf_tool()

st.markdown("""
    <script>
        window.parent.document.querySelector('iframe').scrollTo(0, 0);
    </script>
""", unsafe_allow_html=True)
