import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Scott Quinn – Finance Portfolio",
    page_icon="💼",
    layout="wide"
)

# --- REMOVE HEADER ANCHOR LINKS ---
st.markdown("""
<style>
h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
    text-decoration: none !important;
    color: inherit !important;
    pointer-events: none !important;
}
</style>
""", unsafe_allow_html=True)

# --- CUSTOM CSS ---
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

/* ABOUT ME */
.about {
    max-width: 900px;
    margin: auto;
    text-align: center;
    color: white;
}

/* TOOL CARDS */
.tool-card {
    border: 1px solid #30363d;
    border-radius: 14px;
    padding: 26px 20px;
    text-align: center;
    transition: 0.25s ease;
    background-color: #161b22;
    height: 200px;
    margin-bottom: 30px;
    color: white;
}

.tool-card:hover {
    transform: translateY(-6px);
    border-color: #58a6ff;
    box-shadow: 0 6px 18px rgba(0,0,0,0.4);
}

.tool-icon {
    font-size: 2.8rem;
    margin-bottom: 12px;
}

.tool-name {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 6px;
    color: #58a6ff;
}

/* FOOTER */
.footer {
    text-align: center;
    padding: 20px;
    color: #8b949e;
    margin-top: 40px;
    font-size: 0.9rem;
}

</style>
""", unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown(
    """
<div class="hero">
    <h1>Scott Quinn</h1>
    <h3>Business Controller & Accounting</h3>
    <p>
        Welcome to my finance portfolio. I have created a collection of tools and frameworks that reflect the analytical,
        structured, and decision‑focused work done in modern business controlling and accounting roles.
    </p>
</div>
""",
    unsafe_allow_html=True
)


# --- ABOUT ME (FIXED: NO INDENTATION) ---
st.markdown(
"""
<div class="about">
<h2>About Me</h2>

I’m Scott, and I’m building a career in <strong>business controlling and accounting</strong>.<br><br>
My focus is on understanding how organisations create value, how financial performance is measured,
and how structured analysis supports better decisions.<br><br>
I am also instrested in seeing how <strong><span style="color:#00cc66;">SUSTAINABILITY</span></strong> affects the pure "financial value" decision making in modern business<br><br>

This portfolio brings together tools and frameworks commonly used in:<br><br>
• Business control<br>
• Financial planning & analysis (FP&A)<br>
• Investment evaluation<br>
• Performance measurement<br>
• Management accounting<br><br>

Each tool reflects the type of work done in modern finance roles and that I have been learning in my Bachelor program.<br> These include: analysing outcomes, evaluating alternatives, and supporting management with clear, decision‑ready insight.
</div>
""",
    unsafe_allow_html=True
)
# --- SPACING BEFORE TOOLS ---
st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)

# --- TOOLS SECTION ---
st.markdown("<h2 style='text-align:center;'>Financial Tools</h2>", unsafe_allow_html=True)
st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

tools = [
    ("📊", "NPV Calculator"),
    ("💰", "DCF Valuation Model"),
    ("📈", "Financial Ratios Dashboard"),
    ("📉", "CAPM Calculator"),
    ("🏦", "Bond Pricing Tool"),
    ("🧮", "WACC Calculator"),
]

cols = st.columns(3)

for i, (icon, name) in enumerate(tools):
    with cols[i % 3]:
        st.markdown(
f"""
<div class="tool-card">
    <div class="tool-icon">{icon}</div>
    <div class="tool-name">{name}</div>
    <p style="color: #8b949e;">Coming soon</p>
</div>
""",
            unsafe_allow_html=True
        )

import streamlit as st
import requests
import time

API_KEY = "re_CX2LaATW_5hPbtxjA2Cf45BaHSjeN1GRG"

st.markdown("<h2 style='text-align:center; margin-top:40px;'>Contact Me</h2>", unsafe_allow_html=True)

# --- SPAM PROTECTION SETTINGS ---
RATE_LIMIT_SECONDS = 30  # user must wait this long before sending again

# --- ANIMATION HTML ---
def animated_message(text):
    return f"""
        <div style='text-align:center; margin-top:30px;'>
            <div style="
                font-size: 60px;
                color: #4CAF50;
                animation: pop 0.4s ease-out;
            ">✔</div>
            <div style="
                font-size: 22px;
                margin-top: 10px;
                animation: fadein 1s ease-in;
            ">
                {text}
            </div>
        </div>

        <style>
        @keyframes pop {{
            0% {{ transform: scale(0.5); opacity: 0; }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}
        @keyframes fadein {{
            0% {{ opacity: 0; }}
            100% {{ opacity: 1; }}
        }}
        </style>
    """

# --- RATE LIMIT CHECK ---
last_sent = st.session_state.get("last_sent_time", None)
if last_sent and time.time() - last_sent < RATE_LIMIT_SECONDS:
    st.markdown(animated_message("Please wait a moment before sending another message."), unsafe_allow_html=True)
    st.stop()

# --- IF MESSAGE ALREADY SENT ---
if st.session_state.get("message_sent", False):
    st.markdown(animated_message("Your message has been sent! I'll get back to you as soon as I can."), unsafe_allow_html=True)
    st.stop()

# --- CONTACT FORM ---
with st.form("contact_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Your Message")

    # PURE HTML HONEYPOT — invisible, no Streamlit widget
    st.markdown("""
        <input type="text" id="botfield" name="botfield" style="display:none;">
        <script>
            document.getElementById("botfield").value = "";
        </script>
    """, unsafe_allow_html=True)

    submitted = st.form_submit_button("Send Message")

    if submitted:

        # Retrieve honeypot value via JS injection
        bot_value = st.session_state.get("botfield", "")

        # SPAM CHECK: if bot_value is not empty → bot
        if bot_value.strip() != "":
            st.markdown(animated_message("Your message has been sent!"), unsafe_allow_html=True)
            st.stop()

        if not name or not email or not message:
            st.error("Please fill in all fields.")
        else:
            url = "https://api.resend.com/emails"
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            payload_to_you = {
                "from": "Scott Quinn <onboarding@resend.dev>",
                "to": ["scott-quinn1@outlook.com"],
                "subject": f"New message from {name}",
                "html": f"""
                    <h2>New Contact Form Submission</h2>
                    <p><strong>Name:</strong> {name}</p>
                    <p><strong>Email:</strong> {email}</p>
                    <p><strong>Message:</strong></p>
                    <p>{message}</p>
                    <hr>
                    <p>This message was sent from your portfolio website.</p>
                """
            }

            r1 = requests.post(url, json=payload_to_you, headers=headers)

            if r1.status_code == 200:
                st.session_state["message_sent"] = True
                st.session_state["last_sent_time"] = time.time()
                st.rerun()
            else:
                st.error("Something went wrong. Please try again later.")



# --- FOOTER ---
st.markdown(
    """
<div class="footer">
    Thank You for you time ❤️ 
</div>
""",
    unsafe_allow_html=True
)
