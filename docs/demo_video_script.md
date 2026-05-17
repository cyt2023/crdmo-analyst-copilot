# Demo Video Script

## Goal

Record a 3-5 minute demonstration showing that the project is a usable industry-focused AI equity research workflow, not only a technical model.

## Suggested Timing

- 0:00-0:30 Introduction
- 0:30-1:10 Product positioning
- 1:10-2:00 Data and financial analysis
- 2:00-3:00 Assumption setting and DCF
- 3:00-4:00 Output and export
- 4:00-4:30 Limitations and conclusion

## Full Script

### 0:00-0:30 Introduction

“Hello everyone. Our project is called CRDMO Analyst Copilot. It is an AI equity research valuation agent designed for the pharmaceutical CRDMO industry, using WuXi AppTec as the case study company. The purpose of the tool is to support analysts through an end-to-end research workflow including company input, data analysis, assumption review, DCF valuation, and report generation.”

### 0:30-1:10 Product Positioning

“The target users are brokerage or buy-side equity research analysts who cover pharmaceutical outsourcing companies such as CROs, CDMOs, and integrated CRDMO platforms. We focused on this industry because it has specific analytical features such as backlog visibility, customer outsourcing demand, capacity utilisation, and regulatory or geopolitical risks. So our design is industry-specific rather than generic.”

### 1:10-2:00 Data And Financial Analysis

“Here on the left, we enter the company name, ticker, and industry segment. For this demonstration, we use the bundled WuXi AppTec historical dataset included in the repository. These figures were updated from official company disclosures, so the prototype now uses real historical company data rather than invented sample numbers. Even so, analysts should still cite the underlying annual reports or official filings in the final submission.”

“The system then calculates historical metrics such as revenue growth, gross margin, operating margin, net margin, current ratio, debt ratio, asset turnover, free cash flow margin, and backlog growth. These are shown in both a ratio table and charts, so the user can quickly understand the historical profile of the company.”

### 2:00-3:00 Assumption Setting And DCF

“Next, we move to the industry-specific section. This includes analyst review of CRDMO factors such as customer demand, capacity utilisation, margin resilience, overseas regulatory and geopolitical risk, and customer concentration risk. This reflects the idea that AI should support analyst judgement, not replace it.”

“Below that is the human-in-the-loop valuation section. The user can change the revenue growth forecast for Years 1 to 5, target EBIT margin, tax rate, WACC, terminal growth rate, net debt, and shares outstanding. Once the assumptions are set, the model calculates the DCF forecast, including revenue, EBIT, NOPAT, free cash flow, discounted free cash flow, terminal value, enterprise value, equity value, and fair value per share.”

### 3:00-4:00 Output And Export

“On the right side of the valuation section, we also show a sensitivity table for WACC and terminal growth. This is important because DCF outputs are highly assumption-sensitive. The system then generates a report-style output including industry analysis, company analysis, financial analysis, valuation commentary, key risks, and limitations.”

“Finally, the analyst can export the output as Markdown or plain text. This makes the prototype feel closer to a usable financial product workflow rather than just a visual demo.”

### 4:00-4:30 Limitations And Conclusion

“In conclusion, our project demonstrates a realistic equity research workflow for the CRDMO industry. Its strengths are industry fit, structured prompt design, human judgement checkpoints, and clear valuation logic. Its main limitations are that the DCF is simplified, the system does not include real-time market data, and analysts still need to verify sources and challenge assumptions. In future work, we would add peer multiple comparison, stronger citation tracking, and live data integration.”

## Presentation Tips

- Keep the app open before recording starts
- Zoom the browser so charts and tables are readable
- Change one input live to show sensitivity
- Remind the audience that the bundled WuXi AppTec figures are historical real data, but the valuation assumptions are still analyst inputs
- End with why human judgement still matters
