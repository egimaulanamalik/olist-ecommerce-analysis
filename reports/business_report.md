#  Olist E-Commerce - Business Insights Report

**Dataset:** Brazilian E-Commerce Public Dataset by Olist
**Period:** September 2016 - August 2018
**Total Orders:** 98,666 | **Total Revenue:** ~R$13M | **Unique Customers:** 95,420

---

## Execitive Summary

Olist grew explosively from R$267/month in late 2016 to a R$1M/month plateau by mid-2018, driven entirely by new customer acquisition. However, 96.9% of customers never returned after their first purchase, delivery times in the North and Northeast regularly exceeded 25 days, and satisfaction scores dropped in direct proportion to how long deliveries took. The platform has a strong acquisition engine and a broken retention engine. Fixing retention is the single highest-leverage opportunity.

## Finding 1 - Delivery Speed Drives Everything

**Evidence:**

* 1-star customers waited an average of 20.9 days vs 10.2 days for 5-star customers.
* Every additional star of review score = ~2-3 fewer delivery days (perfect monotonic relationship across all 5 score levels)
* North and Northeast states averaged 23-29 day deliveries vs 11-13 days in the South.

**Actions:**

* Negotiate stricter SLAs with logistics partners serving AM, RR, PA and MA.
* Offer delivery guarantees (or estimated date buffers) specifically for Northeast orders.
* Flag orders projected to exceed 20 days for proactive customer communication.

---

## Finding 2 - 97% of Customers Never Return

**Evidence:**

* Cohort analysis showed retention dropped below 1% by Month 1 across ALL cohorts.
* Churn prediction model confirmed AUC of only 0.60 - no single first-order signal reliably predicts who returns.
* Growth from 2016-2018 was 100% acquisition-driven, not retention-driven.

**Action:**

* Trigger an automated email 7 days after delivery with a 10% second-purchased voucher.
* Target the voucher universally - the model is too weak to justify selective targeting.
* Build a second seasonal spike (Valentine's Day, Mother's Day, etc) to create return purchase occasions beyond Black Friday.

---

## Finding 3 - 41% Customers Are One Purchase Away From Loyalty

**Evidence:**

- Recency, Frequency and Monetary (RFM) segmentation identified 39,343 Potential Loyalist (41.2% of all customers).
- These customers bought recently but have not yet established a repeat pattern.
- Champions (8,102 customers) already generate disproporionate revenue.

**Action:**

- Potential Loyalist: trigger a personalised follow-up based on their first category (e.g. a beauty customer gets a beauty voucher, not a generic discount)
- Champions: give early access to new products, priority support, and no-questions-asked returns - protect their segment at all costs.
- At Risk (12,694 customers): send a reactivation campaign before they go cold.

---

## Finding 4 — Product Category Predicts Customer Type

**Evidence:**

- Feature importance showed first_category as the #2 predictor of churn.
- beleza_saude (Health & Beauty) leads revenue at R$1.26M with 8,836 orders a high-frequency repurchase category.
- relogios_presentes (Watches & Gifts) generates R$1.20M from only 5,624 orders through high avg price (R$201) — but gift buyers rarely return.

**Action:**

* Double down on Health & Beauty seller recruitment — natural repeat purchase category.
* For gift category buyers, trigger a "buy for yourself" follow-up campaign rather than expecting organic return.
* Use category as a segmentation variable in all retention communications.

---

## Finding 5 — Olist Is a São Paulo Marketplace

**Evidence:**

* SP generated R$5.2M — nearly 3x the next state (RJ at R$1.8M).
* Only 6 states had enough sellers to pass the 100-order analysis threshold.
* Seller base is almost entirely concentrated in South/Southeast.

**Action:**

* Recruit sellers actively in RJ, MG, and RS to reduce SP concentration risk.
* Incentivise Northeast sellers to join — shorter last-mile distances would directly improve the delivery times that are killing satisfaction scores there.
* Consider a regional fulfilment partnership in the North to serve AM, RR, and PA.

---

## Summary — Priority Actions

| Priority | Action                                  | Finding |
| :------: | --------------------------------------- | ------- |
|    1    | Universal post-purchase retention email | 2       |
|    2    | Negotiate logistics SLAs for North/NE   | 1       |
|    3    | Protect Champions segment with perks    | 3       |
|    4    | Category-personalised vouchers          | 4       |
|    5    | Northeast seller recruitment            | 5       |

---

*Report generated from Phase 3 EDA and Phase 4a churn prediction model.
All revenue figures in Brazilian Real (R$).*
