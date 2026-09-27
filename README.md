readme_content = '''# PharmEasy Regional Pulse Analysis: Regional Delivery Package

## Headline Finding
Between April and June 2026, Guntur emerged as our most volatile growth driver, registering a dramatic, broad-based **+122.19% Month-on-Month sales surge in May** (peaking at ₹138,738.93) before stabilizing to a healthy, permanent baseline in June (₹99,745.18).

---

## 📦 Artifact Index
1. **Streamlit Dashboard (`app.py`):** Interactive, three-level web application designed for dynamic regional data, category performance, and monthly ledger exploration.
2. **CII Executive Summary (Embedded in `app.py`):** High-level structured narrative at the top of the dashboard connecting key KPIs and trends directly to business implications.
3. **One-Page Memo (`memo.md`):** Formally documented operational recommendations, evidence logs, next-step audits, and structured uncertainty risk-tags.
4. **Presentation Storyline (`presentation_storyline.md`):** Audience-tailored narrative frameworks (Executive vs. Regional Manager) paired with defensive Q&A protocols.

---

## 🗺️ Recommended Review Order
To evaluate this package effectively, we recommend reviewing the artifacts in the following sequence:
1. **`app.py` & Embedded CII Summary:** Begin here to absorb the core numbers, explore the visual insights dynamically, and establish quantitative context.
2. **`memo.md`:** Pivot to the formal business memorandum to understand the concrete operational recommendations and risk classifications ([LOW]/[MEDIUM]/[HIGH]).
3. **`presentation_storyline.md`:** Review this next to examine how the findings are strategically framed for different internal stakeholders, along with robust Q&A defenses.

---

## ⚠️ Core Unverified Assumption
**Local Driver Hypothesis:** The rapid surge in Guntur during May is assumed to have been triggered by a localized marketing campaign or an aggressive expansion in supply availability; however, these external drivers are not recorded in the database transactions and require validation from local operational leads.

---

## ⚙️ How to Run the Dashboard Locally
To launch the interactive dashboard on your local machine, run the following commands:
```bash
# Install required dependencies
pip install streamlit pandas plotly

# Launch the Streamlit application
streamlit run app.py
```
'''