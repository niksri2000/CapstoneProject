def draft_report_v1(flagged_regions, metrics):
    """
    Generates Context-Insight-Implication markdown blocks for each unique flagged region.
    metrics is a dictionary containing growth and sales metrics.
    """
    report_markdown = "# Regional Pulse Business Report\n\n"
    for region in sorted(list(flagged_regions)):
        report_markdown += f"### Region: {region}\n\n"
        
        # Retrieve metrics safely
        apr = metrics['apr_sales'].get(region, 0.0)
        may = metrics['may_sales'].get(region, 0.0)
        jun = metrics['june_sales'].get(region, 0.0)
        
        change_apr_may = metrics['changes_apr_may'].get(region, 0.0)
        change_may_jun = metrics['changes_may_jun'].get(region, 0.0)
        
        is_flagged_apr_may = metrics['flags_apr_may'].get(region, False)
        is_flagged_may_jun = metrics['flags_may_jun'].get(region, False)
        
        # Construct Context
        context_str = f"**Context:** {region} registered total sales of INR {apr:,.2f} in April, INR {may:,.2f} in May, and INR {jun:,.2f} in June. "
        
        # Construct Insight
        insights = []
        if is_flagged_apr_may:
            insights.append(f"a significant MoM change of {change_apr_may}% from April to May")
        if is_flagged_may_jun:
            insights.append(f"a significant MoM change of {change_may_jun}% from May to June")
        
        insight_str = f"**Insight:** Analysis reveals " + " and ".join(insights) + ". "
        
        # Construct Implication
        implications = []
        if is_flagged_apr_may:
            direction = "growth" if change_apr_may > 0 else "decline"
            implications.append(f"the initial April-May {direction} demands immediate resource matching to sustain " if change_apr_may > 0 else f"the initial April-May {direction} suggests severe supply or operational bottlenecks during that period ")
        if is_flagged_may_jun:
            direction = "growth" if change_may_jun > 0 else "decline"
            implications.append(f"the subsequent May-June {direction} requires long-term inventory strategy modifications" if change_may_jun > 0 else f"the subsequent May-June {direction} requires localized marketing interventions to arrest the trend")
            
        implication_str = f"**Implication:** " + " Additionally, ".join(implications) + ".\n\n---\n\n"
        
        report_markdown += context_str + "\n" + insight_str + "\n" + implication_str
        
    return report_markdown

# 1. First, let's extract the May-June transitions to have the complete metrics profile
jun_sales = df_display['June Sales (INR)'].to_dict()
changes_may_jun = {reg: compute_percentage_change_v1(jun_sales[reg], may_sales[reg]) for reg in may_sales}
flags_may_jun = flag_significant_regions_v1(changes_may_jun, threshold=8)

# 2. Gather all metrics into a consolidated structure
metrics_dict = {
    'apr_sales': apr_sales,
    'may_sales': may_sales,
    'june_sales': jun_sales,
    'changes_apr_may': ap_may_changes,
    'changes_may_jun': changes_may_jun,
    'flags_apr_may': ap_may_flags,
    'flags_may_jun': flags_may_jun
}

# 3. Find unique regions flagged in EITHER transition
all_flagged_regions = set()
for reg, flagged in ap_may_flags.items():
    if flagged:
        all_flagged_regions.add(reg)
for reg, flagged in flags_may_jun.items():
    if flagged:
        all_flagged_regions.add(reg)

# 4. Generate and display the markdown report
markdown_report = draft_report_v1(all_flagged_regions, metrics_dict)
from IPython.display import display, Markdown
display(Markdown(markdown_report))

"""
#Output:

Regional Pulse Business Report
Region: Bengaluru
Context: Bengaluru registered total sales of INR 203,505.48 in April, INR 172,929.68 in May, and INR 170,294.11 in June. Insight: Analysis reveals a significant MoM change of -15.02% from April to May. Implication: the initial April-May decline suggests severe supply or operational bottlenecks during that period .

Region: Guntur
Context: Guntur registered total sales of INR 62,442.27 in April, INR 138,738.93 in May, and INR 99,745.18 in June. Insight: Analysis reveals a significant MoM change of 122.19% from April to May and a significant MoM change of -28.11% from May to June. Implication: the initial April-May growth demands immediate resource matching to sustain Additionally, the subsequent May-June decline requires localized marketing interventions to arrest the trend.

Region: Hyderabad
Context: Hyderabad registered total sales of INR 209,670.15 in April, INR 243,825.28 in May, and INR 294,088.56 in June. Insight: Analysis reveals a significant MoM change of 16.29% from April to May and a significant MoM change of 20.61% from May to June. Implication: the initial April-May growth demands immediate resource matching to sustain Additionally, the subsequent May-June growth requires long-term inventory strategy modifications.

Region: Karimnagar
Context: Karimnagar registered total sales of INR 49,815.71 in April, INR 61,585.90 in May, and INR 34,490.58 in June. Insight: Analysis reveals a significant MoM change of 23.63% from April to May and a significant MoM change of -44.0% from May to June. Implication: the initial April-May growth demands immediate resource matching to sustain Additionally, the subsequent May-June decline requires localized marketing interventions to arrest the trend.

Region: Tirupati
Context: Tirupati registered total sales of INR 54,582.74 in April, INR 91,083.20 in May, and INR 75,530.99 in June. Insight: Analysis reveals a significant MoM change of 66.87% from April to May and a significant MoM change of -17.07% from May to June. Implication: the initial April-May growth demands immediate resource matching to sustain Additionally, the subsequent May-June decline requires localized marketing interventions to arrest the trend.

Region: Vijayawada
Context: Vijayawada registered total sales of INR 171,334.19 in April, INR 174,863.57 in May, and INR 153,849.68 in June. Insight: Analysis reveals a significant MoM change of -12.02% from May to June. Implication: the subsequent May-June decline requires localized marketing interventions to arrest the trend.

Region: Visakhapatnam
Context: Visakhapatnam registered total sales of INR 134,765.29 in April, INR 50,590.08 in May, and INR 100,735.57 in June. Insight: Analysis reveals a significant MoM change of -62.46% from April to May and a significant MoM change of 99.12% from May to June. Implication: the initial April-May decline suggests severe supply or operational bottlenecks during that period Additionally, the subsequent May-June growth requires long-term inventory strategy modifications.

Region: Warangal
Context: Warangal registered total sales of INR 100,468.14 in April, INR 78,339.23 in May, and INR 66,715.24 in June. Insight: Analysis reveals a significant MoM change of -22.03% from April to May and a significant MoM change of -14.84% from May to June. Implication: the initial April-May decline suggests severe supply or operational bottlenecks during that period Additionally, the subsequent May-June decline requires localized marketing interventions to arrest the trend.
"""
