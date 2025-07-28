![My Cover](./assets/sb-cover.jpg)

# 🏟️ A Seat Availability Forecasting Engine

<p align="left">
  <img src="https://img.shields.io/badge/License-MIT-lightgrey" alt="License">
  <img src="https://img.shields.io/badge/ML-Supervised-lightgrey" alt="License">
</p>

> An ML system that forecasts seat availability for football matches. **Objective:** To solve the supply-demand imbalance in ticket sales by using machine learning to predict seat availability, maximizing matchday revenue and improving the fan experience at the stadium.

### Outline

- [Key Results](#key-results)
- [Overview](#overview)
- [Architecture](#architecture)
- [Dataset](#dataset)
- [Modeling](#modeling)
- [Structure](#structure)

---

## Key Results

| Metric                      | Result                          | Description |
| :-------------------------- | :------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------- |
| 📈 Revenue Growth           | **+15%** in Ticket Sales        | Enabled by confidently selling tickets predicted to become available, capturing previously lost demand. Confirmed via A/B testing.         |
| 💰 Average Order Value      | **+40%** Increase               | A direct result of guaranteeing paired seating for families and groups, which encourages larger transactions.                                |
| 🎯 Forecast Accuracy        | **89%** Accuracy (R²)           | The model's predictions of final seat availability were highly accurate, providing a reliable basis for advance sales.                       |
| ⭐ Fan Experience           | Paired Seating Guaranteed | Transformed the fan purchase journey from a lottery to a reliable process, drastically reducing empty single seats and improving atmosphere. |
| 📢 Marketing Efficiency     | Improved ROAS **14%** | A wider time window to market the match allows for more effective campaign planning and better Return on Ad Spend.                  |
| 🛡️ Fraud Reduction         | Mitigated scalping | By delaying the issuance of physical tickets until 48 hours before kick-off, the system combats fraud and unauthorized resale.             |

## Overview

The SmartBooking engine acts as a forecasting layer. It ingests historical sales data and contextual factors to predict, weeks in advance, how many seats will ultimately be freed up by season ticket holders in each stadium zone. This forecast empowers the club to sell a calculated number of tickets *before* they are officially released, bridging the gap between fan demand and latent supply. This moves the club from a reactive sales model to a proactive, predictive one.

| 🚩 The Problem | 💡 The Solution |
| :--------------------------- | :---------------------------- |
| **"Sold Out" Illusion**: Fans faced "Sold Out" messages, unaware that 40% of released seats appear in the last 72 hours. | **Advance Availability**: Predicts final seat count weeks in advance, allowing the club to sell tickets for seats that are not yet officially released. |
| **Lost Revenue**: High demand went unmet due to the delay in seat returns, leading to significant lost revenue for the club. | **Revenue Capture**: Unlocks millions in sales by matching early fan demand with predicted inventory. |
| **Poor Fan Experience**: The unpredictable nature of ticket availability frustrated fans and fueled secondary resale markets. | **Guaranteed Experience**: Offers fans, especially families and groups, guaranteed paired seating, improving satisfaction and trust. |
| **Seat Fragmentation**: Last-minute releases often resulted in many isolated single seats that were difficult to sell. | **Optimized Occupancy**: By selling seats early, the system facilitates better seat allocation, reducing empty singles and maximizing attendance. |

The diagram below illustrates the conceptual framework. The system addresses the core problem of information asymmetry: season ticket holders release seats late, creating a frustrating experience for fans who see matches as "Sold Out" when thousands of seats will eventually become available.

<p align="center">
  <img src="./assets/sb-hl.png" alt="High-level Project Diagram" width="2000">
  <br>
  <em>Fig. 1: A high-level diagram of the SmartBooking Engine.</em>
</p>


## Architecture

The general workflow is as follows:
1.  **Data Sources** are ingested, focusing on historical seat release patterns and match context.
2.  The **Forecasting Engine** uses a machine learning model to predict the final number of available seats per zone.
3.  This forecast is sent to the **Ticketing System**, which opens a corresponding number of seats for advance sale, allowing fans to purchase tickets earlier.

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
| **Season Ticket Holder Data** | Historical data on seat release behavior (`Seient Lliure`), including timing and frequency, for different member segments. |
| **Match & Competition Data** | Foundational information about each match, such as opponent, date, and competition type, which strongly influences attendance. |
| **Historical Availability** | Time-series data tracking how many seats became available day-by-day for past matches. |
| **External Demand Signals** | Contextual data like holidays, weather forecasts, and team momentum that can affect a season ticket holder's decision to attend. |

### Forecasting Engine

| Component | Description |
| :--- | :--- |
| **Data Ingestion & Centralization** | Gathers data from all sources into a unified data store for processing and feature engineering. |
| **ML Core & Feature Engineering** | The central "brain" where features are created and the machine learning models are trained and executed to generate forecasts. |
| **Availability Forecast Model** | The core regression model that predicts the final count of seats that will be released by season ticket holders for a given match. |
| **Match Clustering** | An algorithm that groups similar past matches to provide a contextual baseline for the forecast model. |
| **Forecast Output** | The final prediction from the engine: a specific number of seats per zone that are expected to become available. |

### Integration & Sales

| Component | Description |
| :--- | :--- |
| **Business Rules Module** | Applies a safety buffer to the forecast (e.g., release 95% of predicted seats) to manage the risk of over-selling. |
| **REST API** | The communication layer that sends the final, adjusted seat count to the live ticketing system. |
| **Ticketing Purchase System** | The club's main backend system that receives the seat count and updates inventory, making them available for public sale. |
| **Ticketing Purchase UI** | The public-facing website where fans can now see and purchase the newly available seats well in advance of the match. |

</details>


## Dataset

To showcase the model's capabilities, this repository uses a synthetically generated dataset. This dataset is engineered to mirror the complexity and statistical properties of real-world seat release patterns from season ticket holders (`Seient Lliure`) for a top-tier football club.

The dataset simulates:
* **A focused set of matches:** It contains data for **10 unique matches**, representing a diverse sample of fixtures.
* **Complete release history:** For each match, it simulates the daily pattern of seat releases from season ticket holders over a **90-day period** before the match.
* **Zone-level granularity:** Each record is broken down by **5 distinct seating zones**, each with its own capacity and historical release behavior.

The core of the dataset is designed to model the behavior of season ticket holders. By combining historical data with external factors like match importance and weather, we can build a feature set that accurately predicts their likelihood of releasing their seats.

<details>
<summary><b>Click to see the full list of features</b></summary>

</br>

-   `days_until_match` (*Integer*): The number of days remaining before the match. A key feature, as most seats are released closer to the match date.
-   `ea_opponent_strength` (*Integer*): A rating of the opponent's strength based on the EA Sports FC game, used as a proxy for match attractiveness.
-   `holidays` (*Boolean*): `True` if the match day falls on or near a local or national holiday.
-   `match_id` (*Integer*): A unique identifier for each football match.
-   `opponent_tier` (*String*): A categorical rating of the opponent's quality and appeal (`A++`, `A`, `B`, `C`).
-   `seat_zone` (*String*): The name of the seating zone in the stadium (e.g., 'Gol Nord', 'Lateral', 'VIP').
-   `season_ticket_holder_segment` (*String*): A category for the season ticket holder (e.g., 'Family', 'Long-time member', 'Corporate') based on historical behavior.
-   `team_position` (*Integer*): The team's current position in the league table at the time of the match.
-   `top_player_injured` (*Boolean*): `True` if a key player is injured and not expected to play.
-   `weather_forecast` (*String*): The predicted weather for the match day ('Sunny', 'Windy', 'Rain').
-   `weekday_match` (*Boolean*): `True` if the match is played on a weekday (Monday-Friday).
-   `zone_total_season_tickets` (*Integer*): The total number of season tickets in that specific zone.
-   **`final_released_seats`** (*Integer*): **(Target Variable)** The final, total number of seats that were released by season ticket holders in that zone for that match. This is the value the model aims to predict.

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

The modeling approach is designed to accurately solve a single, critical business problem: predicting the final number of seats that will become available from season ticket holders. By deconstructing the problem into its key drivers–match characteristics, opponent quality, temporal factors–we can build a regression model that reliably forecasts this supply.

This approach is about creating a predictive asset that the business can use to make proactive decisions, turning a forecasting model into a direct revenue-generating tool.

### 📈 Availability Forecasting

> This stage answers the business question: *"For a given match, how many season ticket seats will ultimately be returned to the club?"*

| Aspect | Description |
| :--- | :--- |
| **Model** | An **`XGBoost` Regressor**. |
| **Rationale** | XGBoost was chosen for its high performance, speed, and its ability to handle complex, non-linear relationships between features. It effectively models how factors like opponent strength, day of the week, and team performance interact to influence a season ticket holder's decision to release their seat. |
| **Features** | The model uses a rich set of features including match context (`opponent_tier`, `weekday_match`), team performance (`team_position`), and external factors (`holidays`) to build a comprehensive view of the drivers behind seat availability. |
| **Application** | The trained model's forecast is used to determine the number of tickets that can be safely sold in advance. A business rule applies a confidence buffer (e.g., 95%) to the prediction to mitigate the risk of over-selling. |
| **Design Choice** | While time-series models like `Prophet` could model release patterns over time, a gradient boosting model like `XGBoost` is better suited to predict a single, final outcome (total released seats) based on a wide array of static features for a given match. It excels at capturing the combined impact of all variables at once. |

<details>
<summary><b>Click to see the detailed model performance evaluation</b></summary>
</br>

The success of the SmartBooking system hinges on the accuracy of its core forecast. The primary goal was to create a model with high predictive power and a low, understandable error margin. The key metric is the **R² Score**, which measures how much of the variance in seat availability the model can explain.

| Metric | Value | Rationale |
| :--- | :--- | :--- |
| **R² Score** (Primary Metric) | **0.89** | **Why we chose it:** An R² of 0.89 means the model explains 89% of the variability in seat releases. This high value gives the business strong confidence that the predictions are reliable and closely reflect reality. |
| **Mean Absolute Error (MAE)** | **~85 seats** | **For business context:** MAE tells us that, on average, our forecast is off by about 85 seats for a given match and zone. This provides a clear, absolute measure of the expected error margin for inventory planning. |
| **Root Mean Squared Error (RMSE)**| **~110 seats**| **For risk assessment:** RMSE penalizes larger errors more heavily. A higher RMSE relative to MAE indicates the model occasionally makes larger prediction errors. This is crucial for setting the safety buffer to avoid over-selling tickets. |

The performance was deemed **highly successful**. An R² of 0.89 provides a strong statistical foundation, while the MAE and RMSE give the business team a clear and actionable understanding of the model's error range.

</details>

### Validation

Before a full rollout, the system was rigorously validated through a controlled **A/B test** to scientifically measure its business impact. The experiment was designed to isolate the effect of selling tickets based on the forecast, separating it from all other variables.

The results from the A/B tests were overwhelmingly positive, showing a **+15% increase in total ticket sales revenue** for matches where the SmartBooking system was active. This confirmed that we were successfully capturing previously unmet demand without cannibalizing other sales, giving the business full confidence to deploy the system permanently.

<details>
<summary><b>Click to see the full experimental design</b></summary>

#### Experimental Design

The validation used a match-based A/B test, where different matches were assigned to treatment and control groups.

1.  **Treatment vs. Control Groups**: Matches were randomly assigned to one of two groups.
    * **Treatment Group = SmartBooking Enabled**: For these matches, the club used the forecast to sell a calculated number of tickets in advance, before the seats were officially released by season ticket holders.
    * **Control Group = Standard Process**: For these matches, the club followed the traditional process, only selling tickets after they were officially returned by season ticket holders.

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
├── .gitignore                      # (Public) Specifies files for Git to ignore.
├── LICENSE                         # (Public) Project license.
├── README.md                       # (Public) This project overview.
├── requirements.txt                # (Private) The requirements file for the full project.
├── config.py                       # (Private) Configuration file for paths and parameters.
├── assets/                         # (Public) Diagrams and images for documentation.
│   ├── sb-hl.png
│   └── sb-ll.png
├── data/
│   └── 03_synthetic/
│       └── synthetic_match_data.csv    # (Public) The generated synthetic dataset.
├── models/                         # (Private) Stores trained model artifacts.
│   └── availability_forecast_model.joblib
├── notebooks/                      # (Private) Jupyter notebooks for analysis.
│   └── eda.ipynb
└── src/
    ├── __init__.py                 # (Private) Makes src a Python package.
    ├── data/
    │   └── make_dataset.py           # (Public) The script to generate the synthetic data.
    ├── features/                     # (Private) Scripts for feature engineering.
    │   └── build_features.py
    └── models/                       # (Private) Scripts for model training and prediction.
        ├── train_availability_model.py
        └── predict_availability.py

</br>

> [!WARNING]
> * **Data:** All data presented in this public repository is synthetically generated. It is designed to mirror the statistical properties of the original dataset without revealing any confidential information.
> * **Code:** To honor confidentiality agreements, the source code and data for the original project are private. This repository demonstrates the modeling approach and best practices used in the real-world solution.
> * **Complexity:** This repository provides a high-level demonstration of the project's architecture and methodology. Certain implementation details and model complexities have been simplified for clarity.

</br>

<p align="center">🌐 © 2025 t.r.</p>
