# 📌 Investment Risk & Portfolio Recommendation Algorithm

## 📖 Introduction

This document explains the algorithm used to calculate an investor's **risk capacity**, **risk tolerance**, **investing potential**, and other financial metrics. The goal is to provide a **personalized investment portfolio recommendation** based on an investor's financial situation and behavior.

This document is written for **non-technical users** who may not have a background in finance or programming.

---

## **🛠️ How Does the Algorithm Work?**

The algorithm takes **responses from 19 investment-related questions** and calculates different **financial scores and metrics**. These scores determine an investor's:

1. **Risk Capacity** – How much financial risk they can afford to take.
2. **Risk Tolerance** – How comfortable they are with investment risks.
3. **Investing Potential** – How much they can invest based on their finances.
4. **Liquidity Ratio** – Whether they have enough emergency savings before investing.
5. **Debt-to-Income Ratio** – Whether they have too much debt to take on more risk.
6. **Investment Horizon** – How long they plan to stay invested.

Using these factors, the algorithm **recommends a personalized investment portfolio**.

---

## **📊 1. Risk Capacity Score**

### **🧐 What is Risk Capacity?**

Risk capacity is how much financial risk an investor **can afford to take** based on their **income, savings, experience, and financial obligations**.

### **📏 How Do We Calculate Risk Capacity?**

Risk Capacity is calculated based on these factors:

| Factor                                            | Explanation                                                                          | Impact                                         |
| ------------------------------------------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------- |
| **Income Stability**                              | A stable monthly income increases risk capacity.                                     | ✅ Higher risk capacity if income is stable.    |
| **Savings Rate**                                  | Higher savings means better financial health.                                        | ✅ More savings = Higher risk capacity.         |
| **Home Ownership**                                | Owning a house provides financial security.                                          | ✅ Homeowners can take more risk.               |
| **Investment Experience**                         | More experience means better risk management.                                        | ✅ More experience = Higher risk capacity.      |
| **Existing Investments in Fixed Deposits (FDs)**  | Too much money in FDs means low risk-taking ability.                                 | ❌ More FDs = Lower risk capacity.              |
| **Dependents (Family Members Relying on Income)** | More dependents = More financial responsibilities.                                   | ❌ More dependents = Lower risk capacity.       |
| **Short-Term Financial Goals**                    | If they have short-term goals (buying a house, marriage, etc.), they need liquidity. | ❌ More short-term goals = Lower risk capacity. |

### **📌 Formula for Risk Capacity Score**

```python
risk_capacity = (income_stability * 10) + savings_rate + owns_house + investment_experience \
                + fixed_asset_allocation + has_dependents + major_financial_goals
```

---

## **📊 2. Risk Tolerance Score**

### **🧐 What is Risk Tolerance?**

Risk tolerance measures how **emotionally comfortable** an investor is with market fluctuations. It is different from risk capacity (which is about affordability).

### **📏 How Do We Calculate Risk Tolerance?**

| Factor                                   | Explanation                                                                        | Impact                                            |
| ---------------------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------- |
| **How Often They Check Their Portfolio** | Checking too often means they might panic-sell.                                    | ❌ Checking daily = Lower risk tolerance.          |
| **Reaction to Market Crashes**           | If they panic-sell, they have low tolerance.                                       | ✅ Holding or investing more = Higher tolerance.   |
| **Market Dip Reaction**                  | If they sell at a 10% drop, they are risk-averse.                                  | ❌ Selling early = Lower risk tolerance.           |
| **Preferred Portfolio Strategy**         | Some people prefer low risk, others want aggressive growth.                        | ✅ High growth preference = Higher risk tolerance. |
| **Investment Type (SIP vs. One-Time)**   | SIP investors tend to be conservative, while one-time investors take higher risks. | ✅ One-time investors have higher tolerance.       |

### **📌 Formula for Risk Tolerance Score**

```python
risk_tolerance = (portfolio_checking_freq + market_dip_action + investment_strategy +
                  portfolio_crash_reaction + investment_type)
```

---

## **📊 3. Investing Potential**

### **🧐 What is Investing Potential?**

This metric determines **how much money an investor can safely invest** based on their income, expenses, and financial commitments.

### **📏 How Do We Calculate Investing Potential?**

| Factor                           | Explanation                          | Impact                            |
| -------------------------------- | ------------------------------------ | --------------------------------- |
| **Declared Investment Amount**   | The amount the user wants to invest. | ✅ Directly affects potential.     |
| **Additional Sources of Income** | Side businesses, rental income, etc. | ✅ More income = Higher potential. |

### **📌 Formula for Investing Potential**

```python
investing_potential = int(responses.get("How much amount do you want to invest?", "5000"))
```

---

## **📊 4. Liquidity Ratio**

### **🧐 What is Liquidity Ratio?**

Liquidity Ratio ensures that an investor has enough **emergency funds** before taking investment risks.

### **📌 Formula for Liquidity Ratio**

```python
liquidity_ratio = {
    "Less than 3 months": -10,
    "3 to 6 months": 0,
    "More than 6 months": 10
}.get(responses.get("How many months of expenses can your emergency savings cover?", ""), 0)
```

---

## **📊 5. Debt-to-Income Ratio**

### **🧐 What is Debt-to-Income Ratio?**

This ensures the investor does not have too much debt before making investments.

### **📌 Formula for Debt-to-Income Ratio**

```python
debt_to_income_ratio = {
    "Less than 20%": 10,
    "20-40%": 0,
    "More than 40%": -10
}.get(responses.get("What percentage of your income goes towards EMIs?", ""), 0)
```

---

## **🎯 Final Portfolio Recommendation**

Once all the scores are calculated, we categorize investors into five types:

| Final Score | Portfolio Type         | Asset Allocation     |
| ----------- | ---------------------- | -------------------- |
| 0 - 30      | **Ultra Conservative** | 80% Debt, 20% Equity |
| 31 - 50     | **Conservative**       | 65% Debt, 35% Equity |
| 51 - 70     | **Moderate Growth**    | 50% Equity, 50% Debt |
| 71 - 85     | **Aggressive Growth**  | 70% Equity, 30% Debt |
| 86 - 100    | **High Growth**        | 90% Equity, 10% Debt |

---

## **⏳ TL;DR (Summary)**

- This algorithm **analyzes an investor’s financial health & behavior** to suggest the **best portfolio**.
- It calculates **Risk Capacity, Risk Tolerance, Investing Potential, Liquidity Ratio, and Debt-to-Income Ratio**.
- Using these scores, it recommends an investment strategy that **aligns with their risk profile**.

🚀 **This ensures safe & optimized investment decisions!**

