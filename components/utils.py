import streamlit as st
import streamlit.components.v1 as components

def scroll_top():
    components.html(
        """
        <script>
            window.parent.scrollTo(0, 0);
        </script>
        """,
        height=0,
    )
