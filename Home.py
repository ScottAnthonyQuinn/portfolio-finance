import streamlit as st
from components.npv_tools import render_npv_tool

# ---------------------------------------------------------
# PAGE CONFIG + REMOVE SIDEBAR
# ---------------------------------------------------------
st.set_page_config(
    page_title="Scott Quinn – Finance Portfolio",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    [data-testid="stSidebar"] {display: none !important;}
    [data-testid="stSidebarNav"] {display: none !important;}
    [data-testid="collapsedControl"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ROUTER
# ---------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"


def go_to(page):
    st.session_state.page = page
    st.rerun()


# ---------------------------------------------------------
# NPV TOOL PAGE
# ---------------------------------------------------------
if st.session_state.page == "npv":

    # ✅ FORCE TOOL PAGE TO START AT TOP
    st.markdown(
        """
        <a id="top"></a>
        <script>
            document.getElementById("top").scrollIntoView();
        </script>
        """,
        unsafe_allow_html=True
    )

    # Wider layout for tool pages
    st.markdown("""
    <style>
        .block-container {
            max-width: 1500px !important;
            padding-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Render NPV tool
    render_npv_tool(go_to)

    st.stop()


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------

# Remove anchor links
st.markdown("""
<style>
h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
    text-decoration: none !important;
    color: inherit !important;
    pointer-events: none !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# GLOBAL CSS
# ---------------------------------------------------------
st.markdown("""
<style>

body {
    background-color: #0d1117;
    color: white;
}

/* HERO SECTION */
.hero {
    padding: 70px 40px;
    border-radius: 12px;
    background: #504C50;
    color: white;
    text-align: center;
}

.hero h1 {
    font-size: 3.2rem;
    margin-bottom: 5px;
}

.hero h3 {
    font-size: 1.4rem;
    color: #58a6ff;
    margin-bottom: 20px;
}

.hero p {
    font-size: 1.15rem;
    max-width: 650px;
    margin: auto;
    opacity: 0.95;
}

/* ABOUT */
.about {
    max-width: 900px;
    margin: auto;
    text-align: center;
    color: white;
    font-size: 1.05rem;
    line-height: 1.6;
}

/* TOOL BUTTONS */
div.stButton > button {
    border: 1px solid #30363d !important;
    border-radius: 14px !important;
    padding: 26px 20px !important;
    text-align: center !important;
    background-color: #161b22 !important;
    height: 200px !important;
    width: 100% !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    color: #58a6ff !important;
    transition: 0.25s ease !important;
}

div.stButton > button:hover {
    transform: translateY(-6px);
    border-color: #58a6ff !important;
    box-shadow: 0 6px 18px rgba(0,0,0,0.4);
}

/* FOOTER */
.footer {
    text-align: center;
    padding: 20px;
    color: #8b949e;
    margin-top: 50px;
    font-size: 0.9rem;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HERO SECTION
# ---------------------------------------------------------
st.markdown("""
<div class="hero">
    <h1>Scott Quinn</h1>
    <h3>Business Controller & Accounting</h3>
    <p>
        Welcome to my finance portfolio. I have created a collection of tools and frameworks
        that reflect the analytical, structured, and decision-focused work done in modern
        business controlling and accounting roles.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# ABOUT SECTION
# ---------------------------------------------------------
st.markdown("<div style='height:45px;'></div>", unsafe_allow_html=True)

st.markdown("""
<div class="about">
<h2>About Me</h2>

I’m Scott, and I’m building a career in <strong>business controlling and accounting</strong>.<br><br>

My focus is on understanding how organisations create value, how financial performance is measured,
and how structured analysis supports better decisions.<br><br>

I am also interested in how <strong><span style="color:#00cc66;">SUSTAINABILITY</span></strong>
affects financial decision making in modern business.<br><br>

This portfolio brings together tools and frameworks commonly used in:<br><br>

• Business control<br>
• Financial planning & analysis (FP&A)<br>
• Investment evaluation<br>
• Performance measurement<br>
• Management accounting<br><br>

Each tool reflects the type of work done in modern finance roles and concepts I have been developing
through my Bachelor program.
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# TOOLS HEADER
# ---------------------------------------------------------
st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;'>Financial Tools</h2>", unsafe_allow_html=True)
st.markdown("<div style='height:25px;'></div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# TOOL DEFINITIONS
# ---------------------------------------------------------
tools = [
    ("📊", "NPV / IRR / Payback Calculator", "npv", False),
    ("💰", "DCF Valuation Model", None, True),
    ("📈", "Financial Ratios Dashboard", None, True),
    ("📉", "CAPM Calculator", None, True),
    ("🏦", "Bond Pricing Tool", None, True),
    ("🧮", "WACC Calculator", None, True),
]

cols = st.columns(3)

# ---------------------------------------------------------
# TOOL GRID
# ---------------------------------------------------------
for i, (icon, name, route, coming_soon) in enumerate(tools):

    with cols[i % 3]:

        if coming_soon:
            st.markdown(f"""
            <div style="
                border: 1px solid #30363d;
                border-radius: 14px;
                padding: 26px;
                height: 200px;
                background-color: #161b22;
                text-align: center;
                margin-bottom: 30px;
            ">
                <div style="font-size: 2.6rem;">{icon}</div>
                <div style="font-size: 1.1rem; font-weight: 600; color: #58a6ff;">
                    {name}
                </div>
                <p style="color: #8b949e;">Coming soon</p>
            </div>
            """, unsafe_allow_html=True)

        else:
            if st.button(f"{icon}   {name}", use_container_width=True):
                go_to(route)

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown("""
<div class="footer">
    Thank you for your time ❤️
</div>
""", unsafe_allow_html=True)
