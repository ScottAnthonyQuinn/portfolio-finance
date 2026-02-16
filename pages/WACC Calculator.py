import streamlit as st
from components.wacc import render_wacc_tool

st.session_state["visited_tool"] = True


render_wacc_tool()

st.markdown("""
    <script>
        window.parent.document.querySelector('iframe').scrollTo(0, 0);
    </script>
""", unsafe_allow_html=True)