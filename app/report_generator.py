from __future__ import annotations

from typing import Any

import pandas as pd


def _format_currency(value: float) -> str:
    return f"RMB {value:,.2f} million"


def _format_percent(value: float) -> str:
    return f"{value:.1%}"


def _format_share_value(value: float) -> str:
    return f"RMB {value:,.2f} per share"


def generate_report_markdown(
    company_name: str,
    ticker: str,
    industry_segment: str,
    metrics_df: pd.DataFrame,
    peer_df: pd.DataFrame,
    dcf_df: pd.DataFrame,
    valuation_outputs: dict[str, float],
    sensitivity_df: pd.DataFrame,
    assumptions: dict[str, Any],
    industry_inputs: dict[str, Any],
    narrative_sections: dict[str, Any],
) -> str:
    latest = metrics_df.iloc[-1]
    latest_year = int(latest["year"])

    markdown = f"""# CRDMO Analyst Copilot Sample Output

## Project Context
- Target company: {company_name} ({ticker})
- Industry segment: {industry_segment}
- Data status: Sample prototype dataset only. Replace with verified figures from annual reports or trusted databases before academic submission or investment use.

## Executive Summary
CRDMO Analyst Copilot is a prototype equity research valuation workflow for brokerage-style coverage of pharmaceutical outsourcing companies. For this sample run on {company_name}, the system combines historical sample data analysis, analyst-reviewed assumptions, and a simplified DCF model to produce an indicative fair value per share of {_format_share_value(valuation_outputs['fair_value_per_share'])}.

The latest sample year in the prototype is {latest_year}. Revenue is {_format_currency(latest['revenue'])}, operating margin is {_format_percent(latest['operating_margin'])}, and backlog is {_format_currency(latest['backlog'])}. The workflow is designed to automate repetitive calculations while preserving human checkpoints for assumptions, risk judgement, and final report editing.

## Industry Analysis
{narrative_sections['industry_analysis']}

Analyst-selected CRDMO operating signals in this run:
- Backlog growth signal: {_format_percent(latest['backlog_growth']) if pd.notna(latest['backlog_growth']) else 'N/A'}
- Pharma and biotech R&D demand: {industry_inputs['demand_signal']}
- Capacity utilisation: {industry_inputs['capacity_utilisation']}
- Margin resilience: {industry_inputs['margin_resilience']}
- Overseas regulatory and geopolitical risk: {industry_inputs['regulatory_risk']}
- Customer concentration risk: {industry_inputs['customer_concentration']}

## Company Analysis
{narrative_sections['company_analysis']}

## Financial Analysis
{narrative_sections['financial_analysis']}

## Valuation Analysis
{narrative_sections['valuation_analysis']}

Key valuation outputs:
- Enterprise value: {_format_currency(valuation_outputs['enterprise_value'])}
- Equity value: {_format_currency(valuation_outputs['equity_value'])}
- Implied fair value per share: {_format_share_value(valuation_outputs['fair_value_per_share'])}
- WACC: {_format_percent(valuation_outputs['wacc'])}
- Terminal growth: {_format_percent(valuation_outputs['terminal_growth'])}
- Target EBIT margin: {_format_percent(valuation_outputs['target_ebit_margin'])}
- Tax rate: {_format_percent(valuation_outputs['tax_rate'])}

## Key Risks
{narrative_sections['risk_review']}

## Limitations
- This prototype uses sample, clearly labelled non-audited data for demonstration.
- The DCF model is simplified and uses NOPAT or an optional FCF margin as a proxy for free cash flow.
- Valuation outputs are highly sensitive to WACC, terminal growth, and margin assumptions.
- The workflow does not include real-time market data, current share price benchmarking, or live regulatory news.
- CRDMO companies face regulatory, geopolitical, client funding, and utilization risks that require analyst judgement beyond model outputs.

## Historical Financial Table
{metrics_df.to_markdown(index=False)}

## DCF Forecast Table
{dcf_df.to_markdown(index=False)}

## Valuation Sensitivity Table
{sensitivity_df.to_markdown(index=False)}

## Peer Context Table
{peer_df.to_markdown(index=False)}

## Assumption Log
- Forecast revenue growth rates (Y1-Y5): {", ".join(_format_percent(rate) for rate in assumptions['growth_rates'])}
- Target EBIT margin: {_format_percent(assumptions['ebit_margin'])}
- Tax rate: {_format_percent(assumptions['tax_rate'])}
- WACC: {_format_percent(assumptions['wacc'])}
- Terminal growth rate: {_format_percent(assumptions['terminal_growth'])}
- Net debt: {_format_currency(assumptions['net_debt'])}
- Shares outstanding: {assumptions['shares_outstanding']:,.2f} million
- Optional FCF margin override: {(_format_percent(assumptions['fcf_margin_override']) if assumptions['fcf_margin_override'] is not None else 'Not used; FCF approximated with NOPAT')}
"""
    return markdown


def build_narrative_sections(
    company_name: str,
    industry_segment: str,
    financial_trends: dict[str, str],
    assumptions: dict[str, Any],
    valuation_outputs: dict[str, float],
    industry_inputs: dict[str, Any],
) -> dict[str, str]:
    industry_analysis = (
        f"{company_name} operates within the {industry_segment} value chain, where client demand "
        f"is shaped by pharma and biotech R&D outsourcing, project conversion into development "
        f"and manufacturing work, and visibility supported by order backlog. In this prototype run, "
        f"the analyst has assessed demand as {industry_inputs['demand_signal'].lower()}, capacity "
        f"utilisation as {industry_inputs['capacity_utilisation'].lower()}, and margin resilience as "
        f"{industry_inputs['margin_resilience'].lower()}. These factors matter because CRDMO earnings "
        f"quality depends not only on revenue growth but also on utilisation discipline and the mix of "
        f"higher-value projects."
    )
    industry_analysis += (
        f" The model also flags {industry_inputs['regulatory_risk'].lower()} overseas regulatory and "
        f"geopolitical risk together with {industry_inputs['customer_concentration'].lower()} customer "
        f"concentration risk. That framing is important for WuXi-style global platforms because cross-border "
        f"delivery, customer confidence, and compliance perceptions can materially influence backlog conversion."
    )

    company_analysis = (
        f"{company_name} is positioned as an integrated outsourcing platform rather than a single-service "
        f"provider. For an equity research workflow, this means analysts should consider service breadth, "
        f"execution across the discovery-to-manufacturing chain, and the ability to translate scientific "
        f"capability into recurring client demand. Within the prototype, the company case study is analysed "
        f"as a CRDMO name whose investment debate is linked to backlog quality, platform resilience, and "
        f"external policy risk rather than to simple headline growth alone."
    )

    financial_analysis = (
        f"{financial_trends['revenue']} {financial_trends['profitability']} {financial_trends['liquidity']} "
        f"{financial_trends['cash_flow']} {financial_trends['backlog']}"
    )

    valuation_analysis = (
        f"The valuation module applies analyst-reviewed assumptions instead of fully automated forecasts. "
        f"For this run, the model uses a target EBIT margin of {_format_percent(assumptions['ebit_margin'])}, "
        f"a tax rate of {_format_percent(assumptions['tax_rate'])}, a WACC of {_format_percent(assumptions['wacc'])}, "
        f"and terminal growth of {_format_percent(assumptions['terminal_growth'])}. These inputs generate an "
        f"enterprise value of {_format_currency(valuation_outputs['enterprise_value'])} and an implied fair value "
        f"per share of {_format_share_value(valuation_outputs['fair_value_per_share'])}. The result should be read as "
        f"an indicative scenario output rather than a definitive target price because modest changes in discount rate, "
        f"growth, or normalized margins can shift the valuation materially."
    )

    risk_review = (
        "The most important risks in this prototype are assumption sensitivity, sample data limitations, "
        "and sector-specific uncertainty. CRDMO valuations can change quickly if biotech funding weakens, "
        "regulatory scrutiny intensifies, overseas customer sentiment shifts, or newly built capacity is "
        "underutilised. Human analyst review remains necessary to validate source data, challenge management "
        "guidance, and assess whether the chosen WACC, terminal growth, and normalized margins are justified."
    )

    return {
        "industry_analysis": industry_analysis,
        "company_analysis": company_analysis,
        "financial_analysis": financial_analysis,
        "valuation_analysis": valuation_analysis,
        "risk_review": risk_review,
    }
