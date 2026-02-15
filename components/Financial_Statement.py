import streamlit as st
import pandas as pd


def render_financial_statement(go_to):

    # =========================================================
    # PAGE TITLE
    # =========================================================
    st.markdown(
        "<h1 style='text-align:center;'>Financial Statements</h1>",
        unsafe_allow_html=True
    )

    st.write(
        "This page presents a simplified **three-statement financial model** "
        "(Income Statement, Cash Flow Statement, and Balance Sheet). "
        "We can explore how statements connect and evaluate performance "
        "using key financial ratios. Calculate rations below"
    )

    if st.button("⬅️ Back to Home", use_container_width=True):
        go_to("home")

    st.markdown("---")

    # =========================================================
    # SESSION STATE
    # =========================================================
    if "show_ratios" not in st.session_state:
        st.session_state.show_ratios = False

    # =========================================================
    # 1. INCOME STATEMENT
    # =========================================================
    st.markdown("## Income Statement")

    revenue = st.number_input("Revenue", value=500000.0, step=1.0)

    cogs = st.number_input(
        "Cost of Goods Sold (negative)",
        value=-325000.0,
        step=1.0
    )

    gross_profit = revenue + cogs
    st.write("**Gross Profit:**", f"{gross_profit:,.0f}")

    operating_expenses = st.number_input(
        "Operating Expenses (negative)",
        value=-120000.0,
        step=1.0
    )

    operating_profit = gross_profit + operating_expenses
    st.write("**Operating Profit (EBIT):**", f"{operating_profit:,.0f}")

    interest_expense = st.number_input(
        "Interest Expense (negative)",
        value=-15000.0,
        step=1.0
    )

    profit_before_tax = operating_profit + interest_expense
    st.write("**Profit Before Tax:**", f"{profit_before_tax:,.0f}")

    # -----------------------------
    # TAX RATE + REMEASUREMENT
    # -----------------------------
    old_tax_rate = 25.0
    tax_rate = st.number_input("Tax Rate (%)", value=25.0, step=0.1)

    # Remeasurement gain/loss (simplified teaching version)
    tax_remeasurement = (tax_rate - old_tax_rate) / 100 * profit_before_tax

    st.write("**Tax Rate Remeasurement Adjustment:**", f"{tax_remeasurement:,.0f}")

    # Teaching note only when tax changes
    if tax_rate != old_tax_rate:
        st.info(
            "💡 **The tax rate changed.**\n\n"
            "**Why net income did NOT change:**\n"
            "A higher tax rate increases this year's tax expense, but accounting rules require companies to "
            "remeasure their **deferred tax assets and liabilities** when tax rates change. This remeasurement "
            "creates a one‑time gain or loss that offsets the change in tax expense, so the net effect on "
            "this year's net income is neutral.\n\n"
            "**Why this matters:**\n"
            "- Prior‑year retained earnings are **not** restated.\n"
            "- The remeasurement ensures the tax rate change does **not distort this year's performance**.\n"
            "- The balance sheet stays balanced without altering last year's reported results.\n\n"
            "This is how IFRS/GAAP handle tax rate changes in financial statements."
        )

    # Apply tax expense normally
    tax_expense = -(profit_before_tax * tax_rate / 100)
    st.write("**Tax Expense:**", f"{tax_expense:,.0f}")

    # Net income now includes remeasurement
    net_income = profit_before_tax + tax_expense + tax_remeasurement
    st.markdown("### ✅ Net Income: " + f"{net_income:,.0f}")

    st.markdown("---")

    # =========================================================
    # 2. CASH FLOW STATEMENT
    # =========================================================
    st.markdown("## Cash Flow Statement")

    depreciation = st.number_input("Depreciation", value=25000.0, step=1.0)

    change_wc = st.number_input(
        "Change in Working Capital",
        value=-5000.0,
        step=1.0
    )

    cash_from_ops = net_income + depreciation + change_wc
    st.write("**Cash from Operating Activities:**", f"{cash_from_ops:,.0f}")

    capex = st.number_input(
        "Capital Expenditures (negative)",
        value=-30000.0,
        step=1.0
    )

    net_cash_flow = cash_from_ops + capex
    st.markdown("### ✅ Net Cash Flow: " + f"{net_cash_flow:,.0f}")

    st.markdown("---")

    # =========================================================
    # 3. BALANCE SHEET (BALANCES ON LOAD)
    # =========================================================
    st.markdown("## Balance Sheet")

    st.markdown("### Assets")

    opening_cash = st.number_input("Opening Cash", value=40000.0, step=1.0)

    closing_cash = opening_cash + net_cash_flow

    st.write(
        "**Closing Cash:**",
        f"{closing_cash:,.0f}",
        "(Opening Cash",
        f"{opening_cash:,.0f}",
        "+ Net Cash Flow",
        f"{net_cash_flow:,.0f})"
    )

    ar = st.number_input("Accounts Receivable", value=60000.0, step=1.0)
    inv = st.number_input("Inventory", value=55000.0, step=1.0)
    ppe = st.number_input("Property, Plant & Equipment", value=300000.0, step=1.0)

    total_assets = closing_cash + ar + inv + ppe
    st.markdown("### **Total Assets:** " + f"{total_assets:,.0f}")

    st.markdown("### Equity and Liabilities")

    current_liabilities = st.number_input(
        "Current Liabilities",
        value=75000.0,
        step=1.0
    )

    noncurrent_liabilities = st.number_input(
        "Non-Current Liabilities",
        value=150000.0,
        step=1.0
    )

    total_liabilities = current_liabilities + noncurrent_liabilities

    share_capital = st.number_input(
        "Share Capital",
        value=120000.0,
        step=1.0
    )

    retained_earnings = st.number_input(
        "Retained Earnings",
        value=130000.0,
        step=1.0
    )

    total_equity = share_capital + retained_earnings
    st.write("**Total Equity:**", f"{total_equity:,.0f}")

    total_e_and_l = total_equity + total_liabilities
    st.markdown("### **Total Equity + Liabilities:** " + f"{total_e_and_l:,.0f}")

    diff = total_assets - total_e_and_l

    if abs(diff) == 0:
        st.success("✅ Balance sheet is balanced.")
    else:
        st.warning("⚠️ Balance sheet does not balance. Difference: " + f"{diff:,.0f}")

    st.markdown("---")

    # =========================================================
    # 4. FINANCIAL RATIOS
    # =========================================================
    if st.button("Calculate Ratios", use_container_width=True):
        st.session_state.show_ratios = True

    if st.session_state.show_ratios:

        st.markdown("## Financial Ratios")

        current_assets = closing_cash + ar + inv
        ebit = operating_profit
        ebitda = operating_profit + depreciation

        ratios = {
            "Liquidity Ratios": [
                ("Current Ratio", current_assets / current_liabilities,
                 "Short-term solvency", "1.5 – 2.5"),
                ("Quick Ratio", (closing_cash + ar) / current_liabilities,
                 "Liquidity excluding inventory", "≥ 1.0"),
                ("Cash Ratio", closing_cash / current_liabilities,
                 "Most conservative liquidity", "0.2 – 0.5"),
            ],

            "Profitability Ratios": [
                ("Gross Margin", gross_profit / revenue,
                 "Profit after COGS", "30% – 60%"),
                ("Operating Margin", operating_profit / revenue,
                 "Core operating profitability", "10% – 25%"),
                ("Net Margin", net_income / revenue,
                 "Bottom-line profitability", "5% – 20%"),
            ],

            "Leverage Ratios": [
                ("Debt-to-Equity", total_liabilities / total_equity,
                 "Financial leverage", "0.5 – 2.0"),
                ("Debt Ratio", total_liabilities / total_assets,
                 "Assets financed by debt", "< 0.6"),
            ],

            "Return Ratios": [
                ("ROA", net_income / total_assets,
                 "Return on assets", "5% – 10%"),
                ("ROE", net_income / total_equity,
                 "Return on equity", "10% – 20%"),
            ],
        }

        for category, items in ratios.items():
            st.markdown("### " + category)

            df = pd.DataFrame(
                [{
                    "Ratio": name,
                    "Value": f"{value:.2%}" if value < 1 else f"{value:.2f}",
                    "Good Range": good_range,
                    "Explanation": explanation
                }
                for name, value, explanation, good_range in items]
            )

            st.table(df)
