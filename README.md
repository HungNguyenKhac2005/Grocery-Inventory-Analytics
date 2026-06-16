# 🛒 Grocery Inventory Analytics: End-to-End Data Pipeline

## 🌟 1. Project Overview

This end-to-end data analytics project simulates a real-world enterprise pipeline to optimize grocery inventory management. Leveraging a dataset from Kaggle, the project implements an automated ETL pipeline, cloud data warehousing, in-depth SQL business analysis, and interactive dashboarding to drive strategic business decisions.

### 🚀 Key Achievements

- **Automated ETL Pipeline:** Engineered a robust data ingestion, cleaning, and transformation workflow using **Python (Pandas, Scikit-Learn)**, fully automated and orchestrated via **Apache Airflow** in **Docker**.
- **Cloud Data Warehousing:** Deployed the target database in the cloud using **Neon PostgreSQL** hosted on **AWS (Asia Pacific - Singapore)** for high availability.
- **Advanced SQL Analytics:** Performed deep-dive SQL analysis to uncover **10 high-value business insights** regarding stock levels, warehouse performance, supplier reliability, and shelf-life expiration risks.
- **Interactive Visualization:** Designed a comprehensive executive dashboard in **Power BI Desktop** directly connected to the Cloud DWH, with automated report updates configured via **Power BI Service**.

### ⚠️ Current Limitations

- The orchestration pipeline (Apache Airflow) is currently hosted locally via Docker, meaning scheduled execution relies on the host machine being active.

---

## 🏗️ 2. System Architecture

![System Architecture]([Your image link here])

**Architecture Explanation and Workflow Description:**

- **Workflow 1 (Data Source):** Data is downloaded from the reputable data platform Kaggle and stored in a flat `.csv` file format.
- **Workflow 2 (Automated ETL System):** Python (`data_processing.py`) is used to extract data from the CSV file. The processing steps include: handling missing data, removing duplicates, handling outliers, and normalizing data types. Clean data is then loaded into the Data Warehouse. This entire process is automated using **Apache Airflow** running in isolated **Docker** containers.
- **Workflow 3 (Cloud Data Warehouse):** The analytical Data Warehouse is built using the **PostgreSQL** database management system, running on the **AWS (Asia Pacific - Singapore)** cloud platform through **Neon.tech's** Serverless solution.
- **Workflow 4 (Data Analysis):** Visual Studio Code integrated with the SQLTools extension is used to connect directly to the Cloud Data Warehouse. Queries and data analysis are performed directly on the server using **SQL**.
- **Workflow 5 (Visualization & Reporting):** Executive dashboards are built on **Power BI Desktop** based on insights retrieved using SQL. Subsequently, automated report data refresh flows (Scheduled Refresh) are configured via the **Power BI Cloud Service**.

---

## 🛠️ 3. Tech Stack

- **IDE:** Visual Studio Code
- **Programming Languages:** Python, SQL, DAX
- **Libraries/Frameworks:** Pandas, Numpy, Matplotlib, Seaborn, Scikit-Learn, Os, SQLAlchemy
- **Database & Data Warehouse:** PostgreSQL, Neon.tech
- **Orchestration (Automation):** Apache Airflow
- **Containerization:** Docker
- **Business Intelligence (BI):** Power BI Desktop, Power BI Cloud Service
- **Cloud Platform:** Amazon Web Services (AWS)

---

## 📊 4. Dataset Overview

The raw dataset `grocery_inventory.csv` is collected from Kaggle with the following structure:

- **Rows:** 989
- **Columns:** 10
- **Key Features:**
  - _Date Information:_ date_received, last_order_date, expiration_date
  - _Product Information:_ Product_id, Product_name, Category
  - _Supplier Information:_ Supplier_id, supplier_name
  - _Warehouse Information:_ warehouse_locations
  - _Inventory Status:_ Status

---

## 🔍 5. SQL Analytics *(see details in the [reports.pdf](file:///C:/Python/Data_Science_Atifficial_Interligent/project_datascience%20_AI/Project%20CV/Personal%20Projects/Grocery_Inventory_Analytics_git/reports/reports.pdf) file in the [reports](file:///C:/Python/Data_Science_Atifficial_Interligent/project_datascience%20_AI/Project%20CV/Personal%20Projects/Grocery_Inventory_Analytics_git/reports) folder)*

### 5.1. Product Count by Category

```sql
CREATE VIEW statistical_category AS
SELECT
    catagory,
    COUNT(*) AS total
FROM grocery_inventory_table
GROUP BY catagory
ORDER BY total DESC;

SELECT * FROM statistical_category;
```

### 5.2. Expiration Risk Analysis (Within the Next 30 and 60 Days)

```sql
CREATE VIEW vw_inventory_shelf_life_analysis_ AS
WITH expiration_analysis AS (
    SELECT
        *,
        expiration_date - date_received AS shelf_life_days
    FROM grocery_inventory_table
),
expiration_labels AS (
    SELECT
        *,
        CASE
            WHEN shelf_life_days < INTERVAL '30 days' AND shelf_life_days >= '0 days' THEN '30 days'
            WHEN shelf_life_days >= INTERVAL '30 days' AND shelf_life_days < INTERVAL '60 days' THEN '30 - 60 days'
            ELSE '> 60 days'
        END AS labels_expiration
    FROM expiration_analysis
)
SELECT * FROM expiration_labels;

-- Expiration risk statistics by Category
SELECT
    catagory,
    SUM(CASE WHEN labels_expiration = '30 days' THEN 1 ELSE 0 END) AS total_expiring_30_days,
    SUM(CASE WHEN labels_expiration = '30 - 60 days' THEN 1 ELSE 0 END) AS total_expiring_60_days
FROM vw_inventory_shelf_life_analysis_
GROUP BY catagory;

-- Expiration risk statistics by Warehouse Location
SELECT
    Warehouse_Location,
    SUM(CASE WHEN labels_expiration = '30 days' THEN 1 ELSE 0 END) AS total_expiring_30_days,
    SUM(CASE WHEN labels_expiration = '30 - 60 days' THEN 1 ELSE 0 END) AS total_expiring_60_days
FROM vw_inventory_shelf_life_analysis_
GROUP BY Warehouse_Location;
```

### 5.3. Supplier Performance Ranking

**Business Question:** Filter out the Top 3 suppliers with the most _Active_ items, and the Top 3 suppliers with the most _Discontinued_ items.

```sql
CREATE VIEW supplier_status_ranking_view AS
WITH supplier_status_summary AS (
    SELECT
        Supplier_Name,
        COUNT(*) FILTER(WHERE status_ = 'Discontinued') AS total_Discontinued,
        COUNT(*) FILTER(WHERE status_ = 'Active') AS total_Active
    FROM grocery_inventory_table
    GROUP BY Supplier_Name
),
supplier_status_ranking AS (
    SELECT
        *,
        RANK() OVER (ORDER BY total_Discontinued DESC) AS total_Discontinued_rank,
        RANK() OVER (ORDER BY total_Active DESC) AS total_Active_rank
    FROM supplier_status_summary
)
SELECT * FROM supplier_status_ranking;

-- Filter Top 3 Active suppliers
SELECT * FROM supplier_status_ranking_view
WHERE total_Active_rank <= 3;

-- Filter Top 3 Discontinued suppliers
SELECT * FROM supplier_status_ranking_view
WHERE total_Discontinued_rank <= 3;
```

---

## 💡 6. Business Recommendations *(see details in the [reports.pdf](file:///C:/Python/Data_Science_Atifficial_Interligent/project_datascience%20_AI/Project%20CV/Personal%20Projects/Grocery_Inventory_Analytics_git/reports/reports.pdf) file in the [reports](file:///C:/Python/Data_Science_Atifficial_Interligent/project_datascience%20_AI/Project%20CV/Personal%20Projects/Grocery_Inventory_Analytics_git/reports) folder)*

Based on the insights extracted from the Data Warehouse, below are the proposed strategic actions for executive leadership:

- **🎯 Near-Expiry Clearance Marketing Campaigns:** In the next 30 and 60 days, a large volume of goods will expire and face disposal. Sales and Marketing teams must immediately launch promotional campaigns, including cross-selling and up-selling, to clear inventory and prevent financial losses. Resolution efforts should focus on three product groups: **Fruits and Vegetables, Dairy**, and **Grains & Pulses**, as these have the highest volumes of near-expiry inventory.
- **🚫 Terminate Underperforming Suppliers (Backordered):** Currently, the backorder (delayed delivery/deferred orders) rate is at a high-risk level: >40% high/medium risk, ~40% low risk, and only <20% operating stably. Notably, **33 suppliers have reached a 100% backorder rate**. The Purchasing department is requested to terminate contracts with these 33 partners immediately. Concurrently, identify backup partners for the high-backorder group and issue warnings/delivery commitment requests to the remaining suppliers.
- **🚨 Mitigate PR Crisis Risks:** The data indicates a high rate of "expired items remaining in the delivery flow to customers." This poses a severe threat to brand reputation and could trigger customer boycotts. Warehouse and Operations management teams must immediately halt the dispatch of these faulty orders. Urgently recall affected orders and implement appropriate compensation policies for orders already delivered.
- **💰 Optimize Logistics Costs:** Three product groups (Fruits and Vegetables, Dairy, Grains & Pulses) have highly fragmented supplier networks, driving up operations, warehousing, and transportation costs. The Purchasing team is requested to evaluate and consolidate strategic suppliers to minimize costs (Cost Optimization).
- **📈 Restructure Seasonal Sourcing Model (Seasonality):** Current procurement volumes are distributed too evenly across months, leading to capital lockup and inefficiencies. Proposed new procurement process:
  - _January, February, March:_ Reduce import volumes (due to decreased post-holiday shopping demand and remaining customer stockpiles).
  - _April to August:_ Stabilize import volumes and maintain safe inventory levels.
  - _September, October, November:_ Maximize capital allocation to scale up inventory sourcing in preparation for the peak holiday season, preventing supply shortages and price volatility (cost inflation).
  - _December:_ Pause large-batch shipments, opting only for localized, fill-in purchases based on market demand.
