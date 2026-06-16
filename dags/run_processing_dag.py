# Import thư viện cần thiết
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Cấu hình mặc định cho các task trong DAG
default_args = {
    'owner': 'Nguyễn Khắc Hưng',
    'depends_on_past': False,
    'start_date': datetime(2026, 6, 8),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

# DAG chạy file xử lý dữ liệu mỗi 30 phút
dag = DAG(
    'auto_run_processing_script',
    default_args=default_args,
    description='Run data processing pipeline automatically',
    schedule_interval='*/30 * * * *',
    catchup=False,
    max_active_runs=1
)

# Thực thi script xử lý dữ liệu
run_script_task = BashOperator(
    task_id='execute_python_script',
    bash_command='python /opt/airflow/dags/scripts/data_processing.py',
    dag=dag,
)

# Thiết lập workflow
run_script_task