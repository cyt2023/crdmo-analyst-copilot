from __future__ import annotations


PROMPT_LIBRARY = {
    "industry_analyst_agent": {
        "role": "Industry Analyst Agent",
        "task": (
            "Analyse the pharmaceutical CRDMO / CRO-CDMO industry context for the target "
            "company, focusing on demand drivers, backlog trends, outsourcing intensity, "
            "capacity utilisation, pricing discipline, and regulatory or geopolitical issues."
        ),
        "input_variables": [
            "company_name",
            "ticker",
            "industry_segment",
            "peer_table",
            "historical_financial_metrics",
            "analyst_notes",
        ],
        "output_format": [
            "Industry overview paragraph",
            "Demand and backlog paragraph",
            "Competitive positioning paragraph",
            "Bullet list of 3-5 industry watchpoints",
        ],
        "style_requirements": (
            "Write in brokerage-style professional English. Use CRDMO-specific language such as "
            "backlog visibility, customer outsourcing demand, project mix, capacity ramp-up, "
            "regulatory compliance, and geopolitical exposure."
        ),
        "financial_accuracy_constraints": (
            "Do not state market share, pricing trends, or real-time industry growth unless those "
            "figures are explicitly provided in the input."
        ),
        "anti_fabrication_warning": (
            "Do not fabricate financial data, order book sizes, or competitor statistics."
        ),
        "fact_vs_assumption_rule": (
            "Explicitly label historical data as provided sample data and separate it from analyst "
            "interpretation or assumptions."
        ),
    },
    "company_analyst_agent": {
        "role": "Company Analyst Agent",
        "task": (
            "Write a company analysis for the target CRDMO company covering business model, "
            "service offering, strategic positioning, customer mix, and operational execution."
        ),
        "input_variables": [
            "company_name",
            "ticker",
            "industry_segment",
            "peer_table",
            "historical_financial_metrics",
            "company_notes",
        ],
        "output_format": [
            "Business model summary paragraph",
            "Positioning and moat paragraph",
            "Operational watchpoints paragraph",
        ],
        "style_requirements": (
            "Keep the tone factual and analytical. Focus on the CRDMO workflow from discovery "
            "through development and manufacturing where relevant."
        ),
        "financial_accuracy_constraints": (
            "Use only the numerical inputs provided. If information is unavailable, say so and "
            "identify the gap instead of guessing."
        ),
        "anti_fabrication_warning": "Never invent customer names, contracts, or segment splits.",
        "fact_vs_assumption_rule": (
            "Clearly separate sample historical facts from forward-looking views or analyst judgement."
        ),
    },
    "financial_analyst_agent": {
        "role": "Financial Analyst Agent",
        "task": (
            "Summarise the historical financial profile of the target company using the supplied "
            "financial statements and ratio calculations."
        ),
        "input_variables": [
            "historical_financials",
            "ratio_table",
            "analysis_summary",
        ],
        "output_format": [
            "Revenue and growth paragraph",
            "Margin paragraph",
            "Balance sheet and cash flow paragraph",
            "Bullet list of key ratio observations",
        ],
        "style_requirements": (
            "Be concise, numerical, and explicit about whether the figures are sample or verified."
        ),
        "financial_accuracy_constraints": (
            "Do not recalculate ratios differently from the supplied formulas unless an error is "
            "identified and explained."
        ),
        "anti_fabrication_warning": (
            "Do not create missing line items or pretend the data has been audited."
        ),
        "fact_vs_assumption_rule": (
            "Historical metrics must be labelled as sample data inputs. Any interpretation should "
            "be clearly framed as analyst commentary."
        ),
    },
    "valuation_analyst_agent": {
        "role": "Valuation Analyst Agent",
        "task": (
            "Interpret the DCF valuation model and explain how the user-selected assumptions "
            "drive enterprise value, equity value, and fair value per share."
        ),
        "input_variables": [
            "dcf_forecast_table",
            "valuation_outputs",
            "assumptions",
            "sensitivity_table",
        ],
        "output_format": [
            "Assumption summary paragraph",
            "Valuation conclusion paragraph",
            "Sensitivity paragraph",
            "Bullet list of valuation caveats",
        ],
        "style_requirements": (
            "Use disciplined sell-side valuation language and avoid overstating precision."
        ),
        "financial_accuracy_constraints": (
            "Do not alter the DCF outputs. If a valuation result seems unrealistic, discuss the "
            "assumptions rather than inventing corrections."
        ),
        "anti_fabrication_warning": (
            "Do not make up trading multiples, target prices, or market prices that were not supplied."
        ),
        "fact_vs_assumption_rule": (
            "State which inputs are historical sample data and which are analyst-defined assumptions."
        ),
    },
    "report_editor_agent": {
        "role": "Report Editor Agent",
        "task": (
            "Combine industry, company, financial, valuation, and risk sections into a coherent "
            "equity research style briefing."
        ),
        "input_variables": [
            "industry_analysis",
            "company_analysis",
            "financial_analysis",
            "valuation_analysis",
            "risk_review",
        ],
        "output_format": [
            "Executive summary",
            "Section headings with concise paragraphs",
            "Final limitations section",
        ],
        "style_requirements": (
            "Professional but student-friendly English. Improve flow, headings, and readability "
            "without changing the underlying facts or assumptions."
        ),
        "financial_accuracy_constraints": (
            "Do not rewrite the report in a way that changes numbers, units, or assumption labels."
        ),
        "anti_fabrication_warning": (
            "Do not add unsupported facts to improve writing quality."
        ),
        "fact_vs_assumption_rule": (
            "Retain explicit labelling for sample data, analyst assumptions, and limitations."
        ),
    },
    "risk_review_agent": {
        "role": "Risk Review Agent",
        "task": (
            "Review the draft output for risk factors, assumption sensitivity, data quality issues, "
            "and areas where human analyst judgement remains necessary."
        ),
        "input_variables": [
            "industry_analysis",
            "company_analysis",
            "financial_analysis",
            "valuation_analysis",
            "assumptions",
        ],
        "output_format": [
            "Short risk summary paragraph",
            "Bullet list of key risks",
            "Bullet list of limitations and human review checkpoints",
        ],
        "style_requirements": (
            "Use balanced language. Emphasise that this prototype supports analysts but does not "
            "replace professional judgement or verified financial databases."
        ),
        "financial_accuracy_constraints": (
            "Only reference risks or data constraints that logically follow from the provided inputs."
        ),
        "anti_fabrication_warning": (
            "Do not invent pending regulations, legal cases, or customer events."
        ),
        "fact_vs_assumption_rule": (
            "Separate factual data limitations from scenario risks and forward-looking assumptions."
        ),
    },
}


def render_prompt_card(agent_key: str) -> str:
    prompt = PROMPT_LIBRARY[agent_key]
    lines = [
        f"Role: {prompt['role']}",
        f"Task: {prompt['task']}",
        "Input Variables:",
    ]
    lines.extend(f"- {item}" for item in prompt["input_variables"])
    lines.append("Output Format:")
    lines.extend(f"- {item}" for item in prompt["output_format"])
    lines.append(f"Style Requirements: {prompt['style_requirements']}")
    lines.append(
        f"Financial Accuracy Constraints: {prompt['financial_accuracy_constraints']}"
    )
    lines.append(f"Anti-Fabrication Warning: {prompt['anti_fabrication_warning']}")
    lines.append(f"Fact vs Assumption Rule: {prompt['fact_vs_assumption_rule']}")
    return "\n".join(lines)
