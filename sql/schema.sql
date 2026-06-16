
-- Tạo database
create database airflow;

-- Tạo table
create table grocery_inventory_table(
    Product_Name VARCHAR(50) not null,
    Catagory VARCHAR(50) not null,
    Supplier_Name VARCHAR(50) not null,
    Warehouse_Location VARCHAR(50) not null,
    Status_ VARCHAR(20) not null,
    Product_ID VARCHAR(30) not null,
    Supplier_ID VARCHAR(30) not null,
    Date_Received TIMESTAMP not null,
    Last_Order_Date TIMESTAMP not null,
    Expiration_Date TIMESTAMP not null
);

-- Kiểm tra dữ liệu và bảng
select * from grocery_inventory_table;



