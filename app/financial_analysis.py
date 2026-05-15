from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd


REQUIRED_FINANCIAL_COLUMNS = [
    "year",
    "revenue",
    "gross_profit",
    "operating_profit",
    "net_profit",
    "total_assets",
    "total_liabilities",
    "current_assets",
    "current_liabilities",
    "operating_cash_flow",
    "capex",
    "free_cash_flow",
    "backlog",
]


@dataclass
class AnalysisSummary:
    latest_year: int
    latest_revenue: float
    latest_operating_margin: float
    latest_net_margin: float
    latest_backlog: float
    latest_backlog_growth: float


def load_financial_data(file_obj: str | bytes | None = None) -> pd.DataFrame:
    """Load uploaded or local CSV financial data."""
    if file_obj is None:
        raise ValueError("A file path or file-like object is required.")

    df = pd.read_csv(file_obj)
    return validate_financial_data(df)


def validate_financial_data(df: pd.DataFrame) -> pd.DataFrame:
    missing_columns = [col for col in REQUIRED_FINANCIAL_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(
            "Financial data is missing required columns: "
            + ", ".join(missing_columns)
        )

    numeric_columns = [col for col in REQUIRED_FINANCIAL_COLUMNS if col != "year"]
    cleaned = df.copy()
    cleaned["year"] = cleaned["year"].astype(int)
    for column in numeric_columns:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    if cleaned[numeric_columns].isna().any().any():
        raise ValueError("Financial data contains non-numeric values in numeric columns.")

    return cleaned.sort_values("year").reset_index(drop=True)


def calculate_historical_metrics(df: pd.DataFrame) -> pd.DataFrame:
    metrics = df.copy()
    previous_revenue = metrics["revenue"].shift(1)
    previous_backlog = metrics["backlog"].shift(1)

    metrics["revenue_growth"] = np.where(
        previous_revenue > 0,
        metrics["revenue"] / previous_revenue - 1,
        np.nan,
    )
    metrics["gross_margin"] = metrics["gross_profit"] / metrics["revenue"]
    metrics["operating_margin"] = metrics["operating_profit"] / metrics["revenue"]
    metrics["net_margin"] = metrics["net_profit"] / metrics["revenue"]
    metrics["current_ratio"] = metrics["current_assets"] / metrics["current_liabilities"]
    metrics["debt_ratio"] = metrics["total_liabilities"] / metrics["total_assets"]
    metrics["asset_turnover"] = metrics["revenue"] / metrics["total_assets"]
    metrics["fcf_margin"] = metrics["free_cash_flow"] / metrics["revenue"]
    metrics["backlog_growth"] = np.where(
        previous_backlog > 0,
        metrics["backlog"] / previous_backlog - 1,
        np.nan,
    )

    return metrics


def build_analysis_summary(metrics_df: pd.DataFrame) -> AnalysisSummary:
    latest = metrics_df.iloc[-1]
    return AnalysisSummary(
        latest_year=int(latest["year"]),
        latest_revenue=float(latest["revenue"]),
        latest_operating_margin=float(latest["operating_margin"]),
        latest_net_margin=float(latest["net_margin"]),
        latest_backlog=float(latest["backlog"]),
        latest_backlog_growth=float(latest["backlog_growth"])
        if pd.notna(latest["backlog_growth"])
        else 0.0,
    )


def build_ratio_table(metrics_df: pd.DataFrame) -> pd.DataFrame:
    ratio_columns = [
        "year",
        "revenue_growth",
        "gross_margin",
        "operating_margin",
        "net_margin",
        "current_ratio",
        "debt_ratio",
        "asset_turnover",
        "fcf_margin",
        "backlog_growth",
    ]
    return metrics_df[ratio_columns].copy()


def summarize_financial_trends(metrics_df: pd.DataFrame) -> dict[str, str]:
    latest = metrics_df.iloc[-1]
    earliest = metrics_df.iloc[0]
    revenue_cagr = calculate_cagr(
        earliest["revenue"],
        latest["revenue"],
        len(metrics_df) - 1,
    )

    latest_growth = latest["revenue_growth"] if pd.notna(latest["revenue_growth"]) else 0.0
    latest_backlog_growth = (
        latest["backlog_growth"] if pd.notna(latest["backlog_growth"]) else 0.0
    )

    return {
        "revenue": (
            f"Sample revenue grew from RMB {earliest['revenue']:,.0f} million in "
            f"{int(earliest['year'])} to RMB {latest['revenue']:,.0f} million in "
            f"{int(latest['year'])}, implying a sample CAGR of {revenue_cagr:.1%}. "
            f"The latest one-year growth rate is {latest_growth:.1%}."
        ),
        "profitability": (
            f"Latest sample gross, operating, and net margins are "
            f"{latest['gross_margin']:.1%}, {latest['operating_margin']:.1%}, and "
            f"{latest['net_margin']:.1%}, respectively."
        ),
        "liquidity": (
            f"The latest sample current ratio is {latest['current_ratio']:.2f}x and "
            f"debt ratio is {latest['debt_ratio']:.1%}, which helps frame near-term "
            f"balance sheet flexibility."
        ),
        "cash_flow": (
            f"The latest sample free cash flow margin is {latest['fcf_margin']:.1%}. "
            f"This prototype uses free cash flow as the core DCF cash driver."
        ),
        "backlog": (
            f"Latest sample backlog is RMB {latest['backlog']:,.0f} million with "
            f"year-on-year growth of {latest_backlog_growth:.1%}. In CRDMO coverage, "
            f"backlog helps indicate demand visibility and capacity planning discipline."
        ),
    }


def format_percentage_columns(
    df: pd.DataFrame,
    percentage_columns: Iterable[str],
    decimal_places: int = 1,
) -> pd.DataFrame:
    formatted = df.copy()
    for column in percentage_columns:
        formatted[column] = formatted[column].apply(
            lambda value: ""
            if pd.isna(value)
            else f"{value * 100:.{decimal_places}f}%"
        )
    return formatted


def calculate_cagr(start_value: float, end_value: float, periods: int) -> float:
    if start_value <= 0 or periods <= 0:
        return 0.0
    return (end_value / start_value) ** (1 / periods) - 1
