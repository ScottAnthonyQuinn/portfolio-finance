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
            The Capital Asset Pricing Model (CAPM) calculates the expected return of an asset based on its risk.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # ---------- INPUTS ----------
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

        st.success(f"Expected Return: **{expected_return_percent:.2f}%**")

        st.markdown("---")
        st.markdown(
            f"""
            <p style='font-size:16px;'>
                <strong>Details:</strong><br>
                • Risk‑Free Rate (Rf): {risk_free:.2f}%<br>
                • Market Return (Rm): {market_return:.2f}%<br>
                • Market Risk Premium (Rm − Rf): {market_premium:.2f}%<br>
                • Beta (β): {beta:.2f}<br>
            </p>
            """,
            unsafe_allow_html=True,
        )

    # ---------- FOOTER ----------
    st.markdown("---")
    st.markdown(
        """
        <p style='color:#8b949e; font-size:14px;'>
            Formula:<br>
            <strong>Expected Return = Rf + β (Rm − Rf)</strong>
        </p>
        """,
        unsafe_allow_html=True,
    )
