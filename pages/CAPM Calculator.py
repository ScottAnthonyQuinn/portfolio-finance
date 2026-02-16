import streamlit as st
from components.CAPM import render_capm_tool

st.session_state["visited_tool"] = True


render_capm_tool()
st.markdown("""
    <script>
        window.parent.document.querySelector('iframe').scrollTo(0, 0);
    </script>
""", unsafe_allow_html=True)
