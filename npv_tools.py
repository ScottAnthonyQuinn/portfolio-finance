import streamlit as st
import numpy as np
import numpy_financial as nf
import pandas as pd
import plotly.graph_objects as go

# -----------------------------
# Number formatting (space thousands, dot decimals)
# -----------------------------
def format_number(n):
    return f"{n:,.2f}".replace(",", "X").replace(".", ",").replace("X", " ").replace(",", ".")

# -----------------------------
# MAIN RENDER FUNCTION
# -----------------------------
def render_npv_tool():

    st.title("💰 NPV / IRR / Payback Calculator")

    st.write(
        "Evaluate an investment by calculating Net Present Value (NPV), "
        "Internal Rate of Return (IRR), and Payback Period. "
        "Includes a tornado sensitivity chart for ±10% changes."
    )

    st.markdown("---")

    # -----------------------------
    # Inputs Section
    # -----------------------------
    st.header("📥 Input Parameters")

    colA, colB, colC = st.columns(3)

    with colA:
        initial_investment = st.number_input(
            "Initial Investment (SEK)",
            min_value=0.0,
            value=10000.0,
            step=1000.0
        )

    with colB:
        discount_rate = st.number_input(
            "Discount Rate (%)",
            min_value=0.0,
            value=10.0,
            step=0.5
        ) / 100

    with colC:
        years = st.number_input(
            "Number of Years",
            min_value=1,
            max_value=30,
            value=5
        )

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

    # -----------------------------
    # Calculation
    # -----------------------------
    if st.button("Calculate Results"):

        # NPV
        discounted = []
        npv = -initial_investment

        for t, cf in enumerate(cash_flows, start=1):
            dcf = cf / ((1 + discount_rate) ** t)
            discounted.append(dcf)
            npv += dcf

        # IRR
        irr = nf.irr([-initial_investment] + cash_flows)

        # Fractional Payback Period
        cumulative = 0
        payback = None

        for year, cf in enumerate(cash_flows, start=1):
            prev_cumulative = cumulative
            cumulative += cf

            if cumulative >= initial_investment:
                remaining = initial_investment - prev_cumulative
                fraction = remaining / cf
                payback = year - 1 + fraction
                break

        # -----------------------------
        # Results Display
        # -----------------------------
        st.header("📊 Results Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric("💵 NPV", f"{format_number(npv)} SEK")
        col2.metric("📈 IRR", f"{irr*100:.2f}%")
        col3.metric("⏳ Payback Period", f"{payback:.2f} years" if payback else "Not reached")

        st.markdown("---")

        # -----------------------------
        # Cash Flow Table
        # -----------------------------
        df = pd.DataFrame({
            "Year": list(range(1, int(years)+1)),
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
        # Cash Flow Chart
        # -----------------------------
        st.subheader("📉 Cash Flow Chart")
        st.line_chart(df, x="Year", y=["Cash Flow (SEK)", "Discounted Cash Flow (SEK)"])

        st.markdown("---")

        # -----------------------------
        # Tornado Sensitivity Analysis
        # -----------------------------
        st.subheader("🌪️ Tornado Chart: ±10% Sensitivity")

        def calc_npv(inv, cfs, dr):
            total = -inv
            for t, cf in enumerate(cfs, start=1):
                total += cf / ((1 + dr) ** t)
            return total

        base_npv = npv
        variables = []

        # Initial Investment ±10%
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
            show_low = True if idx == tornado_df.index[0] else False
            show_high = True if idx == tornado_df.index[0] else False

            fig.add_trace(go.Bar(
                y=[row["Variable"]],
                x=[row["Low Impact"]],
                orientation='h',
                name='-10%',
                marker_color='salmon',
                showlegend=show_low
            ))

            fig.add_trace(go.Bar(
                y=[row["Variable"]],
                x=[row["High Impact"]],
                orientation='h',
                name='+10%',
                marker_color='lightgreen',
                showlegend=show_high
            ))

        fig.update_layout(
            barmode='overlay',
            title="Tornado Sensitivity Chart (NPV Impact)",
            xaxis_title="NPV Impact (SEK)",
            yaxis_title="Variable",
            template="simple_white",
            height=450
        )

        st.plotly_chart(fig, use_container_width=True)
