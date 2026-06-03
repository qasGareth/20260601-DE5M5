from datetime import datetime
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator

def hello():
    print("Hello")

with DAG(
    dag_id="hello",
    start_date=datetime(2026,6,3,12,0,0),
    schedule="* * * * *",
    catchup=False, 
) as dag:
    task = PythonOperator(
        task_id="hello",
        python_callable=hello
    )