import streamlit as st
from components.utils import scroll_top

scroll_top()

def render_dcf_tool():

    # ---------------------------------------------------------
    # HEADER
    # ---------------------------------------------------------
    st.markdown("<h1 style='text-align:center;'>DCF Valuation Model</h1>", unsafe_allow_html=True)

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
        <p style='font-size:16px;'>
            More information below ↓
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
            revenue = revenue * (1 + rev_growth)
            revenues.append(revenue)

            ebit = revenue * ebit_m
            ebits.append(ebit)

            tax = ebit * t
            taxes.append(tax)

            da = revenue * da_p
            da_list.append(da)

            capex = revenue * capex_p
            capex_list.append(capex)

            wc_change = revenue * wc_p
            wc_changes.append(wc_change)

            fcf = ebit * (1 - t) + da - capex - wc_change
            fcfs.append(fcf)

        pv_fcfs = sum(fcf / ((1 + r) ** (i + 1)) for i, fcf in enumerate(fcfs))

        last_fcf = fcfs[-1]
        if r <= g:
            terminal_value = float("nan")
            pv_terminal = float("nan")
        else:
            terminal_value = last_fcf * (1 + g) / (r - g)
            pv_terminal = terminal_value / ((1 + r) ** years)

        enterprise_value = pv_fcfs + pv_terminal
        equity_value = enterprise_value - net_debt
        value_per_share = equity_value / shares_outstanding if shares_outstanding > 0 else float("nan")

        # ---------------------------------------------------------
        # OUTPUT
        # ---------------------------------------------------------
        st.success(f"Estimated Enterprise Value: **${enterprise_value:,.2f}**")
        st.success(f"Estimated Value of Debt: **${net_debt:,.2f}**")
        st.success(f"Estimated Equity Value: **${equity_value:,.2f}**")
        st.success(f"Estimated Value per Share: **${value_per_share:,.2f}**")

        st.markdown("---")

        # ---------------------------------------------------------
        # PREMIUM CARD‑STYLE SUMMARY
        # ---------------------------------------------------------
        st.markdown("### 📊 Cash Flow Summary")

        st.markdown(f"""
        <div style="
            background-color:#161b22;
            padding:18px;
            border-radius:12px;
            border:1px solid #30363d;
            font-size:15px;">
            <b>Present Value of Forecast FCFs:</b> ${pv_fcfs:,.2f}<br>
            <b>Present Value of Terminal Value:</b> ${pv_terminal:,.2f}<br>
            <b>Undiscounted Terminal Value:</b> ${terminal_value:,.2f}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("### ⚙️ Key Assumptions")

        st.markdown(f"""
        <div style="
            background-color:#161b22;
            padding:18px;
            border-radius:12px;
            border:1px solid #30363d;
            font-size:15px;">
            <b>Forecast years:</b> {int(years)}<br>
            <b>WACC:</b> {wacc:.2f}%<br>
            <b>Terminal growth rate:</b> {terminal_growth:.2f}%<br>
            <b>Tax rate:</b> {tax_rate:.2f}%<br>
            <b>EBIT margin:</b> {ebit_margin:.2f}%<br>
            <b>Capex % of revenue:</b> {capex_percent:.2f}%<br>
            <b>D&A % of revenue:</b> {da_percent:.2f}%<br>
            <b>Δ Working capital % of revenue:</b> {wc_percent:.2f}%<br>
            <b>Net debt:</b> ${net_debt:,.2f}<br>
            <b>Shares outstanding:</b> {shares_outstanding:,.0f}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

    # ---------------------------------------------------------
    # ADDITIONAL INFORMATION SECTION
    # ---------------------------------------------------------
    st.subheader("📘 Additional Information")

    with st.expander("What does this DCF model do?"):
        st.markdown("""
This DCF model:

- Projects revenues and operating profits (EBIT)  
- Converts EBIT into **Free Cash Flow to the Firm (FCFF)**  
- Discounts all FCFFs using **WACC**  
- Calculates a **terminal value** using the Gordon Growth Model  
- Sums all discounted cash flows to estimate **Enterprise Value**  
- Subtracts net debt to get **Equity Value**  
- Divides by shares outstanding to estimate **intrinsic value per share**  
""")

    with st.expander("What is this model used for?"):
        st.markdown("""
DCF valuation is widely used in:

- Investment banking  
- Equity research  
- Corporate finance  
- Private equity  
- Business controlling  

It helps determine whether a company is **undervalued or overvalued** by comparing intrinsic value to market price.

It is also used for:

- Acquisition decisions  
- Strategic planning  
- Capital budgeting  
- Scenario and sensitivity analysis  
""")

    with st.expander("How does a DCF actually create value? (Conceptual Explanation)"):
        st.markdown("""
A DCF works by translating a company’s **future potential** into a value today.

### 1. The business generates cash flows over time  
A company earns money each year. These future cash flows are the foundation of value.  
DCF asks: *“How much are those future cash flows worth today?”*

### 2. Money in the future is worth less than money today  
Because of risk, inflation, and opportunity cost, future cash flows must be **discounted**.  
This is why we use **WACC** — it represents the required return investors demand.

### 3. The forecast period captures the near‑term performance  
You explicitly model the next 5–10 years.  
This shows how the business grows, invests, and generates cash in the medium term.

### 4. The terminal value captures the long‑term future  
After the forecast period, the business is assumed to grow steadily forever.  
This “steady‑state” value is called the **terminal value**, and it usually represents most of the company’s worth.

### 5. Discount everything back to today  
Both the forecast cash flows and the terminal value are discounted using WACC.  
This converts long‑term potential into a **present‑day valuation**.

### 6. Adjust for debt to get equity value  
Enterprise value reflects the whole business.  
Subtracting net debt gives the value that belongs to shareholders.

### 7. Divide by shares to get intrinsic value per share  
This tells you what each share is fundamentally worth based on the company’s ability to generate cash.

---

**In short:**  
A DCF values a company by estimating all the cash it will ever produce, adjusting for risk, and converting that into today’s money.  
""")

 