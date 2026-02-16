import streamlit as st
from components.bond_tool import render_bond_tool

st.set_page_config(page_title="Bond Pricing Tool")

st.session_state["visited_tool"] = True

render_bond_tool()
