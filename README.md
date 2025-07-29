![My Cover](./assets/sb-cover.jpg)

# 🏟️ Seat Availability Forecasting Engine

<p align="left">
  <img src="https://img.shields.io/badge/License-MIT-lightgrey" alt="License">
  <img src="https://img.shields.io/badge/ML-Supervised_Regression-lightgrey" alt="ML Task">
</p>

> An ML system that forecasts stadium seat availability for football matches. **Objective:** To solve the supply-demand imbalance in ticket sales by using machine learning to predict seat availability, maximizing matchday revenue and improving the fan experience at the stadium.

### Outline

- [Key Results](#key-results)
- [Overview](#overview)
- [Architecture](#architecture)
- [Dataset](#dataset)
- [Modeling](#modeling)
- [Structure](#structure)

---

## Key Results

| Metric | Result | Description |
| :-------------------------- | :------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------- |
| 📈 Revenue Growth | **+15%** in Ticket Sales | Enabled by confidently selling tickets predicted to become available, capturing previously lost demand. Confirmed via A/B testing. |
| 💰 Average Order Value | **+40%** Increase | A direct result of guaranteeing paired seating for families and groups, which encourages larger transactions and improves the fan experience. |
| 🎯 Forecast Accuracy | **85%** Accuracy | The ML model's predictions significantly outperformed internal domain experts (65% accuracy) and simple averages (45%). |
| ⭐ Fan Experience | Paired Seating Guaranteed | Transformed the fan purchase journey. Users buy for a zone, not a specific seat, and are guaranteed paired seats assigned 24-48 hours before the match. |
| 📢 Marketing Efficiency | Improved ROAS **14%** | A wider time window to market the match allows for more effective campaign planning, better segmentation, and improved Return on Ad Spend. |
| 🛡️ Fraud Reduction | Mitigated Scalping | By delaying the issuance of final tickets until just before kick-off, the system combats fraud and gives a competitive advantage over secondary markets. |

## Overview

The core business problem originates with the club's membership model. Approximately 85% of the stadium's 99,000+ seats are allocated to season ticket holders ("members"). This leaves only about 9,500 seats available for general sale from day one. Members who cannot attend a match can release their seat back to the club for resale via the `Seient Lliure` ("Free Seat") program.

However, member behavior creates a massive supply-demand gap: **on average, 40% of seats are freed up within the last 72 hours of a match**, while fan demand is highest weeks in advance. This mismatch leads to lost revenue, a poor fan experience with "sold-out" messages, and fragmented single seats that are hard to sell.

The SmartBooking engine was designed to bridge this gap. It acts as a forecasting layer, using machine learning to generate a **recommendation** on how many seats will become available. A **Ticketing Manager** then reviews this forecast, applies business logic and safety margins, and makes the final decision on how much inventory to push to the live ticketing system. This "human-in-the-loop" approach combines predictive power with expert oversight.

| 🚩 The Problem | 💡 The Solution |
| :--------------------------- | :---------------------------- |
| **"Sold Out" Illusion**: Fans faced "Sold Out" messages, unaware that thousands of seats appear in the last 72 hours. | **Advance Availability**: Predicts final seat count weeks in advance, allowing the club to sell tickets for seats that are not yet officially released. |
| **Lost Revenue**: High, early demand went unmet due to the delay in seat returns, leading to significant lost revenue for the club. | **Revenue Capture**: Unlocks millions in sales by matching early fan demand with manager-approved predicted inventory. |
| **Poor Fan Experience**: The unpredictable nature of ticket availability frustrated fans and fueled secondary resale markets. | **Guaranteed Experience**: Offers fans, especially families and groups, guaranteed paired seating, improving satisfaction and trust. |
| **Seat Fragmentation**: Last-minute releases often resulted in many isolated single seats that were difficult to sell. | **Optimized Occupancy**: By selling seats early and guaranteeing pairs, the system reduces empty singles and maximizes attendance. |

The diagram below illustrates the supply-demand gap the system was built to solve. The engine forecasts the final supply (the peak of the blue curve) and makes that inventory available to meet the high early demand (the red line).

<p align="center">
  <img src="https://.png" alt="High-level Project Diagram" width="2000">
  <br>
  <em>Fig. 1: The supply-demand gap between early fan demand and late seat releases.</em>
</p>


## Architecture

The general workflow is as follows:
1.  **Data Sources** are ingested, focusing on historical `Seient Lliure` patterns and contextual match data.
2.  The **Forecasting Engine** generates a seat availability forecast that is delivered as a recommendation to the Ticketing Manager.
3.  The **Ticketing Manager** reviews the forecast, applies a safety buffer, and pushes the final, approved inventory to the **Ticketing System**.

<p align="center">
  <img src="./assets/sb-ll.png" alt="Low-level Project Diagram" width="950">
    <br>
  <em>Fig. 2: A low-level diagram of the SmartBooking Engine.</em>
</p>

<details>
<summary><b>Click to see the detailed architecture breakdown</b></summary>

### Data Sources

| Component | Description |
| :--- | :--- |
| **`Seient Lliure` Data** | Historical data on seat release behavior, including timing and frequency, for different member segments and stadium zones. |
| **Match & Competition Data** | Foundational information about each match: opponent, date/time, competition type, and matchday number. |
| **Historical Sales Data** | Time-series data tracking ticket prices and sales velocity for past matches. |
| **Contextual Demand Signals**| External factors that affect attendance decisions: holidays, weather forecasts, team momentum (league position, recent results), and player status. |

### Forecasting & Approval

| Component | Description |
| :--- | :--- |
| **ML Core & Feature Engineering**| The central "brain" where features are created and the ML models are trained to generate forecasts. |
| **Availability Forecast Model** | The core regression model that predicts the final count of seats that will be released by members for a given match. |
| **Manager Review** | A crucial "human-in-the-loop" step where a Ticketing Manager reviews the forecast recommendation. |
| **Business Rules & Safety Buffer**| The manager applies expert knowledge and a safety margin (e.g., approve 95% of the forecast) to mitigate risk before pushing inventory live. |

### Integration & Sales

| Component | Description |
| :--- | :--- |
| **Ticketing Purchase System**| The club's main backend system that receives the manager-approved seat count and updates inventory. |
| **Ticketing Purchase UI** | The public-facing website where fans can now see and purchase the newly available seats well in advance of the match. |

</details>


## Dataset

To showcase the model's capabilities, this repository uses a synthetically generated dataset engineered to mirror the complexity and statistical properties of real-world `Seient Lliure` data. The feature set is based directly on the variables used in the production model, which are grouped into logical categories to capture every angle of the problem.

By combining historical data with external factors like match importance and weather, we can build a feature set that accurately predicts a member's likelihood of releasing their seat.

<details>
<summary><b>Click to see the full list of features used in the model</b></summary>

</br>

The model uses a wide range of features, categorized to ensure a holistic view of supply and demand drivers.

| Category | Features | Description |
| :--- | :--- | :--- |
| **Match** | Day/Month/Time, Competition, Days-to-match, # Matchday | Core temporal and event-specific details. |
| **Rival** | Position, Points/Goals difference, FIFA ranking, # Trophies, Derby/Clásico | Quantifies the opponent's quality and the match's importance. |
| **Barça Momentum**| Barça Position, Last result, Goals +/-, Top player injured | Captures the team's current form and fan excitement. |
| **Sales and Stock** | Sales historical data, Free-up seats historical data, Ticket prices | Historical supply, demand, and pricing information. |
| **Members and Zones**| Max/Avg free-up per zone, Type of member, Zone, `Seient Lliure` incentives | Member-specific behavior and zone-level characteristics. |
| **Web** | Navigational data, User segmentation, Visits to checkout | Digital analytics signals indicating purchase intent. |
| **Weather** | Storm, Rain, Wind | Weather forecasts that can influence a local member's decision to attend. |
| **External Factors**| Holidays, Day before holiday, Political disturbances, New player(s) | Macro-level factors that can impact attendance. |

- **`final_released_seats`** (Integer): **(Target Variable)** The final, total number of seats that were released by season ticket holders in that zone for that match. This is the value the model aims to predict.

</details>

### Match Excitement Factor

To create a realistic dataset, the generation script doesn't just create random numbers. Instead, it simulates the underlying market dynamics by creating a unified **"Match Excitement Factor"**. This single, powerful variable acts as the primary driver for most of the demand signals in the dataset.

This systemic approach ensures that the relationships between the features in the synthetic dataset are correlated in a logical and realistic way, making it a robust foundation for building and testing a demand forecasting model.

## Modeling

The modeling approach is designed to accurately solve a single, critical business problem: predicting the final number of seats that will become available from season ticket holders. This is a classic supervised regression problem. By deconstructing the problem into its key drivers, we can build a model that reliably forecasts this supply.

This approach creates a predictive asset that the business can use to make proactive decisions, turning a forecasting model into a direct revenue-generating tool.

### 📈 Availability Forecasting

> This stage answers the business question: *"For a given match, how many season ticket seats will ultimately be returned to the club?"*

| Aspect | Description |
| :--- | :--- |
| **Model** | An **`XGBoost` Regressor**. |
| **Rationale** | After exploring several algorithms (including Decision Trees and Neural Networks), XGBoost was chosen for its high performance, speed, and its ability to handle complex, non-linear relationships. It effectively models how factors like opponent strength, day of the week, and team performance interact to influence a member's decision to release their seat. |
| **Features** | The model uses a rich set of features including match context (`opponent_tier`), temporal factors (`days_until_match`), team performance (`team_position`), and external factors (`holidays`) to build a comprehensive view of the drivers behind seat availability. |
| **Application** | The model's forecast is delivered as a **recommendation** to the Ticketing Manager. A safety buffer (e.g., 95% of the forecast) is manually applied by the manager to mitigate risk before the final inventory is pushed live. |
| **Design Choice** | While time-series models could model release patterns over time, a gradient boosting model like `XGBoost` is better suited to predict a single, final outcome (total released seats) based on a wide array of static features for a given match. It excels at capturing the combined impact of all variables at once. |

<details>
<summary><b>Click to see the detailed model performance evaluation</b></summary>
</br>

The success of the SmartBooking system hinges on the accuracy of its core forecast. The model was evaluated against simpler benchmarks to prove its value.

| Source of Prediction | Accuracy |
| :--- | :--- |
| Random Guess | 15% |
| Averages (Mean, Median, etc.) | 45% |
| Domain Experts | 65% |
| **Machine Learning Model** | **85%** |

*Table: Comparison of prediction accuracy across different methods.*

The model's **85% accuracy** was deemed highly successful, providing a strong statistical foundation for the business to act on the forecasts with confidence. The model was also interpreted using **SHAP values** to ensure the relationships it learned were logical and explainable to stakeholders.

</details>

### Validation

Before a full rollout, the system was rigorously validated through a controlled **A/B test** to scientifically measure its business impact. The experiment was designed to isolate the effect of selling tickets based on the forecast, separating it from all other variables.

The results from the A/B tests were overwhelmingly positive, showing a **+15% increase in total ticket sales revenue** for matches where the SmartBooking system was active. This confirmed that we were successfully capturing previously unmet demand without cannibalizing other sales, giving the business full confidence to deploy the system permanently.

<details>
<summary><b>Click to see the full experimental design</b></summary>

#### Experimental Design

The validation used a match-based A/B test, where different matches were assigned to treatment and control groups.

1.  **Treatment vs. Control Groups**: Matches were divided into two groups.
    * **Treatment Group = SmartBooking Enabled**: For these matches, the club used the forecast to sell a calculated number of tickets in advance, before the seats were officially released by members.
    * **Control Group = Standard Process**: For these matches, the club followed the traditional process, only selling tickets after they were officially returned by members.

2.  **Hypothesis**: Our primary hypothesis was that the treatment group (SmartBooking matches) would generate significantly higher total ticket sales revenue compared to the control group, by capturing early demand.

3.  **Duration**: The test was run across a full season, covering a diverse range of matches (league, cup, international) to ensure the results were robust and not specific to a certain type of event.

#### Key metrics tracked

To evaluate the experiment's outcome, we monitored several KPIs for both groups:

* **Primary metric**: Total Ticket Sales Revenue per Match.
* **Secondary metrics**:
    * Ticket Sell-Through Rate (occupancy).
    * Average Order Value (to measure group/family sales).
    * Percentage of Paired Seats Sold.
    * Time of purchase (to confirm we were capturing *early* demand).

</details>


## Structure

While most of the source code for this project is private, this section outlines the full structure:

```bash
FCB_Smart-Booking/
├── .gitignore                      # (Public) Specifies files for Git to ignore.
├── LICENSE                         # (Public) Project license.
├── README.md                       # (Public) This project overview.
├── requirements.txt                # (Private) The requirements file for the full project.
├── config.py                       # (Private) Configuration file for paths and parameters.
├── assets/                         # (Public) Diagrams and images for documentation.
│   ├── sb-cover.jpg
│   └── sb-ll.png
├── data/
│   └── 03_synthetic/
│       └── synthetic_match_data.csv    # (Public) The generated synthetic dataset.
├── models/                         # (Private) Stores trained model artifacts.
│   └── availability_forecast_model.joblib
├── notebooks/      _**_              # (Private) Jupyter notebooks for analysis.
│   └── eda.ipynb
└── src/
    ├── __init__.py                 # (Private) Makes src a Python package.
    ├── data/
    │   └── make_dataset.py           # (Public) The script to generate the synthetic data.
    ├── features/                     # (Private) Scripts for feature engineering.
    │   └── build_features.py
    └── models/                       # (Private) Scripts for model training and prediction.
        ├── train_availability_model.py
        └── predict_availability.py
```

</br>

> [!WARNING]
> * **Data:** All data presented in this public repository is synthetically generated. It is designed to mirror the statistical properties of the original dataset without revealing any confidential information.
> * **Code:** To honor confidentiality agreements, the source code and data for the original project are private. This repository demonstrates the modeling approach and best practices used in the real-world solution.
> * **Complexity:** This repository provides a high-level demonstration of the project's architecture and methodology. Certain implementation details and model complexities have been simplified for clarity.

</br>

<p align="center">🌐 © 2025 t.r.</p>
