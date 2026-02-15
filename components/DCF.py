import streamlit as st


def render_dcf_tool(go_to):

    # ---------------------------------------------------------
    # HEADER
    # ---------------------------------------------------------
    st.markdown("<h1 style='text-align:center;'>DCF Valuation Model</h1>", unsafe_allow_html=True)

    if st.button("⬅️ Back to Home", use_container_width=True):
        go_to("home")

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
        <p style='font-size:18px;'>
            Discounted Cash Flow (DCF) is a valuation method used to estimate the intrinsic value of a business 
            by forecasting its future free cash flows and discounting them back to today using a required rate of return 
            (typically the Weighted Average Cost of Capital, WACC).
        </p>
        <p style='font-size:16px;'>
            It is widely used in corporate finance, investment banking, equity research, and business controlling 
            to support decisions such as acquisitions, investments, and strategic planning.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ---------------------------------------------------------
    # HIGH-LEVEL ASSUMPTIONS
    # ---------------------------------------------------------
    st.subheader("High-Level Assumptions")

    col1, col2 = st.columns(2)

    with col1:
        years = st.number_input("Forecast Horizon (years)", min_value=3, max_value=15, value=5)
        starting_revenue = st.number_input("Current Revenue", value=1_000_000.0, step=50_000.0)
        revenue_growth = st.number_input("Annual Revenue Growth Rate [%]", value=5.0, step=0.5)
        ebit_margin = st.number_input("EBIT Margin [%]", value=15.0, step=0.5)

    with col2:
        tax_rate = st.number_input("Tax Rate [%]", value=20.0, step=0.5)
        capex_percent = st.number_input("Capex as % of Revenue [%]", value=5.0, step=0.5)
        wc_percent = st.number_input("Change in Working Capital as % of Revenue [%]", value=2.0, step=0.5)
        da_percent = st.number_input("Depreciation & Amortisation as % of Revenue [%]", value=4.0, step=0.5)

    st.markdown("---")

    # ---------------------------------------------------------
    # DISCOUNT RATE & TERMINAL VALUE
    # ---------------------------------------------------------
    st.subheader("Discount Rate & Terminal Value")

    col3, col4 = st.columns(2)

    with col3:
        wacc = st.number_input("Discount Rate (WACC) [%]", value=10.0, step=0.25)
        terminal_growth = st.number_input("Terminal Growth Rate [%]", value=2.0, step=0.25)

    with col4:
        net_debt = st.number_input("Net Debt (Debt – Cash)", value=500_000.0, step=50_000.0)
        shares_outstanding = st.number_input("Shares Outstanding", value=100_000.0, step=1_000.0)

    st.markdown(
        """
        <p style='font-size:14px; color:#8b949e;'>
            WACC reflects the blended required return of both equity and debt holders. 
            The terminal growth rate should normally be conservative and not exceed long-term GDP growth.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ---------------------------------------------------------
    # CALCULATION
    # ---------------------------------------------------------
    if st.button("Run DCF Valuation", use_container_width=True):

        r = wacc / 100.0
        g = terminal_growth / 100.0
        t = tax_rate / 100.0
        rev_growth = revenue_growth / 100.0
        ebit_m = ebit_margin / 100.0
        capex_p = capex_percent / 100.0
        wc_p = wc_percent / 100.0
        da_p = da_percent / 100.0

        revenues = []
        ebits = []
        taxes = []
        da_list = []
        capex_list = []
        wc_changes = []
        fcfs = []

        revenue = starting_revenue

        for year in range(1, int(years) + 1):
            # Revenue forecast
            revenue = revenue * (1 + rev_growth)
            revenues.append(revenue)

            # EBIT
            ebit = revenue * ebit_m
            ebits.append(ebit)

            # Tax on EBIT
            tax = ebit * t
            taxes.append(tax)

            # D&A, Capex, Working Capital
            da = revenue * da_p
            da_list.append(da)

            capex = revenue * capex_p
            capex_list.append(capex)

            wc_change = revenue * wc_p
            wc_changes.append(wc_change)

            # Free Cash Flow to Firm (FCFF)
            fcf = ebit * (1 - t) + da - capex - wc_change
            fcfs.append(fcf)

        # Present value of forecast FCFs
        pv_fcfs = 0
        for i, fcf in enumerate(fcfs):
            pv_fcfs += fcf / ((1 + r) ** (i + 1))

        # Terminal value using Gordon Growth
        last_fcf = fcfs[-1]
        if r <= g:
            terminal_value = float("nan")
            pv_terminal = float("nan")
        else:
            terminal_value = last_fcf * (1 + g) / (r - g)
            pv_terminal = terminal_value / ((1 + r) ** years)

        # Enterprise value
        enterprise_value = pv_fcfs + pv_terminal

        # Equity value
        equity_value = enterprise_value - net_debt

        # Per-share value
        if shares_outstanding > 0:
            value_per_share = equity_value / shares_outstanding
        else:
            value_per_share = float("nan")

        # ---------------------------------------------------------
        # OUTPUT
        # ---------------------------------------------------------
        st.success(f"Estimated Enterprise Value: **${enterprise_value:,.2f}**")
        st.success(f"Estimated Equity Value: **${equity_value:,.2f}**")
        st.success(f"Estimated Value per Share: **${value_per_share:,.2f}**")

        st.markdown("---")

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("### Cash Flow Summary")
            st.write("**Present Value of Forecast FCFs:**", f"${pv_fcfs:,.2f}")
            st.write("**Present Value of Terminal Value:**", f"${pv_terminal:,.2f}")
            st.write("**Undiscounted Terminal Value:**", f"${terminal_value:,.2f}")

        with col_b:
            st.markdown("### Key Assumptions")
            st.write("Forecast years:", int(years))
            st.write("WACC:", f"{wacc:.2f}%")
            st.write("Terminal growth rate:", f"{terminal_growth:.2f}%")
            st.write("Tax rate:", f"{tax_rate:.2f}%")
            st.write("EBIT margin:", f"{ebit_margin:.2f}%")
            st.write("Capex % of revenue:", f"{capex_percent:.2f}%")
            st.write("D&A % of revenue:", f"{da_percent:.2f}%")
            st.write("Δ Working capital % of revenue:", f"{wc_percent:.2f}%")
            st.write("Net debt:", f"${net_debt:,.2f}")
            st.write("Shares outstanding:", f"{shares_outstanding:,.0f}")

        st.markdown("---")

        st.markdown(
            """
            <p style='color:#8b949e; font-size:14px;'>
                <strong>What this model does:</strong><br>
                • Projects revenues and operating profits (EBIT) over a forecast horizon.<br>
                • Converts EBIT into Free Cash Flow to the Firm (FCFF) after tax, capex, and working capital needs.<br>
                • Discounts all FCFFs using WACC to obtain their present value.<br>
                • Calculates a terminal value using the Gordon Growth model and discounts it.<br>
                • Sums the present values to obtain Enterprise Value, then adjusts for net debt to get Equity Value.<br>
                • Divides Equity Value by shares outstanding to estimate intrinsic value per share.<br><br>
<strong>What it is used for:</strong><br>
                • Valuing companies for investment decisions, M&A, and strategic planning.<br>
                • Comparing intrinsic value to market price to assess under/overvaluation.<br>
                • Testing scenarios and sensitivities around growth, margins, and capital intensity.<br>
            </p>
            """,
            unsafe_allow_html=True,
        )

