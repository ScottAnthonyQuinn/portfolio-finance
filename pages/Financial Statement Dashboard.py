import streamlit as st
from components.Financial_Statement import render_financial_statement

st.session_state["visited_tool"] = True


render_financial_statement()
st.markdown("""
    <script>
        window.parent.document.querySelector('iframe').scrollTo(0, 0);
    </script>
""", unsafe_allow_html=True)