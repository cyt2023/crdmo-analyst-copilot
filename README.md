# CRDMO Analyst Copilot

[中文说明 / Chinese README](README_CN.md)

CRDMO Analyst Copilot is a prototype AI equity research valuation agent built for the ACC102 group coursework project:

**AI Equity Research Valuation Agent for the Pharmaceutical CRDMO Industry: A Case Study of WuXi AppTec**

The prototype is designed for brokerage-style equity research analysts covering pharmaceutical outsourcing companies. It demonstrates an end-to-end workflow that combines automation with analyst judgement:

1. Company input
2. Data collection
3. Historical financial analysis
4. Human-in-the-loop assumption setting
5. DCF valuation
6. Report-style output generation

## Project Purpose

This repository is intended to show how an industry-focused AI workflow can support equity research analysts rather than replace them. The product is tailored to the pharmaceutical CRDMO / CRO-CDMO industry, where backlog visibility, project mix, client funding conditions, capacity utilisation, compliance standards, and geopolitical risk all influence valuation outcomes.

## Important Data Disclaimer

The bundled WuXi AppTec dataset now contains **verified historical figures for 2019-2023 sourced from official company disclosures**. It is suitable for coursework prototyping, but you should still independently cross-check the original filings before final submission or any real investment use.

Key source types used or recommended for cross-checking include:

- WuXi AppTec annual reports
- WuXi AppTec interim or quarterly reports
- Official annual results presentations
- Official exchange filings

## Repository Structure

```text
/README.md
/app/streamlit_app.py
/app/valuation_model.py
/app/financial_analysis.py
/app/report_generator.py
/app/prompts.py
/data/wuxi_financials_sample.csv
/data/peer_companies_sample.csv
/docs/prompt_and_orchestration_documentation.md
/docs/user_guide.md
/docs/demo_video_script.md
/docs/coze_workflow_spec.md
/docs/ai_usage_disclosure.md
/docs/wuxi_data_sources.md
/outputs/sample_output_pack.md
/outputs/sample_dcf_table.csv
/outputs/sample_financial_ratios.csv
/requirements.txt
```

## Features

- Streamlit interface with a landing page and company input form
- Verified historical WuXi dataset mode or CSV upload mode
- Historical financial ratio analysis
- CRDMO-specific qualitative analysis inputs
- Analyst-editable DCF assumptions
- DCF valuation forecast and sensitivity table
- Markdown/text report export
- Prompt library for agent roles
- Coze / XIPU-AI-ready workflow documentation
- WuXi AppTec source note for the bundled historical dataset

## Streamlit App Workflow

The Streamlit app in [app/streamlit_app.py](/Users/cyt/Desktop/lkh-/app/streamlit_app.py) follows the required workflow:

1. Analyst enters company name, ticker, and industry segment
2. Analyst uploads a CSV or uses the bundled WuXi AppTec historical dataset
3. System calculates historical growth, margin, liquidity, leverage, efficiency, and cash flow ratios
4. Analyst reviews CRDMO operating signals such as demand, utilisation, and risk factors
5. Analyst sets or edits DCF assumptions
6. System generates forecast tables, sensitivity analysis, and commentary
7. Analyst exports the result as Markdown or plain text

## Financial Formulas Used

Historical ratios:

- `revenue_growth = revenue / previous_year_revenue - 1`
- `gross_margin = gross_profit / revenue`
- `operating_margin = operating_profit / revenue`
- `net_margin = net_profit / revenue`
- `current_ratio = current_assets / current_liabilities`
- `debt_ratio = total_liabilities / total_assets`
- `asset_turnover = revenue / total_assets`
- `fcf_margin = free_cash_flow / revenue`

DCF model:

- `forecast_revenue_t = previous_revenue * (1 + growth_rate_t)`
- `EBIT_t = forecast_revenue_t * EBIT_margin`
- `NOPAT_t = EBIT_t * (1 - tax_rate)`
- `FCF_t = NOPAT_t` by default, or analyst may apply an FCF margin override
- `discounted_FCF_t = FCF_t / (1 + WACC)^t`
- `terminal_value = FCF_5 * (1 + terminal_growth) / (WACC - terminal_growth)`
- `enterprise_value = sum(discounted_FCF) + discounted_terminal_value`
- `equity_value = enterprise_value - net_debt`
- `fair_value_per_share = equity_value / shares_outstanding`

## How To Run

1. Create a Python environment if desired.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Launch the app:

```bash
streamlit run app/streamlit_app.py
```

## Suggested Coursework Demonstration Flow

1. Open the landing page and explain the target users.
2. Show the company input section for WuXi AppTec.
3. Use the bundled verified historical dataset to demonstrate the workflow.
4. Walk through the historical ratio analysis.
5. Explain why CRDMO-specific qualitative factors matter.
6. Adjust one or two DCF assumptions live.
7. Show the DCF result and valuation sensitivity table.
8. Export the generated sample output.
9. Conclude with limitations and next-step improvements.

## Limitations

- Uses verified historical WuXi AppTec figures, but still relies on simplified modelling assumptions
- Uses a simplified DCF structure
- Does not connect to real-time APIs or live market data
- Does not automate full source verification
- Requires analyst judgement for assumptions and final interpretation
- Cannot replace full professional equity research workflow, compliance review, or investment advice

## Recommended Final Submission Edits

Before submitting, your group should:

- Add explicit source citations for the bundled WuXi AppTec figures
- Add citations to annual reports and trusted databases
- Tailor the final language to your lecturer’s marking rubric
- Add screenshots from your running Streamlit app
- Record the demo video using the script in [docs/demo_video_script.md](/Users/cyt/Desktop/lkh-/docs/demo_video_script.md)

## Coursework Positioning

This project is strongest when framed as a practical research support tool for an analyst team. The key value is not “AI replaces analysis,” but “AI structures the workflow, accelerates repetitive steps, and preserves human judgement where valuation quality depends on industry knowledge.”
