# 🛒 Grocery Inventory Analytics: End-to-End Data Pipeline

## 🌟 1. Tổng quan về dự án (Project Overview)

This end-to-end data analytics project simulates a real-world enterprise pipeline to optimize grocery inventory management. Leveraging a dataset from Kaggle, the project implements an automated ETL pipeline, cloud data warehousing, in-depth SQL business analysis, and interactive dashboarding to drive strategic business decisions.

### 🚀 Key Achievements
* **Automated ETL Pipeline:** Engineered a robust data ingestion, cleaning, and transformation workflow using **Python (Pandas, Scikit-Learn)**, fully automated and orchestrated via **Apache Airflow** in **Docker**.
* **Cloud Data Warehousing:** Deployed the target database in the cloud using **Neon PostgreSQL** hosted on **AWS (Asia Pacific - Singapore)** for high availability.
* **Advanced SQL Analytics:** Performed deep-dive SQL analysis to uncover **10 high-value business insights** regarding stock levels, warehouse performance, supplier reliability, and shelf-life expiration risks.
* **Interactive Visualization:** Designed a comprehensive executive dashboard in **Power BI Desktop** directly connected to the Cloud DWH, with automated report updates configured via **Power BI Service**.

### ⚠️ Current Limitations
* The orchestration pipeline (Apache Airflow) is currently hosted locally via Docker, meaning scheduled execution relies on the host machine being active.

---

## 🏗️ 2. Kiến trúc của dự án (System Architecture)

![System Architecture]([Link ảnh của bạn chèn vào đây])

**Giải thích kiến trúc và mô tả luồng hoạt động:**

* **Luồng 1 (Nguồn dữ liệu):** Dữ liệu được tải về từ nền tảng cung cấp dữ liệu uy tín Kaggle và lưu trữ dưới định dạng tệp phẳng `.csv`.
* **Luồng 2 (Hệ thống ETL Tự động):** Sử dụng Python (`data_processing.py`) để trích xuất dữ liệu từ file csv. Quá trình xử lý bao gồm: xử lý dữ liệu thiếu, loại bỏ trùng lặp, xử lý ngoại lai (outliers), chuẩn hóa kiểu dữ liệu. Sau đó nạp (Load) dữ liệu sạch vào Data Warehouse. Toàn bộ quy trình này được tự động hóa bằng **Apache Airflow** hoạt động trên môi trường cô lập **Docker**.
* **Luồng 3 (Cloud Data Warehouse):** Kho dữ liệu phân tích (Data Warehouse) được xây dựng bằng hệ quản trị cơ sở dữ liệu **PostgreSQL** chạy trên nền tảng điện toán đám mây **AWS (Asia Pacific - Singapore)** thông qua giải pháp Serverless của **Neon.tech**.
* **Luồng 4 (Phân tích dữ liệu):** Sử dụng IDE Visual Studio Code tích hợp extension SQLTools để kết nối trực tiếp đến Cloud Data Warehouse. Tiến hành truy vấn và phân tích dữ liệu trực tiếp trên Server bằng **SQL**.
* **Luồng 5 (Trực quan hóa & Báo cáo):** Dựa trên các Insights lấy được từ SQL, xây dựng Dashboard điều hành trên **Power BI Desktop**. Sau đó, thiết lập luồng tự động cập nhật dữ liệu báo cáo (Scheduled Refresh) thông qua đám mây **Power BI Cloud Service**.

---

## 🛠️ 3. Công nghệ sử dụng (Tech Stack)

* **IDE:** Visual Studio Code
* **Programming Languages:** Python, SQL, DAX
* **Libraries/Frameworks:** Pandas, Numpy, Matplotlib, Seaborn, Scikit-Learn, Os, SQLAlchemy
* **Database & Data Warehouse:** PostgreSQL, Neon.tech
* **Orchestration (Automation):** Apache Airflow
* **Containerization:** Docker
* **Business Intelligence (BI):** Power BI Desktop, Power BI Cloud Service
* **Cloud Platform:** Amazon Web Services (AWS)

---

## 📊 4. Giới thiệu về bộ dữ liệu (Dataset Overview)

Tập dữ liệu thô `grocery_inventory.csv` được thu thập từ Kaggle với cấu trúc như sau:

* **Số dòng (Rows):** 989
* **Số cột (Columns):** 10
* **Key Features:**
    * *Date Information:* date_received, last_order_date, expiration_date
    * *Product Information:* Product_id, Product_name, Category
    * *Supplier Information:* Supplier_id, supplier_name
    * *Warehouse Information:* warehouse_locations
    * *Inventory Status:* Status

---

## 🔍 5. Phân tích dữ liệu (SQL Analytics)

### 5.1. Thống kê số lượng sản phẩm theo danh mục (Category)
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

### 5.2. Phân tích rủi ro hàng hóa hết hạn (Trong 30 và 60 ngày tới)
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

-- Thống kê rủi ro hết hạn theo Category
SELECT 
    catagory,
    SUM(CASE WHEN labels_expiration = '30 days' THEN 1 ELSE 0 END) AS total_expiring_30_days,
    SUM(CASE WHEN labels_expiration = '30 - 60 days' THEN 1 ELSE 0 END) AS total_expiring_60_days
FROM vw_inventory_shelf_life_analysis_
GROUP BY catagory;

-- Thống kê rủi ro hết hạn theo khu vực Kho (Warehouse Location)
SELECT 
    Warehouse_Location,
    SUM(CASE WHEN labels_expiration = '30 days' THEN 1 ELSE 0 END) AS total_expiring_30_days,
    SUM(CASE WHEN labels_expiration = '30 - 60 days' THEN 1 ELSE 0 END) AS total_expiring_60_days
FROM vw_inventory_shelf_life_analysis_
GROUP BY Warehouse_Location;
```

### 5.3. Xếp hạng trạng thái đối tác (Supplier Performance)
**Business Question:** Lọc ra Top 3 nhà cung cấp có nhiều mã hàng *Active* nhất, và Top 3 nhà cung cấp có nhiều mã *Discontinued* nhất.
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

-- Lọc Top 3 nhà cung cấp Active
SELECT * FROM supplier_status_ranking_view
WHERE total_Active_rank <= 3;

-- Lọc Top 3 nhà cung cấp Discontinued
SELECT * FROM supplier_status_ranking_view
WHERE total_Discontinued_rank <= 3;
```

---

## 💡 6. Đề xuất chiến lược (Business Recommendations)

Dựa trên các insights được bóc tách từ Data Warehouse, dưới đây là các hành động chiến lược đề xuất cho ban điều hành:

* **🎯 Chiến dịch Marketing xả hàng cận Date:** Trong 30 và 60 ngày tới sẽ có một số lượng lớn hàng hóa hết hạn và phải tiêu hủy. Yêu cầu đội Sale và Marketing lập tức triển khai các chiến dịch khuyến mãi bán chéo (Cross-sell/Up-sell) để đẩy hàng, tránh gây lỗ cho công ty. Trọng tâm giải quyết nằm ở 3 nhóm hàng: **Fruits and Vegetables, Dairy** và **Grains & Pulses** vì đây là các nhóm có khối lượng sắp hết hạn cao nhất.
* **🚫 Cắt giảm nhà cung cấp kém hiệu quả (Backordered):** Hiện tại, tỷ lệ giao hàng chậm/nợ đơn (Backordered) đang ở mức rủi ro cao: >40% ở mức cao/trung bình, ~40% ở mức thấp và chỉ <20% hoạt động ổn định. Đặc biệt, có tới **33 nhà cung cấp chạm mức Backordered 100%**. Yêu cầu bộ phận Purchasing chấm dứt hợp đồng ngay lập tức với nhóm 33 đối tác này. Đồng thời, tìm kiếm đối tác dự phòng cho nhóm Backordered cao và phát cảnh báo cam kết tiến độ giao hàng đối với nhóm còn lại.
* **🚨 Ngăn chặn rủi ro khủng hoảng truyền thông:** Dữ liệu cho thấy tỷ lệ "Hàng đã hết hạn nhưng vẫn nằm trong luồng giao cho khách" đang ở mức rất cao. Điều này vô cùng nguy hiểm tới danh tiếng thương hiệu và có thể dẫn đến sự tẩy chay của khách hàng. Yêu cầu đội ngũ quản lý Kho và Vận hành đình chỉ ngay quá trình xuất kho các đơn hàng lỗi này. Khẩn trương thu hồi và có chính sách bồi thường thỏa đáng đối với các đơn đã lỡ giao.
* **💰 Tối ưu hóa chi phí Logistics:** Ba nhóm sản phẩm (Fruits and Vegetables, Dairy, Grains & Pulses) đang có mạng lưới nhà cung cấp quá phân mảnh, làm chi phí vận hành, lưu kho và vận tải bị đẩy lên cao vọt. Yêu cầu đội Purchasing tiến hành đánh giá và gom nhóm nhà cung cấp chiến lược để giảm thiểu chi phí (Cost Optimization).
* **📈 Tái cấu trúc mô hình nhập hàng theo mùa vụ (Seasonality):** Sản lượng nhập hàng hiện tại đang phân bổ quá đều đặn giữa các tháng, gây đọng vốn và thiếu hiệu quả. Đề xuất quy trình nhập hàng mới:
    * *Tháng 1, 2, 3:* Cắt giảm sản lượng nhập khẩu (do nhu cầu mua sắm sau Tết giảm và lượng hàng tích trữ của khách hàng vẫn còn).
    * *Tháng 4 đến 8:* Đưa sản lượng nhập khẩu về mức cân bằng và duy trì lượng tồn kho an toàn.
    * *Tháng 9, 10, 11:* Đẩy mạnh tổng lực nguồn vốn để nhập hàng, chuẩn bị cho mùa vụ cao điểm lễ Tết nhằm tránh tình trạng khan hiếm nguồn cung và biến động giá (Cost inflation).
    * *Tháng 12:* Tạm dừng nhập lô lớn, chỉ nhập bổ sung (Fill-in) cục bộ theo nhu cầu thị trường.
