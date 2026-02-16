import streamlit as st
import numpy as np
import numpy_financial as nf
import pandas as pd
import plotly.graph_objects as go
from components.utils import scroll_top



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

# -----------------------------
# Number formatting
# -----------------------------
def format_number(n):
    return f"{n:,.2f}".replace(",", " ").replace(".", ",")

# -----------------------------
# MAIN RENDER FUNCTION
# -----------------------------
def render_npv_tool(go_to=None):
    scroll_top()

    # -----------------------------
    # Page Styling
    # -----------------------------
    st.markdown("""
    <style>
        .block-container {
            max-width: 1500px !important;
            padding-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

    # -----------------------------
    # Title
    # -----------------------------
    st.title("💰 NPV / IRR / Payback Calculator")
    scroll_top()

    if go_to is not None:
        if st.button("⬅️ Back to Home", use_container_width=True):
            go_to("home")

    st.markdown(
    "Evaluate an investment by calculating Net Present Value (NPV), "
    "Internal Rate of Return (IRR), and Payback Period.\n\n"
    "**More information below ↓**"
)


    st.markdown("---")

    # -----------------------------
    # Inputs
    # -----------------------------
    st.header("📥 Input Parameters")

    colA, colB, colC = st.columns(3)

    with colA:
        initial_investment = st.number_input(
            "Initial Investment (SEK)",
            min_value=0.0,
            value=10000.0,
            step=1000.0,
            key="investment"
        )

    with colB:
    	discount_rate = st.number_input(
        "Discount Rate (%)",
        min_value=0.0,
        value=10.000,
        step=0.01,
        format="%.3f",
        key="rate"
    ) / 100


    with colC:
        years = st.number_input(
            "Number of Years",
            min_value=1,
            max_value=30,
            value=5,
            key="years"
        )

    # -----------------------------
    # Cash Flows
    # -----------------------------
    st.subheader("📈 Annual Cash Flows")

    cash_flows = []
    for i in range(int(years)):
        cf = st.number_input(
            f"Year {i+1} Cash Flow (SEK)",
            value=3000.0,
            step=500.0,
            key=f"cf_{i}"
        )
        cash_flows.append(cf)

    st.markdown("---")

    # =====================================================
    # AUTO CALCULATION
    # =====================================================

    # NPV
    discounted = []
    npv = -initial_investment

    for t, cf in enumerate(cash_flows, start=1):
        dcf = cf / ((1 + discount_rate) ** t)
        discounted.append(dcf)
        npv += dcf

    # IRR (high precision)
    irr = float(nf.irr([-initial_investment] + cash_flows))

    # Payback
    cumulative = 0
    payback = None

    for year, cf in enumerate(cash_flows, start=1):
        prev = cumulative
        cumulative += cf

        if cumulative >= initial_investment:
            remaining = initial_investment - prev
            fraction = remaining / cf
            payback = year - 1 + fraction
            break

    # -----------------------------
    # Results Summary
    # -----------------------------
    st.header("📊 Results Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("💵 NPV", f"{format_number(npv)} SEK")
    col2.metric("📈 IRR", f"{irr*100:.4f}%")  # ← 4 decimals
    col3.metric(
        "⏳ Payback Period",
        f"{payback:.2f} years" if payback else "Not reached"
    )

    st.markdown("---")

    # -----------------------------
    # Table
    # -----------------------------
    df = pd.DataFrame({
        "Year": list(range(1, int(years) + 1)),
        "Cash Flow (SEK)": cash_flows,
        "Discounted Cash Flow (SEK)": discounted
    })

    st.subheader("📋 Cash Flow Table")
    st.dataframe(
        df.style.format({
            "Cash Flow (SEK)": lambda x: format_number(x),
            "Discounted Cash Flow (SEK)": lambda x: format_number(x)
        })
    )

    st.markdown("---")

    # -----------------------------
    # Tornado Sensitivity Chart
    # -----------------------------
    st.subheader("🌪️ Tornado Chart: ±10% Sensitivity")

    def calc_npv(inv, cfs, dr):
        total = -inv
        for t, cf in enumerate(cfs, start=1):
            total += cf / ((1 + dr) ** t)
        return total

    base_npv = npv
    variables = []

    # Investment ±10%
    inv_low = calc_npv(initial_investment * 0.9, cash_flows, discount_rate)
    inv_high = calc_npv(initial_investment * 1.1, cash_flows, discount_rate)
    variables.append(["Initial Investment", inv_low, inv_high])

    # Cash Flows ±10%
    cf_low = calc_npv(initial_investment, [cf * 0.9 for cf in cash_flows], discount_rate)
    cf_high = calc_npv(initial_investment, [cf * 1.1 for cf in cash_flows], discount_rate)
    variables.append(["Cash Flows", cf_low, cf_high])

    # Discount Rate ±10%
    dr_low = calc_npv(initial_investment, cash_flows, discount_rate * 0.9)
    dr_high = calc_npv(initial_investment, cash_flows, discount_rate * 1.1)
    variables.append(["Discount Rate", dr_low, dr_high])

    tornado_df = pd.DataFrame(variables, columns=["Variable", "Low", "High"])
    tornado_df["Low Impact"] = tornado_df["Low"] - base_npv
    tornado_df["High Impact"] = tornado_df["High"] - base_npv
    tornado_df["Range"] = abs(tornado_df["High Impact"] - tornado_df["Low Impact"])
    tornado_df = tornado_df.sort_values("Range", ascending=True)

    fig = go.Figure()

    for idx, row in tornado_df.iterrows():

        fig.add_trace(go.Bar(
            y=[row["Variable"]],
            x=[row["Low Impact"]],
            orientation="h",
            name="-10%",
            marker_color="salmon",
            showlegend=bool(idx == tornado_df.index[0])
        ))

        fig.add_trace(go.Bar(
            y=[row["Variable"]],
            x=[row["High Impact"]],
            orientation="h",
            name="+10%",
            marker_color="lightgreen",
            showlegend=bool(idx == tornado_df.index[0])
        ))

    fig.update_layout(
        barmode="overlay",
        title="Tornado Sensitivity Chart (NPV Impact)",
        xaxis_title="NPV Impact (SEK)",
        yaxis_title="Variable",
        template="simple_white",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # ADDITIONAL INFORMATION SECTION
    # =========================================================
    st.markdown("---")
    st.header("📘 Additional Information")

    with st.expander("What is NPV?"):
        st.markdown(r"""
**Net Present Value (NPV)** measures the value today of future cash flows, discounted at a chosen rate.

- **NPV > 0** → The investment **creates value**  
- **NPV < 0** → The investment **destroys value**  
- **NPV = 0** → The investment **breaks even**  

### Formula



\[
NPV = \sum_{t=1}^{N} \frac{CF_t}{(1+r)^t} - \text{Initial Investment}
\]



Where:  
- \( CF_t \) = cash flow in year t  
- \( r \) = discount rate  
- \( N \) = number of years  
""")

    with st.expander("What is IRR?"):
        st.markdown(r"""
**Internal Rate of Return (IRR)** is the discount rate that makes the NPV equal to zero.

It represents the investment’s annualized return.

Decision rule:

- IRR > Discount Rate → Accept  
- IRR < Discount Rate → Reject  
""")
        st.caption("If you enter the IRR above as the discount rate, the NPV will equal exactly zero.")

    with st.expander("What is Payback Period?"):
        st.markdown("""
The **Payback Period** measures how long it takes to recover the initial investment.

It ignores:

- the time value of money  
- cash flows after payback  

…but it is useful for quick risk assessments.
""")

    with st.expander("Sensitivity Analysis Explained"):
        st.markdown("""
The **Tornado Chart** shows how sensitive NPV is to changes in:

- Initial investment  
- Annual cash flows  
- Discount rate  

A wider bar = greater impact on NPV.
""")

    
