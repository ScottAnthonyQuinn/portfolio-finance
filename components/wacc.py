import streamlit as st


def render_wacc_tool():

    # ---------------------------------------------------------
    # PAGE SETUP
    # ---------------------------------------------------------
    st.set_page_config(
        page_title="WACC Calculator",
        page_icon="📉",
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
        color: white !important;;
    }

    /* Input rounding */
    div[data-baseweb="input"] {
        border-radius: 10px !important;
    }

    /* Metric card */
    div[data-testid="stMetric"] {
        background-color: #11142E !important;
        padding: 1.3rem;
        border-radius: 16px;
        border: 1px solid #30363d;
        text-align: center;
    }

    summary {
        font-size: 1.05rem;
        font-weight: 600;
        color: white !important;;
        cursor: pointer;
    }

    </style>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------------
    # HEADER
    # ---------------------------------------------------------
    st.title("📉 WACC Calculator")

    st.markdown("""
    The **Weighted Average Cost of Capital (WACC)** is the blended required return  
    a company must earn to satisfy both:

    - **Equity investors**
    - **Debt lenders**

    It is commonly used as the **discount rate** in valuation models such as DCF.

    **More information below ↓**
    """)

    st.divider()

    # ---------------------------------------------------------
    # INPUT SECTION
    # ---------------------------------------------------------
    st.subheader("📌 Input Assumptions")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Equity")
        equity_value = st.number_input(
            "Market Value of Equity (E)",
            min_value=0.0,
            value=1_000_000.0,
            step=50_000.0
        )

        cost_of_equity = st.number_input(
            "Cost of Equity (Re, %)",
            min_value=0.0,
            value=10.0,
            step=0.25
        ) / 100

    with col2:
        st.markdown("### Debt")
        debt_value = st.number_input(
            "Market Value of Debt (D)",
            min_value=0.0,
            value=500_000.0,
            step=50_000.0
        )

        cost_of_debt = st.number_input(
            "Cost of Debt (Rd, %)",
            min_value=0.0,
            value=5.0,
            step=0.25
        ) / 100

    with col3:
        st.markdown("### Taxes")
        tax_rate = st.number_input(
            "Corporate Tax Rate (T, %)",
            min_value=0.0,
            max_value=50.0,
            value=20.0,
            step=1.0
        ) / 100

    # ---------------------------------------------------------
    # CALCULATIONS
    # ---------------------------------------------------------
    total_value = equity_value + debt_value

    if total_value > 0:
        weight_equity = equity_value / total_value
        weight_debt = debt_value / total_value
    else:
        weight_equity = 0
        weight_debt = 0

    after_tax_cost_of_debt = cost_of_debt * (1 - tax_rate)

    wacc = (weight_equity * cost_of_equity) + (weight_debt * after_tax_cost_of_debt)

    # ---------------------------------------------------------
    # RESULTS
    # ---------------------------------------------------------
    st.divider()
    st.subheader("📊 Results")

    st.metric(
        label="Weighted Average Cost of Capital (WACC)",
        value=f"{wacc * 100:.2f}%"
    )

    st.markdown("### Capital Structure Breakdown")

    st.markdown(f"""
    | Component | Value |
    |----------|------|
    | Equity Weight (E/V) | **{weight_equity:.2f}** |
    | Debt Weight (D/V) | **{weight_debt:.2f}** |
    | After-Tax Cost of Debt | **{after_tax_cost_of_debt*100:.2f}%** |
    """)

    # ---------------------------------------------------------
    # INFORMATION SECTION (ALL TOGETHER AT BOTTOM)
    # ---------------------------------------------------------
    st.divider()
    st.subheader("📘 Additional Information")

    with st.expander("What is the WACC Formula?"):
        st.markdown("""
        WACC blends the cost of equity and debt based on their share in the capital structure.
        """)

        st.latex(r"""
        WACC = \left(\frac{E}{V}\right)R_e
        \;+\;
        \left(\frac{D}{V}\right)R_d(1-T)
        """)

        st.markdown("""
        Where:

        - **E** = Market value of equity  
        - **D** = Market value of debt  
        - **V = E + D**  
        - **Re** = Cost of equity  
        - **Rd** = Cost of debt  
        - **T** = Corporate tax rate  
        """)

    with st.expander("Why do we adjust debt for taxes?"):
        st.markdown("""
        Interest payments reduce taxable income, creating a **tax shield**.
        """)

        st.latex(r"""
        AfterTaxRd = Rd(1-T)
        """)

        st.markdown("""
        Example:

        - Cost of debt = 5%  
        - Tax rate = 20%  

        Effective cost:

        """)

        st.latex(r"""
        5\%(1-0.20)=4\%
        """)

        st.markdown("""
        Equity does not receive this benefit because dividends are paid after tax.
        """)

   


# Run directly
if __name__ == "__main__":
    render_wacc_tool()
