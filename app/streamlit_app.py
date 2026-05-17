from __future__ import annotations

from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

from financial_analysis import (
    build_analysis_summary,
    build_ratio_table,
    calculate_historical_metrics,
    format_percentage_columns,
    load_financial_data,
    summarize_financial_trends,
)
from prompts import PROMPT_LIBRARY, render_prompt_card
from report_generator import build_narrative_sections, generate_report_markdown
from valuation_model import build_sensitivity_table, format_dcf_table, run_dcf_valuation


BASE_DIR = Path(__file__).resolve().parents[1]
SAMPLE_FINANCIALS_PATH = BASE_DIR / "data" / "wuxi_financials_sample.csv"
SAMPLE_PEERS_PATH = BASE_DIR / "data" / "peer_companies_sample.csv"


st.set_page_config(
    page_title="CRDMO Analyst Copilot",
    page_icon="📊",
    layout="wide",
)

st.markdown(
    """
<style>
    .stApp {
        background:
            radial-gradient(circle at top right, rgba(43,108,176,0.12), transparent 28%),
            linear-gradient(180deg, #f7fafc 0%, #edf2f7 100%);
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid rgba(43, 108, 176, 0.10);
        border-radius: 16px;
        padding: 0.8rem;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04);
    }
    div[data-testid="stVerticalBlock"] div:has(> div > div > div > div.stDownloadButton) {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 16px;
    }
</style>
""",
    unsafe_allow_html=True,
)


def render_landing_page() -> None:
    st.title("CRDMO Analyst Copilot")
    st.caption(
        "Industry-focused AI equity research valuation agent prototype for ACC102 coursework."
    )
    st.markdown(
        """
This prototype is designed for brokerage equity research analysts covering pharmaceutical CRDMO and CRO-CDMO companies.
It demonstrates an end-to-end workflow across company intake, data preparation, historical financial analysis, human-reviewed valuation assumptions, DCF modelling, and report generation.

Important note: the bundled WuXi AppTec dataset now uses verified historical figures from official company disclosures for 2019-2023. Peer data and valuation assumptions remain prototype inputs and should still be reviewed before final submission or investment use.
"""
    )

    user_cols = st.columns(3)
    user_cols[0].metric("Target Users", "Sell-side / buy-side analysts")
    user_cols[1].metric("Industry Focus", "Pharma CRDMO / CRO-CDMO")
    user_cols[2].metric("Workflow Style", "Human-in-the-loop valuation")


def load_peer_data() -> pd.DataFrame:
    return pd.read_csv(SAMPLE_PEERS_PATH)


def render_ratio_chart(metrics_df: pd.DataFrame) -> None:
    margin_df = metrics_df[
        ["year", "gross_margin", "operating_margin", "net_margin", "fcf_margin"]
    ].melt("year", var_name="metric", value_name="value")

    chart = (
        alt.Chart(margin_df)
        .mark_line(point=True)
        .encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y("value:Q", title="Margin", axis=alt.Axis(format="%")),
            color=alt.Color("metric:N", title="Metric"),
            tooltip=["year:O", "metric:N", alt.Tooltip("value:Q", format=".1%")],
        )
        .properties(height=320)
    )
    st.altair_chart(chart, width="stretch")


def render_revenue_chart(metrics_df: pd.DataFrame) -> None:
    chart = (
        alt.Chart(metrics_df)
        .mark_bar(color="#2b6cb0")
        .encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y("revenue:Q", title="Revenue (RMB mn)"),
            tooltip=["year:O", alt.Tooltip("revenue:Q", format=",.0f")],
        )
        .properties(height=320)
    )
    st.altair_chart(chart, width="stretch")


def render_fcf_chart(dcf_df: pd.DataFrame) -> None:
    chart = (
        alt.Chart(dcf_df)
        .mark_line(point=True, color="#c05621")
        .encode(
            x=alt.X("year:O", title="Forecast Year"),
            y=alt.Y("free_cash_flow:Q", title="FCF (RMB mn)"),
            tooltip=["year:O", alt.Tooltip("free_cash_flow:Q", format=",.2f")],
        )
        .properties(height=320)
    )
    st.altair_chart(chart, width="stretch")


def main() -> None:
    render_landing_page()

    with st.sidebar:
        st.header("Company Input")
        company_name = st.text_input("Company name", value="WuXi AppTec")
        ticker = st.text_input("Ticker", value="603259.SH / 2359.HK")
        industry_segment = st.text_input(
            "Industry segment",
            value="Pharmaceutical CRDMO / CRO-CDMO",
        )
        uploaded_file = st.file_uploader(
            "Upload financial CSV",
            type=["csv"],
            help="If no file is uploaded, the bundled WuXi AppTec verified historical dataset is used.",
        )

    financial_source = uploaded_file if uploaded_file is not None else SAMPLE_FINANCIALS_PATH
    financial_df = load_financial_data(financial_source)
    peer_df = load_peer_data()
    metrics_df = calculate_historical_metrics(financial_df)
    ratio_df = build_ratio_table(metrics_df)
    summary = build_analysis_summary(metrics_df)
    trend_summary = summarize_financial_trends(metrics_df)

    st.subheader("Data Collection")
    st.info(
        "This run is using bundled WuXi AppTec historical data sourced from official company disclosures unless you uploaded a replacement CSV. "
        "Please still cross-check the figures and cite the underlying filings in your final submission."
    )
    st.dataframe(financial_df, width="stretch")

    st.subheader("Historical Financial Analysis")
    metric_cols = st.columns(4)
    metric_cols[0].metric("Latest Revenue", f"RMB {summary.latest_revenue:,.0f} mn")
    metric_cols[1].metric("Operating Margin", f"{summary.latest_operating_margin:.1%}")
    metric_cols[2].metric("Net Margin", f"{summary.latest_net_margin:.1%}")
    metric_cols[3].metric("Backlog Growth", f"{summary.latest_backlog_growth:.1%}")

    st.markdown("Historical ratio table")
    display_ratio_df = format_percentage_columns(
        ratio_df,
        [
            "revenue_growth",
            "gross_margin",
            "operating_margin",
            "net_margin",
            "debt_ratio",
            "fcf_margin",
            "backlog_growth",
        ],
    )
    st.dataframe(display_ratio_df, width="stretch")

    chart_cols = st.columns(2)
    with chart_cols[0]:
        st.markdown("Revenue trend")
        render_revenue_chart(metrics_df)
    with chart_cols[1]:
        st.markdown("Margin trend")
        render_ratio_chart(metrics_df)

    st.subheader("Industry-Specific CRDMO Analysis")
    st.markdown(
        "This section mixes automated indicators with analyst judgement, reflecting how a research product should support rather than replace coverage analysts."
    )

    industry_cols = st.columns(2)
    with industry_cols[0]:
        demand_signal = st.select_slider(
            "Customer demand from pharma / biotech R&D",
            options=["Weak", "Soft", "Stable", "Healthy", "Strong"],
            value="Stable",
        )
        capacity_utilisation = st.select_slider(
            "Capacity utilisation",
            options=["Low", "Moderate", "Balanced", "Tight"],
            value="Balanced",
        )
        margin_resilience = st.select_slider(
            "Margin resilience",
            options=["Fragile", "Mixed", "Resilient"],
            value="Mixed",
        )
    with industry_cols[1]:
        regulatory_risk = st.select_slider(
            "Overseas regulatory / geopolitical risk",
            options=["Low", "Moderate", "Elevated", "High"],
            value="Elevated",
        )
        customer_concentration = st.select_slider(
            "Customer concentration risk",
            options=["Low", "Moderate", "Elevated"],
            value="Moderate",
        )
        st.metric("Automated backlog growth", f"{summary.latest_backlog_growth:.1%}")

    st.markdown("Sample peer context")
    st.dataframe(peer_df, width="stretch")

    st.subheader("Human-in-the-Loop Valuation Assumption Setting")
    st.caption(
        "Default values are intentionally editable. Analysts should challenge assumptions before accepting the model output."
    )

    latest_revenue = float(metrics_df.iloc[-1]["revenue"])
    latest_fcf_margin = float(metrics_df.iloc[-1]["fcf_margin"])

    assumption_cols = st.columns(4)
    growth_rates = []
    default_growths = [12.0, 11.0, 10.0, 9.0, 8.0]
    for idx in range(5):
        growth_rates.append(
            assumption_cols[idx % 4].number_input(
                f"Revenue growth Year {idx + 1} (%)",
                min_value=-20.0,
                max_value=60.0,
                value=default_growths[idx],
                step=0.5,
            )
            / 100
        )

    assumption_cols_2 = st.columns(4)
    ebit_margin = (
        assumption_cols_2[0].number_input(
            "Target EBIT margin (%)",
            min_value=0.0,
            max_value=60.0,
            value=16.0,
            step=0.5,
        )
        / 100
    )
    tax_rate = (
        assumption_cols_2[1].number_input(
            "Tax rate (%)",
            min_value=0.0,
            max_value=40.0,
            value=15.0,
            step=0.5,
        )
        / 100
    )
    wacc = (
        assumption_cols_2[2].number_input(
            "WACC / discount rate (%)",
            min_value=1.0,
            max_value=25.0,
            value=9.0,
            step=0.5,
        )
        / 100
    )
    terminal_growth = (
        assumption_cols_2[3].number_input(
            "Terminal growth rate (%)",
            min_value=0.0,
            max_value=8.0,
            value=3.0,
            step=0.25,
        )
        / 100
    )

    assumption_cols_3 = st.columns(3)
    net_debt = assumption_cols_3[0].number_input(
        "Net debt (RMB mn)",
        min_value=-50000.0,
        max_value=100000.0,
        value=1500.0,
        step=100.0,
    )
    shares_outstanding = assumption_cols_3[1].number_input(
        "Shares outstanding (mn)",
        min_value=1.0,
        max_value=10000.0,
        value=2960.0,
        step=10.0,
    )
    use_fcf_margin = assumption_cols_3[2].checkbox(
        "Use FCF margin override",
        value=False,
        help="If unchecked, the simplified DCF uses NOPAT as free cash flow.",
    )
    fcf_margin_override = None
    if use_fcf_margin:
        fcf_margin_override = (
            st.slider(
                "FCF margin override (%)",
                min_value=0.0,
                max_value=40.0,
                value=float(round(latest_fcf_margin * 100, 1)),
                step=0.5,
            )
            / 100
        )

    try:
        dcf_df, valuation_outputs = run_dcf_valuation(
            latest_revenue=latest_revenue,
            growth_rates=growth_rates,
            ebit_margin=ebit_margin,
            tax_rate=tax_rate,
            wacc=wacc,
            terminal_growth=terminal_growth,
            net_debt=net_debt,
            shares_outstanding=shares_outstanding,
            fcf_margin_override=fcf_margin_override,
        )
        sensitivity_df = build_sensitivity_table(
            latest_revenue=latest_revenue,
            growth_rates=growth_rates,
            ebit_margin=ebit_margin,
            tax_rate=tax_rate,
            net_debt=net_debt,
            shares_outstanding=shares_outstanding,
            base_wacc=wacc,
            base_terminal_growth=terminal_growth,
            fcf_margin_override=fcf_margin_override,
        )
    except ValueError as error:
        st.error(str(error))
        return

    st.subheader("DCF Valuation")
    valuation_cols = st.columns(3)
    valuation_cols[0].metric(
        "Enterprise Value",
        f"RMB {valuation_outputs['enterprise_value']:,.0f} mn",
    )
    valuation_cols[1].metric(
        "Equity Value",
        f"RMB {valuation_outputs['equity_value']:,.0f} mn",
    )
    valuation_cols[2].metric(
        "Fair Value / Share",
        f"RMB {valuation_outputs['fair_value_per_share']:,.2f}",
    )

    st.markdown("DCF forecast table")
    st.dataframe(format_dcf_table(dcf_df), width="stretch")

    dcf_chart_col, sensitivity_col = st.columns(2)
    with dcf_chart_col:
        st.markdown("Forecast free cash flow")
        render_fcf_chart(dcf_df)
    with sensitivity_col:
        st.markdown("Valuation sensitivity table")
        st.dataframe(sensitivity_df.round(2), width="stretch")

    st.subheader("Output Generation")
    assumptions = {
        "growth_rates": growth_rates,
        "ebit_margin": ebit_margin,
        "tax_rate": tax_rate,
        "wacc": wacc,
        "terminal_growth": terminal_growth,
        "net_debt": net_debt,
        "shares_outstanding": shares_outstanding,
        "fcf_margin_override": fcf_margin_override,
    }
    industry_inputs = {
        "demand_signal": demand_signal,
        "capacity_utilisation": capacity_utilisation,
        "margin_resilience": margin_resilience,
        "regulatory_risk": regulatory_risk,
        "customer_concentration": customer_concentration,
    }
    narratives = build_narrative_sections(
        company_name=company_name,
        industry_segment=industry_segment,
        financial_trends=trend_summary,
        assumptions=assumptions,
        valuation_outputs=valuation_outputs,
        industry_inputs=industry_inputs,
    )
    report_markdown = generate_report_markdown(
        company_name=company_name,
        ticker=ticker,
        industry_segment=industry_segment,
        metrics_df=metrics_df,
        peer_df=peer_df,
        dcf_df=dcf_df.round(2),
        valuation_outputs=valuation_outputs,
        sensitivity_df=sensitivity_df.round(2),
        assumptions=assumptions,
        industry_inputs=industry_inputs,
        narrative_sections=narratives,
    )

    st.markdown("Generated analyst commentary")
    st.markdown(report_markdown)

    export_cols = st.columns(2)
    export_cols[0].download_button(
        "Export Markdown",
        data=report_markdown,
        file_name="crdmo_analyst_copilot_output.md",
        mime="text/markdown",
    )
    export_cols[1].download_button(
        "Export Text",
        data=report_markdown,
        file_name="crdmo_analyst_copilot_output.txt",
        mime="text/plain",
    )

    with st.expander("Prompt Library"):
        st.markdown(
            "The following prompt templates support a multi-agent orchestration design for Coze or XIPU AI."
        )
        for prompt_key in PROMPT_LIBRARY:
            st.code(render_prompt_card(prompt_key), language="markdown")


if __name__ == "__main__":
    main()
