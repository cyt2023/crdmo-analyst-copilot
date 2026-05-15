from __future__ import annotations

from typing import Sequence

import numpy as np
import pandas as pd


DEFAULT_GROWTH_RATES = [0.12, 0.11, 0.10, 0.09, 0.08]


def normalize_growth_rates(growth_rates: Sequence[float]) -> list[float]:
    rates = list(growth_rates)
    if len(rates) != 5:
        raise ValueError("Exactly five forecast revenue growth rates are required.")
    return rates


def run_dcf_valuation(
    latest_revenue: float,
    growth_rates: Sequence[float],
    ebit_margin: float,
    tax_rate: float,
    wacc: float,
    terminal_growth: float,
    net_debt: float,
    shares_outstanding: float,
    fcf_margin_override: float | None = None,
) -> tuple[pd.DataFrame, dict[str, float]]:
    rates = normalize_growth_rates(growth_rates)
    if wacc <= terminal_growth:
        raise ValueError("WACC must be greater than terminal growth in a Gordon Growth model.")
    if shares_outstanding <= 0:
        raise ValueError("Shares outstanding must be greater than zero.")

    forecast_rows = []
    prior_revenue = latest_revenue
    discounted_fcf_sum = 0.0

    for index, growth_rate in enumerate(rates, start=1):
        revenue = prior_revenue * (1 + growth_rate)
        ebit = revenue * ebit_margin
        tax = ebit * tax_rate
        nopat = ebit * (1 - tax_rate)
        free_cash_flow = revenue * fcf_margin_override if fcf_margin_override is not None else nopat
        discounted_fcf = free_cash_flow / ((1 + wacc) ** index)
        discounted_fcf_sum += discounted_fcf

        forecast_rows.append(
            {
                "year": f"Year {index}",
                "growth_rate": growth_rate,
                "forecast_revenue": revenue,
                "ebit": ebit,
                "tax": tax,
                "nopat": nopat,
                "free_cash_flow": free_cash_flow,
                "discounted_fcf": discounted_fcf,
            }
        )
        prior_revenue = revenue

    forecast_df = pd.DataFrame(forecast_rows)
    terminal_cash_flow = forecast_df.iloc[-1]["free_cash_flow"] * (1 + terminal_growth)
    terminal_value = terminal_cash_flow / (wacc - terminal_growth)
    discounted_terminal_value = terminal_value / ((1 + wacc) ** len(rates))
    enterprise_value = discounted_fcf_sum + discounted_terminal_value
    equity_value = enterprise_value - net_debt
    fair_value_per_share = equity_value / shares_outstanding

    outputs = {
        "terminal_value": terminal_value,
        "discounted_terminal_value": discounted_terminal_value,
        "enterprise_value": enterprise_value,
        "equity_value": equity_value,
        "fair_value_per_share": fair_value_per_share,
        "net_debt": net_debt,
        "shares_outstanding": shares_outstanding,
        "wacc": wacc,
        "terminal_growth": terminal_growth,
        "target_ebit_margin": ebit_margin,
        "tax_rate": tax_rate,
    }
    return forecast_df, outputs


def build_sensitivity_table(
    latest_revenue: float,
    growth_rates: Sequence[float],
    ebit_margin: float,
    tax_rate: float,
    net_debt: float,
    shares_outstanding: float,
    base_wacc: float,
    base_terminal_growth: float,
    fcf_margin_override: float | None = None,
) -> pd.DataFrame:
    wacc_range = [base_wacc - 0.01, base_wacc, base_wacc + 0.01]
    terminal_growth_range = [
        base_terminal_growth - 0.01,
        base_terminal_growth,
        base_terminal_growth + 0.01,
    ]

    table = {}
    for terminal_growth in terminal_growth_range:
        column_name = f"g={terminal_growth:.1%}"
        values = []
        for wacc in wacc_range:
            if wacc <= terminal_growth:
                values.append(np.nan)
                continue
            _, outputs = run_dcf_valuation(
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
            values.append(outputs["fair_value_per_share"])
        table[column_name] = values

    sensitivity_df = pd.DataFrame(table, index=[f"WACC={wacc:.1%}" for wacc in wacc_range])
    sensitivity_df.index.name = "Assumption"
    return sensitivity_df.reset_index()


def format_dcf_table(dcf_df: pd.DataFrame) -> pd.DataFrame:
    formatted = dcf_df.copy()
    percentage_columns = ["growth_rate"]
    numeric_columns = [
        "forecast_revenue",
        "ebit",
        "tax",
        "nopat",
        "free_cash_flow",
        "discounted_fcf",
    ]

    for column in percentage_columns:
        formatted[column] = formatted[column].map(lambda value: f"{value:.1%}")
    for column in numeric_columns:
        formatted[column] = formatted[column].map(lambda value: round(value, 2))
    return formatted
