![My Cover](./assets/sb-cover.jpg)

# 🏟️ A Seat Availability Forecasting Engine

<p align="left">
  <img src="https://img.shields.io/badge/License-MIT-lightgrey" alt="License">
  <img src="https://img.shields.io/badge/ML-Supervised-lightgrey" alt="License">
</p>

> A predictive analytics system that forecasts seat availability for football matches. **Objective:** To solve the massive supply-demand imbalance in ticket sales by using machine learning to predict seat availability, maximizing matchday revenue and improving the fan experience at the stadium.

### Outline

- [Key Results](#key-results)
- [Overview](#overview)
- [Architecture](#architecture)
- [Dataset](#dataset)
- [Modeling](#modeling)
- [Structure](#structure)

---

## Key Results

| Metric                      | Result                               | Description |
| :-------------------------- | :----------------------------------- | :----------------------------------- |
| 📈 Revenue Growth           | **+15%** in Ticket Sales    | Enabled by confidently selling tickets predicted to become available, capturing previously lost demand. |
| 💰 Average Order Value | **+40%** Increase | A direct result of guaranteeing paired seating for families and groups, which encourages larger transactions. |
| 🎯 Forecast Accuracy | **89%** Accuracy (R²) | The model's predictions of final seat availability were highly accurate, providing a reliable basis for advance sales. |
| ⭐ Fan Experience          | **Paired Seating Guaranteed**  | Transformed the fan purchase journey from a lottery to a reliable process, drastically reducing empty single seats and improving atmosphere. |
| 📢 Marketing Efficiency | **Improved ROAS** | A wider time window to market the match allows for more effective campaign planning and better Return on Ad Spend (ROAS). |
| ⚖️ Pricing Flexibility | **Enabled Dynamic Pricing** | An extended sales timeframe creates opportunities to apply dynamic pricing strategies, optimizing revenue further. See **FCB_Dynamic-Pricing** </br> [![Badge Text](https://img.shields.io/badge/Link_to_Repo-grey?style=flat&logo=github)](https://github.com/tomas-ravalli/fcb-dynamic-pricing) |
| 🛡️ Fraud Reduction | **Mitigated Scalping** | By delaying the issuance of physical tickets until 48 hours before kick-off, the system combats fraud and unauthorized resale. |

## Overview

The SmartBooking engine acts as a forecasting layer. It ingests historical sales data and contextual factors to predict, weeks in advance, how many seats will ultimately be freed up in each stadium zone. This forecast empowers the club to sell a calculated number of tickets *before* they are officially released, bridging the gap between fan demand and latent supply. This moves the club from a reactive sales model to a proactive, predictive one.

| 🚩 The Problem | 💡 The Solution |
| :--------------------------- | :---------------------------- |
| **"Sold Out" Illusion**: Fans faced "Sold Out" messages, unaware that 40% of released seats appear in the last 72 hours. | **Advance Availability**: Predicts final seat count weeks in advance, allowing the club to sell tickets for seats that are not yet officially released. |
| **Lost Revenue**: High demand went unmet due to the delay in seat returns, leading to significant lost revenue for the club. | **Revenue Capture**: Unlocks millions in sales by matching early fan demand with predicted inventory. |
| **Poor Fan Experience**: The unpredictable nature of ticket availability frustrated fans and fueled secondary resale markets. | **Guaranteed Experience**: Offers fans, especially families and groups, guaranteed paired seating, improving satisfaction and trust. |
| **Seat Fragmentation**: Last-minute releases often resulted in many isolated single seats that were difficult to sell. | **Optimized Occupancy**: By selling seats early, the system facilitates better seat allocation, reducing empty singles and maximizing attendance. |

The diagram below illustrates the conceptual framework for the SmartBooking project. The system addresses the core problem of information asymmetry in ticket availability. Season ticket holders often release their seats back to the club very late, creating a frustrating experience for fans who see matches as "Sold Out" when thousands of seats will eventually become available.

<p align="center">
  <img src="./assets/dp-hl.png" alt="High-level Project Diagram" width="2000">
  <br>
  <em>Fig. 1: A high-level diagram of the Dynamic Pricing Engine.</em>
</p>


## Architecture

The general workflow is as follows:
1. {placeholder}
2. {placeholder}
3. {placeholder}

<p align="center">
  <img src="./assets/dp-ll.png" alt="Low-level Project Diagram" width="950">
    <br>
  <em>Fig. 2: A low-level diagram of the SmartBooking Engine.</em>
</p>

<details>
<summary><b>Click to see the detailed architecture breakdown</b></summary>

{placeholder}

</details>


## Dataset

{placeholder}

<details>
<summary><b>Click to see the full list of features</b></summary>

{placeholder}

</details>

### Match Excitement Factor

To create a realistic dataset, the generation script doesn't just create random numbers. Instead, it simulates the underlying market dynamics by creating a unified **"Match Excitement Factor"**. This single, powerful variable acts as the primary driver for most of the demand signals in the dataset.

The logic is designed to mimic how a real fan's interest level would change based on the context of a match:

1.  **Start with the opponent:** The excitement level begins with the quality of the opponent (`opponent_tier`). A top-tier opponent naturally generates more interest.

2.  **Adjust for context:** The base excitement is then adjusted up or down based on several real-world factors:
    * **League position:** Excitement increases slightly if the team is high in the league standings.
    * **Player injuries:** Excitement decreases significantly if a star player is injured, especially for a high-profile match.
    * **Match importance:** Excitement drops for less meaningful matches, such as when the league winner is already known.
    * **Holidays & weekdays:** Matches near holidays get a boost in excitement, while weekday matches see a slight decrease.

3.  **Drive demand signals:** This final "Match Excitement Factor" is then used to generate all the other demand signals. For example, a match with a high excitement score will also have higher `google_trends_index`, more positive `social_media_sentiment`, and more `internal_search_trends`.

This systemic approach ensures that the relationships between the features in the synthetic dataset are correlated in a logical and realistic way, making it a robust foundation for building and testing a demand forecasting model.

## Modeling

{placeholder}

{placeholder}

<details>
<summary><b>Click to see the detailed model performance evaluation</b></summary>

{placeholder}

### Validation

Before a full rollout, the system was rigorously validated through a series of controlled **A/B tests** to scientifically measure its impact and mitigate risk. The core principle was to isolate the effect of the dynamic pricing engine from all other market variables. 

The results from the A/B tests confirmed our hypothesis, showing a consistent **+6% lift in average revenue** for the treatment group. Additionaly, this was achieved while also increasing the sell-through rate, demonstrating that the model was effective at finding the true market equilibrium. These conclusive, data-backed results gave the business full confidence to proceed with a full-scale rollout of the dynamic pricing system across all stadium zones.

<details>
<summary><b>Click to see the full experimental design</b></summary>

### Experimental design

{placeholder}

### Key metrics tracked

{placeholder}

</details>


## Structure

While most of the source code for this project is private, this section outlines the full structure:

```bash
{placeholder}
````

</br>

> [!WARNING]
> * **Data:** All data presented in this public repository is synthetically generated. It is designed to mirror the statistical properties of the original dataset without revealing any confidential information.
> * **Code:** To honor confidentiality agreements, the source code and data for the original project are private. This repository demonstrates the modeling approach and best practices used in the real-world solution.
> * **Complexity:** This repository provides a high-level demonstration of the project's architecture and methodology. Certain implementation details and model complexities have been simplified for clarity.

</br>

<p align="center">🌐 © 2025 t.r.</p>
