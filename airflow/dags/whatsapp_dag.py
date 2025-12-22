"""
whatsapp_dag.py
Apache Airflow DAG to run a WhatsApp Web message-sending bot
using Playwright and an asynchronous Python script.

This DAG:
- Loads variables from .env
- Executes an async function via PythonOperator
- Schedules execution using cron
- Maintains a simple one-task workflow
"""

from asyncio import new_event_loop, set_event_loop
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from workflows.sample_taks import taks


def run_async_function():
    """
    Airflow cannot run async functions directly.
    Therefore, we manually create an event loop.
    """
    loop = new_event_loop()
    set_event_loop(loop)
    loop.run_until_complete(taks())
    loop.close()

with DAG(
    dag_id="whatsapp_daily",
    start_date=datetime(2025, 1, 1),
    schedule="33 9 * * *",
    catchup=False,
    default_args={"retries": 0},
    tags=["whatsapp", "asyncio"],
) as dag:

    send_task = PythonOperator(
        task_id="send_whatsapp_message",
        python_callable=run_async_function
    )
