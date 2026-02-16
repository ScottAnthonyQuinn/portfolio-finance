import streamlit as st
from components.utils import scroll_top

scroll_top()

def render_capm_tool():

    # ---------- HEADER ----------
    st.markdown(
        "<h1 style='text-align:center;'>CAPM Calculator</h1>",
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <p style='font-size:18px;'>
            The Capital Asset Pricing Model (CAPM) estimates the expected return of an asset 
            based on its exposure to market risk.
        </p>
        <p style='font-size:16px;'>
            More information below ↓
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ---------- INPUTS ----------
    st.subheader("Input Assumptions")

    col1, col2 = st.columns(2)

    with col1:
        risk_free = st.number_input("Risk‑Free Rate (Rf) [%]", value=2.0, step=0.1)
        beta = st.number_input("Beta (β)", value=1.0, step=0.1)

    with col2:
        market_return = st.number_input("Market Return (Rm) [%]", value=8.0, step=0.1)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- CALCULATION ----------
    if st.button("Calculate Expected Return", use_container_width=True):

        rf = risk_free / 100
        rm = market_return / 100

        expected_return = rf + beta * (rm - rf)
        expected_return_percent = expected_return * 100
        market_premium = (rm - rf) * 100

        # ---------- OUTPUT ----------
        st.success(f"Expected Return: **{expected_return_percent:.2f}%**")

        st.markdown("---")

        # Premium card-style details
        st.markdown("### 📊 Details")

        st.markdown(f"""
        <div style="
            background-color:#161b22;
            padding:18px;
            border-radius:12px;
            border:1px solid #30363d;
            font-size:15px;">
            <b>Risk‑Free Rate (Rf):</b> {risk_free:.2f}%<br>
            <b>Market Return (Rm):</b> {market_return:.2f}%<br>
            <b>Market Risk Premium (Rm − Rf):</b> {market_premium:.2f}%<br>
            <b>Beta (β):</b> {beta:.2f}<br>
        </div>
        """, unsafe_allow_html=True)

    # ---------- ADDITIONAL INFORMATION ----------
    st.markdown("---")
    st.subheader("📘 Additional Information")

    with st.expander("What does CAPM do?"):
        st.markdown("""
CAPM estimates the **expected return** of an investment by linking risk and return.

It answers the question:

**“Given this asset’s risk relative to the market, what return should investors demand?”**

It is widely used in:

- Equity valuation  
- Portfolio management  
- Cost of equity calculations  
- Performance benchmarking  
""")

    with st.expander("Why is CAPM used?"):
        st.markdown("""
CAPM provides a **theoretical required return** based on:

- The time value of money (risk‑free rate)  
- Compensation for taking market risk (beta × market premium)

It helps analysts:

- Estimate the **cost of equity**  
- Compare investments with different risk levels  
- Evaluate whether an asset is **over‑ or under‑priced**  
""")

    with st.expander("How does CAPM work conceptually?"):
        st.markdown("""
CAPM is built on a simple idea:

### 1. All investments carry some level of risk  
A risk‑free asset earns a guaranteed return.  
Riskier assets must offer **more** return to compensate investors.

### 2. Not all risk matters  
Only **market risk** (systematic risk) affects expected return.  
Company‑specific risk can be diversified away.

### 3. Beta measures exposure to market movements  
If the market rises or falls, beta tells you how strongly the asset reacts.  
Higher beta → higher required return.

### 4. Investors demand extra return for taking market risk  
This extra return is the **market risk premium**.

### 5. CAPM combines these ideas  
Expected return =  risk‑free return + compensation for market risk.

---

**In short:**  
CAPM links an asset’s risk to the return investors should rationally expect.  
""")

   
