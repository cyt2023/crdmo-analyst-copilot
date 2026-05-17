# CRDMO Analyst Copilot 中文说明

[English README](README.md)

CRDMO Analyst Copilot 是一个面向 ACC102 小组课程项目的 AI 股票研究与估值原型系统。

项目主题：

**AI Equity Research Valuation Agent for the Pharmaceutical CRDMO Industry: A Case Study of WuXi AppTec**

这个原型系统的目标不是做一个泛化聊天机器人，而是做一个更像券商研究员工作台的产品，用来支持医药 CRDMO / CRO-CDMO 行业的股票研究、财务分析和 DCF 估值流程。

## 项目定位

本项目围绕药明康德（WuXi AppTec）案例，展示一个完整的端到端研究流程：

1. 公司输入
2. 数据收集
3. 历史财务分析
4. 人工参与的估值假设设置
5. DCF 估值建模
6. 输出研究报告、图表和财务表格

系统强调“AI 辅助分析师”，而不是“AI 替代分析师”。在 CRDMO 行业里，很多关键判断都依赖行业理解，例如：

- 在手订单 backlog 的质量和增长
- 下游 pharma / biotech 研发外包需求
- 产能利用率
- 利润率韧性
- 海外监管与地缘政治风险
- 客户集中度风险

## 重要数据声明

仓库中自带的药明康德财务数据现在已经替换为**基于公司官方披露整理的 2019-2023 历史真实数据**。

但这些数据仍然需要注意：

- 虽然来自公司官方披露，但仍应回到原始年报或公告再次核对
- 已经适合课程原型演示，但正式提交时最好补充原始出处引用
- 不应在没有注明来源的情况下直接当作最终研究底稿

建议继续用于交叉核对的来源包括：

- 药明康德年报
- 中报和季报
- 年度业绩演示材料
- 交易所公告
- 可信金融数据库

## 仓库结构

```text
/README.md
/README_CN.md
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

## 主要功能

- Streamlit 原型界面
- 公司输入与 ticker 输入
- 上传 CSV 或直接使用内置的药明康德历史真实数据
- 自动计算历史财务比率
- CRDMO 行业特定分析维度
- 人工可修改的 DCF 假设
- 自动生成估值结果和敏感性表
- 导出 Markdown / 文本格式结果
- 提供多 Agent prompt 设计
- 提供 Coze / XIPU AI 工作流设计文档
- 提供药明康德历史数据来源说明文档

## Streamlit 工作流

[app/streamlit_app.py](/Users/cyt/Desktop/lkh-/app/streamlit_app.py) 中的网页原型包含以下流程：

1. 输入公司名称、ticker 和行业赛道
2. 上传财务 CSV，或直接使用内置的药明康德历史真实数据
3. 自动计算历史收入增长、利润率、偿债和现金流指标
4. 结合 CRDMO 行业特征做定性分析
5. 由用户手动检查并修改 DCF 假设
6. 自动输出 DCF 预测表、敏感性分析和估值结果
7. 生成研究风格输出并支持导出

## 财务公式

历史比率：

- `revenue_growth = revenue / previous_year_revenue - 1`
- `gross_margin = gross_profit / revenue`
- `operating_margin = operating_profit / revenue`
- `net_margin = net_profit / revenue`
- `current_ratio = current_assets / current_liabilities`
- `debt_ratio = total_liabilities / total_assets`
- `asset_turnover = revenue / total_assets`
- `fcf_margin = free_cash_flow / revenue`

DCF 模型：

- `forecast_revenue_t = previous_revenue * (1 + growth_rate_t)`
- `EBIT_t = forecast_revenue_t * EBIT_margin`
- `NOPAT_t = EBIT_t * (1 - tax_rate)`
- `FCF_t = NOPAT_t`，也可由用户改成 FCF margin 近似
- `discounted_FCF_t = FCF_t / (1 + WACC)^t`
- `terminal_value = FCF_5 * (1 + terminal_growth) / (WACC - terminal_growth)`
- `enterprise_value = sum(discounted_FCF) + discounted_terminal_value`
- `equity_value = enterprise_value - net_debt`
- `fair_value_per_share = equity_value / shares_outstanding`

## 如何运行

1. 安装依赖：

```bash
pip install -r requirements.txt
```

2. 启动网页：

```bash
streamlit run app/streamlit_app.py
```

## 展示建议

如果你们需要录课程 demo，推荐按照这个顺序展示：

1. 先介绍目标用户是券商或买方研究员
2. 展示药明康德案例输入
3. 说明当前默认数据来自药明康德官方历史披露
4. 展示历史财务分析图表
5. 强调 CRDMO 行业专属判断维度
6. 现场调整一两个 DCF 假设
7. 展示估值结果和敏感性分析
8. 导出研究输出
9. 最后补充系统局限性

## 项目亮点

- 行业匹配度高，不是泛行业模板
- 有明确的人机协同设计
- 估值逻辑完整，覆盖 DCF 核心步骤
- prompt 设计、工作流设计、文档交付都比较完整
- 很适合课程展示和答辩

## 局限性

- 当前已经内置药明康德真实历史数据，但仍需在正式提交中标注来源
- DCF 模型做了简化
- 没有接入实时股价、实时公告或实时数据库
- 还没有加入可比公司估值法
- 最终输出仍然需要人工复核和修订

## 提交前建议

正式交作业前，建议你们再做几件事：

- 在报告和演示中明确写出药明康德数据来源
- 在报告和文档中加入数据来源引用
- 在 GitHub 首页补上运行截图
- 按照 [docs/demo_video_script.md](/Users/cyt/Desktop/lkh-/docs/demo_video_script.md:1) 录 3-5 分钟演示视频
- 根据老师评分标准稍微微调措辞

## 一句话总结

这个项目最强的地方，在于它把“AI + 医药 CRDMO 行业股票研究 + 人工估值判断”结合成了一个可展示、可运行、可解释的产品原型。
