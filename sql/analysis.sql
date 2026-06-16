
-- Data Analyst: Nguyễn Khắc Hưng
-- Ngày: 11-6-2026
-- Khoa: Công Nghệ Thông Tin
-- Nghành: Khoa Học Dữ Liệu
-- Chuyên Nghành: Phân Tích Dữ Liệu Trong Kinh Tế Và Tài Chính

-- PHÂN TÍCH DỮ LIỆU QUẢN LÝ TỒN KHO CỦA CHUỖI TẠP HÓA

-- Lấy 5 dòng dữ liệu đầu tiên
select
* 
from grocery_inventory_table
limit 5;

-- Phân tích thống kê
-- Thống kê về category
create view statistical_category as
select
catagory,
count(*) as total
from grocery_inventory_table
group by catagory
order by total;

select
*
from statistical_category;

-- Thống kê về supplier_name
create view statistical_supplier_name as
select
supplier_name,
count(*) as total
from grocery_inventory_table
group by supplier_name
order by total;

select
*
from 
statistical_supplier_name;

--Thống kê về status
select
status_,
count(*) as total
from grocery_inventory_table
group by status_
order by total;

-- Thống kê top 10 sản phẩm bán chạy nhất
with product_frequency as (
select
product_name,
count(product_name) as total
from grocery_inventory_table
group by product_name
order by total desc
),
rank_product_frequency as (
select
*,
rank() over (order by total) as rankk
from product_frequency
)
select
*
from 
rank_product_frequency
where rankk <= 10;

-- Phân tích cảnh báo hàng hóa cận date
-- Câu hỏi kinh doanh: Có bao nhiêu sản phẩm sẽ hết hạn trong vòng 30 ngày và 60 ngày tới? Phân bổ số lượng này theo từng Warehouse_Location và Category?.
create view vw_inventory_shelf_life_analysis_ as
with expiration_analysis as (
select 
*,
expiration_date - date_received as shelf_life_days
from grocery_inventory_table
), 
expiration_labels as (
    select 
    *,
    case
        when shelf_life_days < interval '30 days' and shelf_life_days >= '0 days' then '30 days'
        when shelf_life_days >= interval '30 days' and shelf_life_days < interval '60 days' then '30 - 60 days'
        else '> 60 days'
    end as labels_expiration
    from expiration_analysis
)
select 
* 
from 
expiration_labels;

select 
catagory,
sum(case
        when labels_expiration = '30 days' then 1
        else 0
    end) as total_expiring_30_days,
sum(case
        when labels_expiration = '30 - 60 days' then 1
        else 0
    end) as total_expiring_60_days
from vw_inventory_shelf_life_analysis_
group by 
catagory;

select 
Warehouse_Location,
sum(case
        when labels_expiration = '30 days' then 1
        else 0
    end) as total_expiring_30_days,
sum(case
        when labels_expiration = '30 - 60 days' then 1
        else 0
    end) as total_expiring_60_days
from vw_inventory_shelf_life_analysis_
group by 
Warehouse_Location;

-- Phân tích điểm nghẽn nguồn cung
-- Câu hỏi kinh doanh: Tỷ lệ phần trăm các mã hàng đang ở trạng thái Backordered (thiếu hàng chờ giao) trên tổng số mã hàng của từng Supplier_Name là bao nhiêu?
create view supplier_backorder_rate as
with supplier_analysis as (
select 
Supplier_Name,
count(*) as total_supply,
count(*) filter (where status_ = 'Backordered') as total_Backordered
from grocery_inventory_table
group by Supplier_Name
)
select 
Supplier_Name,
total_supply,
total_Backordered,
round(((total_Backordered::float/total_supply::float) * 100.0)::numeric, 2) as percent
from supplier_analysis
order by percent desc;

select
* 
from supplier_backorder_rate;

with supplier_risk_summary as (
select
count(*) filter (where percent > 50.00) as high_risk_suppliers,
count(*) filter (where percent < 50.00 and percent > 16.67) as medium_risk_suppliers,
count(*) filter (where percent < 16.67) as low_risk_suppliers,
count(*) as total
from supplier_backorder_rate
)
select
high_risk_suppliers,
round(((high_risk_suppliers/total::float) * 100.0)::numeric, 2) as percent_high_risk_suppliers,
medium_risk_suppliers,
round(((medium_risk_suppliers/total::float) * 100.0)::numeric, 2) as percent_medium_risk_suppliers,
low_risk_suppliers,
round(((low_risk_suppliers/total::float) * 100.0)::numeric, 2) as percent_low_risk_suppliers,
total
from supplier_risk_summary;

-- Phân tích rà soát rủi ro pháp lý và lỗi hệ thống 
-- Câu hỏi kinh doanh: Nếu khách hàng đặt mua một món hàng đã hết hạn, công ty sẽ đối mặt với khủng hoảng truyền thông. Câu query này giúp anh audit lại quy trình xuất kho và tính toàn vẹn của dữ liệu hệ thống?
create view vw_expired_order_violations as
with expiration_audit as (
select 
*,
last_order_date - expiration_date as days_after_expiration
from grocery_inventory_table
),
order_expiration_status as (
    select 
    *,
    case
        when days_after_expiration < interval '0 days' then 'Order Before Expiration'
        when days_after_expiration > interval '0 days' then 'Order after Expiration'
        else 'order on Expiration Date'
    end as order_expiration_status
    from expiration_audit
)

select
product_name,
product_id
from order_expiration_status
where order_expiration_status = 'Order after Expiration';

select
*
from vw_expired_order_violations;

select
count(product_id) as total
from vw_expired_order_violations;

-- Phân tích khảo sát sức khỏe kho bãi 
-- Câu hỏi kinh doanh: Kho hàng (Warehouse_Location) nào đang phải gánh nhiều mã hàng Discontinued (ngừng kinh doanh) nhất?
create view vw_warehouse_discontinued_products as 
select 
Warehouse_Location,
count(*) filter (where status_ = 'Discontinued') as total
from grocery_inventory_table
group by Warehouse_Location
order by total desc;

select 
*
from
vw_warehouse_discontinued_products;

select
count(*) filter (where total > 0) as total_have_Discontinued,
round((((count(*) filter (where total > 0))::float / (count(*))::float)*100)::numeric, 2) as percent_have_Discontinued,
count(*) filter (where total <= 0) as total_non_Discontinued,
round((((count(*) filter (where total <= 0))::float / (count(*))::float)*100)::numeric, 2) as percent_non_Discontinued,
count(*) as total
from vw_warehouse_discontinued_products;

-- Phân tích vòng đời sản phẩm lưu kho
-- Câu hỏi kinh doanh: Thời gian trung bình (tính bằng ngày) từ lúc nhận hàng (Date_Received) đến lần đặt hàng cuối cùng (Last_Order_Date) của từng Category là bao nhiêu?
create view vw_category_inventory_lifetime as
with inventory_lifetime_analysis as (
select
*,
last_order_date - date_received as days_until_last_order
from grocery_inventory_table
),
category_inventory_lifetime  as (
select
catagory,
extract(day from days_until_last_order)::int as days_until_last_order_int
from inventory_lifetime_analysis 
)

select 
catagory,
round(avg(days_until_last_order_int), 2) as avg_inventory_lifetime_days
from category_inventory_lifetime 
group by catagory
order by avg_inventory_lifetime_days desc;

select
*
from
vw_category_inventory_lifetime; 

-- Phân tích xếp hạng độ tin cậy của nhà cung cấp
-- Câu hỏi kinh doanh: Lọc ra Top 3 nhà cung cấp (Supplier_Name) cung cấp nhiều mã hàng Active nhất, và Top 3 nhà cung cấp có nhiều mã Discontinued nhất.
create view supplier_status_ranking_view as
with supplier_status_summary  as (
select
Supplier_Name,
count(*) filter(where status_ = 'Discontinued') as total_Discontinued,
count(*) filter(where status_ = 'Active') as total_Active
from 
grocery_inventory_table
group by Supplier_Name
),
supplier_status_ranking as (
select
*,
rank() over (
    order by total_Discontinued desc
) as total_Discontinued_rank,
rank() over (
    order by total_Active desc
) as total_Active_rank
from supplier_status_summary 
)
select 
*
from 
supplier_status_ranking;

select
*
from
supplier_status_ranking_view
where total_Active_rank <= 3;

select
*
from
supplier_status_ranking_view
where total_Discontinued_rank <= 3;

-- Phân tích hành vi tìm nguồn cung ứng 
-- Câu hỏi kinh doanh: Mỗi Category hiện đang được cung cấp bởi bao nhiêu Supplier_ID khác nhau? Ngành hàng nào đang bị phân mảnh nguồn cung quá mức?
select
catagory,
count(distinct Supplier_Name) as total
from grocery_inventory_table
group by catagory
order by total desc;

-- Phân tích xu hướng thời vụ và lịch sử nhập hàng 
-- Câu hỏi kinh doanh: Tính tổng số lượng mã sản phẩm được nhập vào (Date_Received) theo từng tháng của năm 2024. Tháng nào có lượng nhập hàng đột biến nhất?
with monthly_data  as (
select 
*, 
EXTRACT(MONTH FROM date_received) AS month
from grocery_inventory_table
)

select
month,
count(product_name) as total
from monthly_data 
group by month
order by total desc;



