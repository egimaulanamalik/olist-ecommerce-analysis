
# Olist Brazilian E-Commerce — End-to-End Data Analysis

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Status](https://img.shields.io/badge/Status-Complete-green)

A full end-to-end data analyst portfolio project using the [Olist Brazilian E-Commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) from Kaggle. The project covers data cleaning, exploratory data analysis, machine learning, and an interactive dashboard.

---

## Key Findings

- **R$13.6M revenue** across 98,666 orders from Sep 2016 to Aug 2018.
- **November 2017 peak** — Black Friday drove the single largest revenue month.
- **Delivery speed drives satisfaction** — 1-star customers waited twice as long as 5-star customers (20.9 vs 10.2 days), a perfect monotonic relationship.
- **96.9% of customers never returned** — growth was entirely acquisition-driven, confirmed by both cohort analysis and churn prediction modelling.
- **Health & Beauty** is the top revenue category at R$1.26M.
- **São Paulo generated R$5.2M** — nearly 3x the next state (Rio de Janeiro at R$1.8M).

---

## Project Structure

olist-ecommerce-analysis/
├── notebooks/
│   ├── notebook_01_data_loading.ipynb
│   ├── notebook_02_data_cleaning.ipynb
│   ├── notebook_03_eda.ipynb
│   └── notebook_04a_churn.ipynb
├── dashboard/
│   └── app.py
├── reports/
│   ├── 01_monthly_revenue_trend.png
│   ├── 02_category_revenue.png
│   ├── 03_delivery_by_state.png
│   ├── 04_review_score_distribution.png
│   ├── 05_delivery_vs_review_score.png
│   ├── 06_rfm_segmentation.png
│   ├── 07_cohort_retention.png
│   ├── 08_seller_scorecard.png
│   ├── 09_geographic_heatmap.html
│   ├── 10_roc_curve_comparison.png
│   ├── 11_confusion_matrix.png
│   ├── 12_feature_importance.png
│   └── business_report.md
└── README.md

---



## Phases

### Phase 1 & 2 — Data Loading & Cleaning

- Loaded 9 relational CSV tables from Kaggle
- Audited nulls, duplicates, and data types
- Joined all tables into a 22-column master orders table
- Saved cleaned files to `data/cleaned/`

### Phase 3 — Exploratory Data Analysis

9 analyses covering:

- Monthly revenue trends
- Revenue by product category
- Delivery performance by seller state
- Review score distribution
- Delivery delay vs review score
- RFM customer segmentation
- Cohort retention analysis
- Seller performance scorecard
- Geographic revenue heatmap

### Phase 4 — Machine Learning & Dashboard

**4A — Churn Prediction**

- Defined churn as customers who never placed a second order (96.9%)
- Built features from first-order signals only
- Trained Logistic Regression, Random Forest, and XGBoost models
- Best model: XGBoost (AUC 0.60)
- Finding: churn is structural, not behavioural — no first-order signal
  reliably predicts who returns

**4B — Business Recommendations**

- 5 actionable findings with supporting evidence
- Priority action list for the Olist team

**4C — Streamlit Dashboard**

- 5 interactive pages: Revenue Trends, Category Performance,
  Delivery & Satisfaction, Customer Segments, Seller Scorecard

---

## Dashboard Preview

> Run locally:
>
> ```bash
> source venv/bin/activate
> streamlit run dashboard/app.py
> ```

---

## Tech Stack

| Tool                 | Purpose               |
| -------------------- | --------------------- |
| Python 3.14          | Core language         |
| pandas               | Data manipulation     |
| matplotlib / seaborn | Static visualisations |
| plotly               | Interactive charts    |
| scikit-learn         | ML models             |
| XGBoost              | Churn prediction      |
| Streamlit            | Interactive dashboard |

---

## Dataset

**Source:** [Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)**Period:** September 2016 – August 2018**Tables:** 9 relational CSVs**Orders:** 99,441 total, 98,666 complete

> Note: Raw data files are not included in this repository due to size.
> Download from Kaggle and place in `data/` to run the notebooks.
>
