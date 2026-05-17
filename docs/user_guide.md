# User Guide

## Overview

CRDMO Analyst Copilot is a Streamlit-based prototype for industry-focused AI equity research on pharmaceutical CRDMO companies. The tool is designed to support an analyst workflow rather than provide fully automated investment advice.

## Intended User

The intended user is a brokerage or buy-side analyst covering pharmaceutical outsourcing companies such as CROs, CDMOs, and integrated CRDMO platforms.

## Launch Steps

1. Open a terminal in the project folder.
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:

```bash
streamlit run app/streamlit_app.py
```

## Main Workflow

### 1. Landing Page

The landing page explains:

- product name
- target user group
- industry focus
- prototype limitations

This helps frame the tool as a financial product rather than only a technical demo.

### 2. Company Input

Enter:

- company name
- ticker
- industry segment

For the coursework demonstration, the default values are already set for WuXi AppTec.

### 3. Data Collection

You may:

- upload a CSV file with the required financial columns, or
- use the bundled WuXi AppTec verified historical dataset

Required financial columns:

- `year`
- `revenue`
- `gross_profit`
- `operating_profit`
- `net_profit`
- `total_assets`
- `total_liabilities`
- `current_assets`
- `current_liabilities`
- `operating_cash_flow`
- `capex`
- `free_cash_flow`
- `backlog`

### 4. Historical Financial Analysis

The app calculates:

- revenue growth
- gross margin
- operating margin
- net margin
- current ratio
- debt ratio
- asset turnover
- free cash flow margin
- backlog growth

The ratios are shown in a table and visualised with charts.

### 5. Industry-Specific CRDMO Analysis

The app includes a mixed automated and analyst-review section for:

- backlog growth
- customer demand from pharma / biotech R&D
- capacity utilisation
- margin resilience
- overseas regulatory and geopolitical risk
- customer concentration risk

These factors are especially important in CRDMO analysis because sector outcomes are driven by demand visibility, project mix, asset utilisation, and policy conditions.

### 6. Human-In-The-Loop Valuation Assumptions

The analyst can review and modify:

- forecast revenue growth for Years 1-5
- target EBIT margin
- tax rate
- WACC
- terminal growth rate
- net debt
- shares outstanding
- optional free cash flow margin override

This step is the main human judgement checkpoint in the workflow.

### 7. DCF Valuation

The app produces:

- forecast revenue
- EBIT
- tax
- NOPAT
- free cash flow
- discounted free cash flow
- terminal value
- enterprise value
- equity value
- implied fair value per share

It also shows a WACC versus terminal growth sensitivity table.

### 8. Output Generation

The app assembles a report-style output containing:

- industry analysis
- company analysis
- financial analysis
- valuation commentary
- risks
- limitations
- historical tables
- DCF tables
- sensitivity analysis

### 9. Export

The user can export the generated output as:

- Markdown
- plain text

## Recommended Classroom Demo Tips

- Start with the bundled verified historical data to reduce setup risk
- Explain clearly that the WuXi AppTec historical figures were taken from official disclosures, while peer data and assumptions remain prototype inputs
- Change one assumption live, such as WACC or EBIT margin, to show how analyst judgement changes valuation
- End by discussing limitations and next-step improvements

## Interpretation Guidance

- Do not treat the output as investment advice
- Do not treat the bundled values as a substitute for checking the original filings
- Use the report as a workflow demonstration and analytical structure
- Cite the original WuXi AppTec disclosures in your final coursework submission

## Common Issues

### The app does not start

Check that:

- dependencies were installed successfully
- Streamlit is available in the environment
- you are running the command from the project root

### CSV upload fails

Check that:

- the file is in CSV format
- all required columns are present
- numeric columns contain valid numeric values

### Valuation error appears

The most common reason is:

- `WACC <= terminal growth`

The Gordon Growth formula requires WACC to be higher than terminal growth.
