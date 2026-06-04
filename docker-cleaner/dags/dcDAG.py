from datetime import datetime, timedelta
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
import logging
log = logging.getLogger(__name__)

def run_pipeline():
    from datacleaner import (
        fileLoader, naCheckCust, naCheckTran,
        dateCheckTran, dataEnrich, crossCheck, addToSQL
    )
    T_path = "/opt/airflow/InputFiles/03_Library Systembook.csv"
    C_path = "/opt/airflow/InputFiles/03_Library SystemCustomers.csv"

    Transactions, Customers, Error_Transactions, Error_Customers = fileLoader(T_path, C_path)
    Customers, Error_Customers = naCheckCust(Customers, Error_Customers)
    Transactions, Error_Transactions = naCheckTran(Transactions, Error_Transactions)
    Transactions, Error_Transactions = dateCheckTran(Transactions, Error_Transactions)
    Transactions = dataEnrich(Transactions)
    Transactions, Customers, Error_Transactions, Error_Customers = crossCheck(
        Customers, Error_Customers, Transactions, Error_Transactions
    )
    addToSQL(Customers, Error_Customers, Transactions, Error_Transactions)

def on_failure(context):
    log.error("Pipeline failed on run: %s", context['run_id'])

def on_success(context):
    print("Pipeline ran successfully on run: ", context['run_id'])

def my_alert_function(dag, task_list, blocking_task_list, slas, blocking_tis):
    print(f"SLA missed for tasks: {task_list}")

with DAG(
    dag_id="lib_pipeline",
    start_date=datetime(2026,6,3,12,0,0),
    schedule="*/20 * * * *",
    catchup=False,
    sla_miss_callback=my_alert_function, 
) as dag:
    task = PythonOperator(
        task_id="run_pipeline",
        python_callable=run_pipeline,
        on_failure_callback=on_failure,
        sla=timedelta(minutes=5),
        on_success_callback=on_success,
    )