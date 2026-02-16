import streamlit as st
import pandas as pd
from components.utils import scroll_top

scroll_top()


def render_financial_statement():

    # =========================================================
    # SESSION STATE (must be at the top!)
    # =========================================================
    if "show_ratios" not in st.session_state:
        st.session_state.show_ratios = False

    # =========================================================
    # PAGE TITLE
    # =========================================================
    st.title("📑 Three-Statement Financial Model")

    st.markdown("""
    This interactive calculator presents a simplified:

    - **Income Statement**
    - **Cash Flow Statement**
    - **Balance Sheet**

    Adjust line items directly and observe how the statements connect.

    **More information and ratio analysis below ↓**
    """)

    st.divider()

    # =========================================================
    # INCOME STATEMENT
    # =========================================================
    st.header("📄 Income Statement")

    revenue = st.number_input("Revenue", value=500000.0, step=10000.0, key="Revenue")

    cogs = st.number_input(
        "Cost of Goods Sold (negative)",
        value=-325000.0,
        step=10000.0,
        key="COGS"
    )

    gross_profit = revenue + cogs
    st.write("**Gross Profit:**", f"{gross_profit:,.0f}")

    operating_expenses = st.number_input(
        "Operating Expenses (negative)",
        value=-120000.0,
        step=5000.0,
        key="Operating Expenses"
    )

    ebit = gross_profit + operating_expenses
    st.write("**EBIT:**", f"{ebit:,.0f}")

    interest_expense = st.number_input(
        "Interest Expense (negative)",
        value=-15000.0,
        step=1000.0,
        key="Interest Expense"
    )

    profit_before_tax = ebit + interest_expense
    st.write("**Profit Before Tax:**", f"{profit_before_tax:,.0f}")

    old_tax_rate = 25.0
    tax_rate = st.number_input("Tax Rate (%)", value=25.0, step=0.5, key="Tax Rate")

    if tax_rate != old_tax_rate:
        st.info("""
💡 **Tax Rate Change Detected**

Under IFRS/GAAP, deferred tax assets and liabilities must be remeasured
when tax rates change. This prevents distortion of current-year earnings.
""")

    tax_expense = -(profit_before_tax * tax_rate / 100)
    net_income = profit_before_tax + tax_expense

    st.write("**Tax Expense:**", f"{tax_expense:,.0f}")
    st.markdown(f"### ✅ Net Income: **{net_income:,.0f}**")

    st.divider()

    # =========================================================
    # CASH FLOW STATEMENT
    # =========================================================
    st.header("💵 Cash Flow Statement")

    depreciation = st.number_input("Depreciation", value=25000.0, step=2000.0, key="Depreciation")

    change_wc = st.number_input(
        "Change in Working Capital",
        value=-5000.0,
        step=2000.0,
        key="Change WC"
    )

    cash_from_ops = net_income + depreciation + change_wc
    st.write("**Cash from Operations:**", f"{cash_from_ops:,.0f}")

    capex = st.number_input(
        "Capital Expenditures (negative)",
        value=-30000.0,
        step=5000.0,
        key="CapEx"
    )

    net_cash_flow = cash_from_ops + capex
    st.markdown(f"### ✅ Net Cash Flow: **{net_cash_flow:,.0f}**")

    opening_cash = st.number_input(
        "Opening Cash Balance",
        value=40000.0,
        step=5000.0,
        key="Opening Cash"
    )

    closing_cash = opening_cash + net_cash_flow

    st.write(
        f"**Closing Cash Balance:** {closing_cash:,.0f} "
        f"(Opening Cash {opening_cash:,.0f} + Net Flow {net_cash_flow:,.0f})"
    )

    st.divider()

    # =========================================================
    # BALANCE SHEET
    # =========================================================
    st.header("🏛 Balance Sheet")

    st.subheader("Assets")

    cash = closing_cash
    st.write(f"**Cash:** {cash:,.0f}")



    accounts_receivable = st.number_input(
        "Accounts Receivable",
        value=60000.0,
        step=5000.0,
        key="Accounts Receivable"
    )

    inventory = st.number_input(
        "Inventory",
        value=55000.0,
        step=5000.0,
        key="Inventory"
    )

    ppe = st.number_input(
        "Property, Plant & Equipment",
        value=300000.0,
        step=10000.0,
        key="PPE"
    )

    total_assets = cash + accounts_receivable + inventory + ppe
    st.markdown(f"### Total Assets: **{total_assets:,.0f}**")

    st.subheader("Liabilities")

    current_liabilities = st.number_input(
        "Current Liabilities",
        value=75000.0,
        step=5000.0,
        key="Current Liabilities"
    )

    long_term_liabilities = st.number_input(
        "Long-Term Liabilities",
        value=150000.0,
        step=5000.0,
        key="Long-Term Liabilities"
    )

    total_liabilities = current_liabilities + long_term_liabilities
    st.markdown(f"### Total Liabilities: **{total_liabilities:,.0f}**")

    st.subheader("Equity")

    share_capital = st.number_input(
        "Share Capital",
        value=120000.0,
        step=5000.0,
        key="Share Capital"
    )

    retained_earnings = st.number_input(
        "Retained Earnings",
        value=130000.0,
        step=5000.0,
        key="Retained Earnings"
    )

    total_equity = share_capital + retained_earnings
    st.markdown(f"### Total Equity: **{total_equity:,.0f}**")

    st.markdown(f"### 📘 Total Equity + Liabilities: **{total_equity + total_liabilities:,.0f}**")

    # =========================================================
    # BALANCE CHECK
    # =========================================================
    st.divider()

    total_e_and_l = total_liabilities + total_equity
    diff = total_assets - total_e_and_l

    if abs(diff) < 1:
        st.success("✅ Balance Sheet is Balanced.")
    else:
        st.warning(
            f"⚠️ Balance Sheet is NOT Balanced.\n\n"
            f"Difference: **{diff:,.0f}**\n\n"
            "Adjust Equity or Liabilities until Assets = Liabilities + Equity."
        )

    # =========================================================
    # RESET BUTTON (SUBTLE + SAFE)
    # =========================================================
    st.markdown("---")
    st.caption("Reset all inputs to their original default values.")

    if st.button("Reset Inputs", use_container_width=True):

        # Clear everything safely
        st.session_state.clear()

        # Restore only the defaults
        st.session_state.update({
            "Revenue": 500000.0,
            "COGS": -325000.0,
            "Operating Expenses": -120000.0,
            "Interest Expense": -15000.0,
            "Tax Rate": 25.0,
            "Depreciation": 25000.0,
            "Change WC": -5000.0,
            "CapEx": -30000.0,
            "Opening Cash": 40000.0,
            "Accounts Receivable": 60000.0,
            "Inventory": 55000.0,
            "PPE": 300000.0,
            "Current Liabilities": 75000.0,
            "Long-Term Liabilities": 150000.0,
            "Share Capital": 120000.0,
            "Retained Earnings": 130000.0,
            "show_ratios": False,
        })

        st.rerun()

    st.divider()

    # =========================================================
    # FINANCIAL RATIOS
    # =========================================================
    st.header("📊 Financial Ratio Analysis")

    st.markdown("Click below to calculate ratios based on the linked statements above.")

    if st.button("📊 Calculate Ratios", use_container_width=True):
        st.session_state.show_ratios = True

    if st.session_state.show_ratios:

        current_assets = cash + accounts_receivable + inventory

        ratios = {
            "Liquidity Ratios": {
                "Current Ratio": current_assets / current_liabilities,
                "Quick Ratio": (cash + accounts_receivable) / current_liabilities,
                "Cash Ratio": cash / current_liabilities
            },

            "Profitability Ratios": {
                "Gross Margin": gross_profit / revenue,
                "Operating Margin": ebit / revenue,
                "Net Margin": net_income / revenue
            },

            "Leverage Ratios": {
                "Debt-to-Equity": total_liabilities / total_equity,
                "Debt Ratio": total_liabilities / total_assets
            },

            "Return Ratios": {
                "ROA (Return on Assets)": net_income / total_assets,
                "ROE (Return on Equity)": net_income / total_equity
            }
        }

        for category, values in ratios.items():
            st.subheader(category)

            ratio_df = pd.DataFrame({
                "Ratio": list(values.keys()),
                "Value": [
                    f"{v:.2%}" if v < 1 else f"{v:.2f}"
                    for v in values.values()
                ]
            })

            st.dataframe(ratio_df, hide_index=True, use_container_width=True)

    # =========================================================
    # ADDITIONAL INFORMATION SECTION
    # =========================================================
    st.divider()
    st.header("📘 Additional Information")

    with st.expander("How the 3 statements connect"):
        st.markdown("""
- **Net Income** flows into Retained Earnings  
- **Depreciation** reduces profit but increases cash  
- **CapEx** reduces cash but increases PPE  
- **Working Capital** explains timing differences between profit and cash  
""")

    with st.expander("Why ratios matter"):
        st.markdown("""
Ratios help analysts evaluate:

- Liquidity  
- Profitability  
- Leverage  
- Returns  

These are essential for valuation, credit analysis, and investment decisions.
""")

    with st.expander("Ratio Formulas & Good Ranges"):
        st.markdown("""
### Liquidity Ratios
| Ratio | Formula | Good Range |
|-------|---------|------------|
| Current Ratio | Current Assets / Current Liabilities | **1.5 – 2.5** |
| Quick Ratio | (Cash + AR) / Current Liabilities | **≥ 1.0** |
| Cash Ratio | Cash / Current Liabilities | **0.2 – 1.0** |

### Profitability Ratios
| Ratio | Formula | Good Range |
|-------|---------|------------|
| Gross Margin | Gross Profit / Revenue | **30% – 60%** |
| Operating Margin | EBIT / Revenue | **10% – 30%** |
| Net Margin | Net Income / Revenue | **5% – 20%** |

### Leverage Ratios
| Ratio | Formula | Good Range |
|-------|---------|------------|
| Debt-to-Equity | Total Liabilities / Total Equity | **0.5 – 2.0** |
| Debt Ratio | Total Liabilities / Total Assets | **20% – 60%** |

### Return Ratios
| Ratio | Formula | Good Range |
|-------|---------|------------|
| ROA | Net Income / Total Assets | **5% – 10%** |
| ROE | Net Income / Total Equity | **10% – 20%** |
""")

