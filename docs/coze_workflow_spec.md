# Coze Workflow Specification

## Overview

This document describes a Coze / XIPU-AI-ready workflow for implementing the CRDMO Analyst Copilot prototype as a node-based orchestration. The workflow is designed so that it can be recreated manually inside a low-code AI workflow builder.

The design objective is to support an equity research analyst covering pharmaceutical CRDMO companies, with WuXi AppTec used as the main case example.

## Workflow Logic

The workflow follows nine nodes:

1. Start Node
2. Data Collection Node
3. Financial Ratio Calculation Node
4. Industry Analysis Node
5. Human Assumption Review Node
6. DCF Calculation Node
7. Risk Review Node
8. Report Generation Node
9. Final Output Node

## Node Specification

### 1. Start Node

**Purpose**  
Receive the main user request and initialise workflow variables.

**Input**

- `company_name`
- `ticker`
- `industry_segment`
- optional uploaded financial CSV

**Output**

- standardised workflow context object

**Prompt**  
No LLM prompt required. This is a form intake or API input node.

**Automation Status**  
Automated

### 2. Data Collection Node

**Purpose**  
Load the uploaded CSV or fallback bundled historical dataset and validate required fields.

**Input**

- workflow context object
- uploaded file or bundled historical data path

**Output**

- validated financial dataset
- peer comparison table
- data quality warning plus source reminder if the bundled dataset is being used

**Prompt**

“Check whether the uploaded dataset contains the required CRDMO financial columns. If no file is uploaded, load the bundled WuXi AppTec historical dataset sourced from official company disclosures. Remind the user to cite the original filings and not to treat the dataset as a substitute for source verification.”

**Automation Status**  
Automated

### 3. Financial Ratio Calculation Node

**Purpose**  
Calculate historical financial ratios and summary indicators.

**Input**

- validated financial dataset

**Output**

- historical ratio table
- summary metrics
- chart-ready data structures

**Prompt**

“Using the supplied historical financial data, calculate revenue growth, gross margin, operating margin, net margin, current ratio, debt ratio, asset turnover, free cash flow margin, and backlog growth. Follow the predefined formulas exactly. Do not invent missing values.”

**Automation Status**  
Automated

### 4. Industry Analysis Node

**Purpose**  
Generate industry commentary tailored to the pharmaceutical CRDMO / CRO-CDMO sector.

**Input**

- company name
- ticker
- industry segment
- peer table
- historical metrics
- analyst notes if any

**Output**

- industry analysis text
- key industry watchpoints

**Prompt**

“Act as an Industry Analyst Agent for the pharmaceutical CRDMO / CRO-CDMO industry. Explain demand drivers, outsourcing trends, backlog visibility, capacity utilisation, pricing discipline, margin resilience, and geopolitical or regulatory risks. Use only supplied facts. If a figure is not provided, do not invent it. Separate historical disclosed data from analyst interpretation.”

**Automation Status**  
Automated draft, then user review recommended

### 5. Human Assumption Review Node

**Purpose**  
Allow the analyst to inspect and edit forward valuation assumptions before DCF calculation.

**Input**

- latest historical revenue
- latest margins
- latest FCF margin
- draft default assumptions

**Output**

- analyst-confirmed assumptions

**Prompt**

“Present default assumptions for revenue growth in Years 1-5, target EBIT margin, tax rate, WACC, terminal growth, net debt, shares outstanding, and optional FCF margin override. Require the analyst to confirm or edit these values before continuing.”

**Automation Status**  
Requires user confirmation

### 6. DCF Calculation Node

**Purpose**  
Run the DCF valuation using analyst-confirmed inputs.

**Input**

- analyst-confirmed assumptions
- latest historical revenue

**Output**

- DCF forecast table
- valuation outputs
- sensitivity table

**Prompt**

“Calculate a five-year DCF using the confirmed assumptions. Forecast revenue, EBIT, tax, NOPAT, free cash flow, discounted free cash flow, terminal value, enterprise value, equity value, and fair value per share. Use NOPAT as free cash flow unless the analyst has provided an FCF margin override. Do not change user assumptions.”

**Automation Status**  
Automated

### 7. Risk Review Node

**Purpose**  
Review the draft output for risk factors and process limitations.

**Input**

- industry analysis
- financial analysis
- valuation outputs
- assumptions

**Output**

- key risks
- limitations
- suggested human review points

**Prompt**

“Act as a Risk Review Agent. Identify the most important risks affecting a pharmaceutical CRDMO valuation, including data quality risk, assumption sensitivity, regulatory risk, geopolitical risk, customer concentration, margin pressure, and utilisation risk where relevant. Do not invent unsupported facts. Separate factual data limitations from forward-looking scenario risks.”

**Automation Status**  
Automated draft, then user review recommended

### 8. Report Generation Node

**Purpose**  
Combine the outputs into a final research-style report.

**Input**

- company input
- financial analysis
- industry analysis
- DCF outputs
- risk review

**Output**

- final report in Markdown or rich text format

**Prompt**

“Act as a Report Editor Agent. Assemble the inputs into a coherent equity research briefing with sections for executive summary, industry analysis, company analysis, financial analysis, valuation analysis, key risks, and limitations. Use professional but student-friendly English. Preserve all labels for historical data, source limitations, and analyst assumptions.”

**Automation Status**  
Automated draft, optional final user review

### 9. Final Output Node

**Purpose**  
Display the final report and support export.

**Input**

- final report
- DCF table
- ratio table
- sensitivity table

**Output**

- on-screen report
- Markdown export
- text export

**Prompt**  
No LLM prompt required. This is a display and export node.

**Automation Status**  
Automated

## Data Objects Passed Between Nodes

- `company_context`
- `financial_dataset`
- `historical_metrics`
- `peer_context`
- `assumption_set`
- `dcf_outputs`
- `risk_review`
- `final_report`

## Human Checkpoints

The most important manual checkpoints are:

1. Confirm whether the data source is the bundled historical dataset or a user-uploaded replacement
2. Review historical results for reasonableness
3. Edit forecast and valuation assumptions
4. Review risk commentary before final export
5. Ensure the final report clearly distinguishes fact, source-based historical data, and assumptions

## Why This Workflow Fits Coze Or XIPU AI

- Each stage can be represented as a distinct node
- Prompted agent roles are easy to map into LLM blocks
- Human approval can be inserted before the valuation node
- Final outputs can be assembled into a report artifact
- The structure is transparent enough for coursework explanation and grading

## Suggested Future Upgrade Nodes

- Source citation node
- Peer multiple valuation node
- Base / bull / bear scenario node
- News and regulatory monitoring node
- Compliance disclaimer node
