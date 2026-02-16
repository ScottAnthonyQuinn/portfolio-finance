import streamlit as st


def render_bond_tool():

    # ---------------------------------------------------------
    # PAGE CONFIG
    # ---------------------------------------------------------
    st.set_page_config(
        page_title="Bond Pricing Tool",
        page_icon="🏦",
        layout="wide"
    )

    # ---------------------------------------------------------
    # CLEAN PROFESSIONAL STYLING
    # ---------------------------------------------------------
    st.markdown("""
    <style>

    /* Background */
    .stApp {
        background-color: #0d1117;
        color: white;
        font-family: "Inter", sans-serif;
    }

    /* Titles */
    h1, h2, h3 {
        font-weight: 700;
        color: #58a6ff;
    }

    /* Input rounding */
    div[data-baseweb="input"] {
        border-radius: 10px !important;
    }

    /* Metric card */
    div[data-testid="stMetric"] {
        background-color: #161b22;
        padding: 1.3rem;
        border-radius: 16px;
        border: 1px solid #30363d;
        text-align: center;
    }

  
    }

    summary {
        font-size: 1.05rem;
        font-weight: 600;
        color: #58a6ff;
        cursor: pointer;
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # HEADER
    # ---------------------------------------------------------
    st.title("🏦 Bond Pricing Calculator")

    st.markdown("""
    This tool calculates the **fair value of a bond** by discounting its future cash flows:

    - Coupon payments  
    - Face value repayment at maturity  

    Bond pricing is fundamental in **fixed income valuation** and **interest rate risk analysis**.

    **More information below ↓**
    """)

    st.divider()

    # ---------------------------------------------------------
    # INPUT SECTION
    # ---------------------------------------------------------
    st.subheader("📌 Bond Assumptions")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Bond Terms")
        face_value = st.number_input(
            "Face Value (F)",
            min_value=0.0,
            value=1000.0,
            step=100.0
        )

        coupon_rate = st.number_input(
            "Coupon Rate (% per year)",
            min_value=0.0,
            value=5.0,
            step=0.25
        ) / 100

    with col2:
        st.markdown("### Yield & Maturity")
        yield_rate = st.number_input(
            "Yield to Maturity (YTM, %)",
            min_value=0.0,
            value=4.0,
            step=0.25
        ) / 100

        years = st.number_input(
            "Years to Maturity",
            min_value=1,
            value=10,
            step=1
        )

    with col3:
        st.markdown("### Payment Frequency")
        frequency = st.selectbox(
            "Coupon Frequency",
            ["Annual", "Semi-Annual", "Quarterly"]
        )

        freq_map = {"Annual": 1, "Semi-Annual": 2, "Quarterly": 4}
        f = freq_map[frequency]

    # ---------------------------------------------------------
    # CALCULATIONS
    # ---------------------------------------------------------
    coupon_payment = (face_value * coupon_rate) / f
    total_periods = int(years * f)
    period_yield = yield_rate / f

    price = 0
    for t in range(1, total_periods + 1):
        price += coupon_payment / ((1 + period_yield) ** t)

    price += face_value / ((1 + period_yield) ** total_periods)

    # ---------------------------------------------------------
    # OUTPUT RESULTS
    # ---------------------------------------------------------
    st.divider()
    st.subheader("📊 Bond Valuation Result")

    st.metric(
        label="Fair Bond Price",
        value=f"${price:,.2f}"
    )

    st.markdown("### Pricing Breakdown")

    st.markdown(f"""
    | Component | Value |
    |----------|------|
    | Coupon Payment (C) | **${coupon_payment:,.2f}** |
    | Total Periods (N) | **{total_periods}** |
    | Periodic Yield (y) | **{period_yield*100:.3f}%** |
    """)

    # ---------------------------------------------------------
    # INFO SECTION (BOTTOM)
    # ---------------------------------------------------------
    st.divider()
    st.subheader("📘 Additional Information")

    # --- Expander 1: Bond Pricing Formula ---
    with st.expander("What is the Bond Pricing Formula?"):

        st.markdown("""
        A bond is worth the **present value of its future cash flows**:

        - Coupon payments  
        - Face value repayment at maturity  
        """)

        st.latex(r"""
        P = \sum_{t=1}^{N}\frac{C}{(1+y)^t}
        + \frac{F}{(1+y)^N}
        """)

        st.markdown("""
        **Where:**

        - **P** = Bond price today  
        - **C** = Coupon payment per period  
        - **F** = Face value repaid at maturity  
        - **y** = Yield per period  
        - **N** = Total number of periods  
        """)

    # --- Expander 2: Yield Relationship ---
    with st.expander("Why does yield affect bond price?"):

        st.markdown("""
        Bond prices move **inversely** to yields:

        - If yields rise → future cash flows are discounted more → **price falls**  
        - If yields fall → future cash flows are discounted less → **price rises**  

        This is the foundation of **interest rate risk**, duration, and fixed-income portfolio management.
        """)




# Run directly
if __name__ == "__main__":
    render_bond_tool()
