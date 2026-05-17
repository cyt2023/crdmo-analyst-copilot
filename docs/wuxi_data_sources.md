# WuXi AppTec Data Sources

## Purpose

This note explains where the bundled WuXi AppTec historical data in `data/wuxi_financials_sample.csv` came from after the project was updated from prototype sample values to real historical company disclosures.

## Scope

The bundled WuXi AppTec file now contains historical figures for:

- 2019
- 2020
- 2021
- 2022
- 2023

Units are recorded in **RMB million**.

## Main Source Documents

### Annual Reports

- 2019 Annual Report  
  https://officialsite-static.wuxiapptec.com/upload/59/20200421/2020041700618.pdf

- 2020 Annual Report  
  https://officialsite-static.wuxiapptec.com/upload/d8/20210519/2021-04-20-2020%20Annual%20Report.pdf

- 2021 Annual Report  
  https://static.wuxiapptec.com/d1/20220613/2021%20ANNUAL%20REPORT.pdf

- 2022 Annual Report  
  https://officialsite-static.wuxiapptec.com/upload/4c/20230505/2023042001056.pdf

- 2023 Annual Report  
  https://officialsite-static.wuxiapptec.com/upload/d2/20240426/2023%20ANNUAL%20REPORT.pdf

### Supplementary Disclosures Used

- 2024 First Quarterly Report  
  Used for December 31, 2023 current asset and current liability balance sheet detail in the current repository dataset.  
  https://officialsite-static.wuxiapptec.com/upload/2024_FIRST_QUARTERLY_REPORT_bc8c0f79a4.pdf

- 2024 Annual Results Presentation  
  Used for the historical operating cash flow and capex chart referenced in the repository dataset.  
  https://officialsite-static.wuxiapptec.com/upload/WXAT_2024_Annual_Results_Presentation_vfinal_77092fc2d1.pdf

## Field Mapping

The following fields were taken from official company disclosures and converted into RMB million:

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
- `backlog`

## Important Definition Notes

### Net Profit

The repository uses net profit attributable to the owners of the company because that is the equity research convention most relevant to shareholders.

### Backlog

The `backlog` field in the repository reflects year-end disclosed remaining performance obligations / unsatisfied performance obligations from official company disclosures, rather than an informal internal order book estimate.

### Free Cash Flow

The `free_cash_flow` field is calculated in the repository as:

`operating_cash_flow - capex`

This matches the project’s modelling logic and also aligns with the company’s disclosed free cash flow framing in the periods where free cash flow is explicitly highlighted in investor materials.

## Coursework Use Reminder

Although the repository now uses real historical company disclosures, you should still:

- cite the original source documents in your final report or appendix
- cross-check numbers before submission
- explain any metric definitions clearly, especially backlog and free cash flow
- avoid presenting the repository as a substitute for full professional investment research
