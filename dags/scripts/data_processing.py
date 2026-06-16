
"""
Data Analyst: Nguyễn Khắc Hưng
Ngày: 9-6-2026
Khoa: Công Nghệ Thông Tin
Nghành: Khoa Học Dữ Liệu
Chuyên Nghành: Phân Tích Dữ Liệu Trong Kinh Tế Và Tài Chính
"""

# NHẬP CÁC THƯ VIỆN 
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text, inspect
import os 
from sklearn.impute import KNNImputer

# ĐỊNH NGHĨA CÁC BIẾN CẤU HÌNH 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(os.path.join(os.path.join(BASE_DIR, 'data'), 'raw'), 'Grocery_Inventory.csv')
ENGINE = create_engine("")

# ĐỊNH NGHĨA HÀM EXTRACT
def extract(data_dir):
    """extract là hàm dùng để trích xuất dữ liệu từ các nguồn ban đầu như .csv, .json"""

    # trích xuất dữ liệu từ file .csv
    df = pd.read_csv(data_dir)

    return df

# ĐỊNH NGHĨA HÀM TRANSFORM
def transform(df, null_by_columns):
    """transform là hàm dùng để xử lý và làm sạch dữ liệu trước khi tiến hành phân tích:
    1. xử lý các cột bị giá trị null theo logic
        + Nếu tổng số null <= 5% thì tiến hành xóa các giả trị null
        + nếu tổng số null > 5% thì tiến hành xử lý các giá tri null:
            - nếu là cột có kiểu dữ liệu object thì tiến hành xử lý bằng cách điền giá trị phổ biến nhất
            - nếu là cột có kiểu dữ liệu number thì tiến hành xử lý bằng KNNImputer
    2. Xử lý các giá trị duplicated bằng cách xóa đi các giá trị trùng lặp chỉ dữ lại 1 giá trị đầu tiên
    3. Chuyển đổi kiểu dữ liệu ngày từ dạng string sang dạng chuẩn hóa datetimes
    4. chuẩn hóa tên cột về chữ thường để khớp với tabel trong database"""
    
    # chuyển null_by_columns(tổng giá trị null theo từng cột) từ dạng pandas series về dạng dataframe và đổi tên cột để dễ thao tác
    df_null_by_columns = null_by_columns.reset_index()
    df_null_by_columns.rename(columns={"index": "columns",0: "total null"}, 
                      inplace=True)
    
    # Tạo một ngưỡng dùng để phân biệt trường hợp xóa null trường hợp xử lý fillna
    threshold = len(df) * 0.05

    # lọc ra những cột có giá trị null và tổng số null nhỏ hơn 5% 
    remove_null = df_null_by_columns[(df_null_by_columns['total null'] < threshold) & (df_null_by_columns['total null'] != 0)]

    # lọc ra những cột có giá trị null và tổng số null lớn hơn 5%
    replace_null = df_null_by_columns[(df_null_by_columns['total null'] > threshold) & (df_null_by_columns['total null'] != 0)]
    
    # Đối với những cột có giá trị null < 5% tiến hành xóa các giá trị null đó đi
    df = df.dropna(subset = remove_null['columns'])

    # Đối với những cột có giá trị null > 5% tiến hành xử lý null bằng cách fillna
    imputer = KNNImputer(n_neighbors=10) # khởi tạo 1 bộ điền giá trị thiếu KNNImputer với n_neighbors = 10 nghĩa là lấy 10 giá trị gần nhất để chạy và tính toán

    object_columns = df[replace_null['columns']].select_dtypes(include='object').columns.tolist() # Lọc ra những cột có kiểu dữ liệu và object
    if(len(object_columns) != 0):
        df[object_columns] = df[object_columns].fillna(df[object_columns].mode().iloc[0]) # xử lý bằng cách điền vào giá trị phổ biến nhất

    numeric_columns = df[replace_null['columns']].select_dtypes(include='number').columns.tolist() # lọc ra những cột có kiểu dữ liệu numeric
    if(len(numeric_columns) != 0):
        df[numeric_columns] = imputer.fit_transform(df[numeric_columns]) # xử lý bằng cách chạy bộ điền KNNimputer để tìm giá giá trị gần nhất trong 10 giá trị sung quanh
    
    # Xử lý các giá trị trùng lặp 
    df = df.drop_duplicates(keep='first')

    # Chuyển đổi kiểu dữ liệu của các cột ngày tháng năm từ string sang dạng chuẩn datetimes
    date_columns = ['Date_Received','Last_Order_Date','Expiration_Date']
    for i in range(len(date_columns)):
        df[date_columns[i]] = pd.to_datetime(df[date_columns[i]], errors='coerce')
    
    # Chuẩn hóa tên cột về chữ thường để khớp với database
    df.columns = df.columns.str.lower()

    return df

# ĐỊNH NGHĨA HÀM LOAD
def load(engine, df):
    """load là hàm dùng để nạp dữ liệu vào database sau khi quy trình xử lý dữ liệu đã song"""
    table_name = 'grocery_inventory_table' # Tên bảng đã tạo trong database
    inspector = inspect(engine)
    
    if inspector.has_table(table_name):
        with engine.begin() as conn:
            conn.execute(text(f"TRUNCATE TABLE {table_name};"))

    # Nạp dữ liệu vào database thông qua thư viện pandas
    df.to_sql(
        table_name,
        engine, # engine là đường dẫn kết nối với database đã khởi tạo trong postgres
        if_exists="append", # khai báo phương thức append để thêm dữ liệu vào tiếp không thêm lại từ đầu
        index=False # không ghi cột index của dataframe vào 
    )

# ĐỊNH NGHĨA HÀM DATA_INFO
def data_info(df):
    """data_info là hàm dùng để trả về những thông tin cơ bản và tổng quát của dữ liệu như 5 dòng đầu, 5 dòng cuối, 
    thống kê của các cột numeric, thống kê của các cột object"""

    head = df.head()
    tail = df.tail()
    try:
        describe_object = df.describe(include="object")
    except:
        print('---------------------------------')
        print('Không có cột dữ liệu kiểu string')
        print('---------------------------------')
        describe_object = None
    try:
        describe_numeric = df.describe(include='number')
    except:
        print('---------------------------------')
        print('không có cột dữ liệu kiểu numeric')
        print('---------------------------------')
        describe_numeric = None
    return head, tail, describe_object, describe_numeric

# ĐỊNH NGHĨA HÀM PRINT_DATA_INFO
def print_data_info(head, tail, describe_object, describe_numeric):
    """print_data_info là hàm dùng để in ra màn hình những thông tin cơ bản và tổng quát của dữ liêu như 5 dòng đầu, 5 dòng cuối, 
    thống kê của các cột numeric, thống kê của các cột object phục vụ cho quá trình theo dõi và xử lý lỗi"""

    print('---------------------------------')
    print('5 DÒNG ĐẦU TIÊN CỦA TẬP DỮ LIỆU')
    print('---------------------------------' + '\n')
    print(head)
    print('---------------------------------')
    print('5 DÒNG CUỐI CÙNG CỦA TẬP DỮ LIỆU')
    print('---------------------------------' + '\n')
    print(tail)
    print('---------------------------------')
    print('THÔNG TIN TỔNG QUÁT CỦA TẬP DỮ LIỆU')
    print('---------------------------------' + '\n')
    df.info()
    print('---------------------------------')
    print('THỐNG KÊ CÁC CỘT OBJECT CỦA TẬP DỮ LIỆU')
    print('---------------------------------' + '\n')
    print(describe_object)
    print('---------------------------------')
    print('THỐNG KÊ CÁC CỘT NUMERIC CỦA TẬP DỮ LIỆU')
    print('---------------------------------' + '\n')
    print(describe_numeric)

# ĐỊNH NGHĨA HÀM CHECK_DATA_QUANLITY
def check_data_quanlity(df):
    """check_data_quanlity là hàm dùng để kiểm tra những lỗi mà dữ liệu đang lặp phải như các giá trị missing, các giá trị duplicated, các giá trị
    outlier, các cột sai kiểu dữ liệu"""

    null_column = df.columns[df.isnull().any(axis=0)].tolist() # láy ra tên những cột có giá trị null
    null_by_columns = df.isnull().sum() # lấy ra tổng số giá trị null theo từng cột
    duplicate = df.duplicated().sum()   # lấy ra tông số giá trị trùng lặp
    return null_column, null_by_columns, duplicate

# ĐỊNH NGHĨA HÀM PRINT_DATA_QUANLITY_ISSUES
def print_data_quanlity_issues(null_by_columns, duplicate):
    """print_data_quanlity_issues là hàm dùng để in ra màn hình những lỗi mà dữ liệu đang gặp phải như missing, duplicated, outlier, sai kiểu dữ liệu
    nhằm phục vụ cho việc xử lý dữ liệu với bước transform"""

    print('---------------------------------')
    print('TỔNG SỐ NULL THEO TỪNG CỘT CỦA TẬP DỮ LIỆU')
    print('---------------------------------' + '\n')
    print(null_by_columns)
    print('---------------------------------')
    print('TỔNG SỐ GIÁ TRỊ TRÙNG LẶP TRONG TẬP DỮ LIỆU')
    print('---------------------------------' + '\n')
    print(duplicate)

# LUỒNG HOẠT ĐỘNG CHÍNH CỦA ETL
if __name__ == "__main__":

    # Trích xuất dữ liệu từ file CSV
    df = extract(DATA_DIR)

    # Thu thập thông tin tổng quan của bộ dữ liệu:
    # - 5 dòng đầu
    # - 5 dòng cuối
    # - Thống kê các cột object
    # - Thống kê các cột numeric
    head, tail, describe_object, describe_numeric = data_info(df)

    # Hiển thị thông tin tổng quan của dữ liệu
    # print_data_info(head, tail, describe_object, describe_numeric)

    # Thu thập thông tin lỗi của bộ dữ liệu:
    # - các giá trị thiếu
    # - các giá trị trùng lặp
    null_column, null_by_columns, duplicate = check_data_quanlity(df)

    # Hiện thị thông tin lỗi của dữ liệu 
    # print_data_quanlity_issues(null_by_columns, duplicate)

    # Làm sạch và tiền xử lý dữ liệu
    df_processed = transform(df, null_by_columns)

    # Kiểm tra lại cấu trúc dữ liệu sau khi xử lý
    df_processed.info()

     # Nạp dữ liệu đã xử lý vào PostgreSQL
    load(ENGINE, df_processed)



    