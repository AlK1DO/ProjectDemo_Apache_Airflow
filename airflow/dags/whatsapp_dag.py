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

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# PROJECT PATH CONFIGURATION
# ---------------------------------------------------------------------------

# Project root path inside WSL
PROJECT_ROOT = Path("/mnt/c/Users/AIKIDO/Downloads/tarea").resolve()

# src/ directory
SRC_DIR = PROJECT_ROOT / "src"

# my_proyect package directory
PROJECT_DIR = SRC_DIR / "whatsapp_agent"

# Allow Airflow to import modules from src/
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# ---------------------------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES FROM example.env
# ---------------------------------------------------------------------------

dotenv_path = PROJECT_DIR / "example.env"
load_dotenv(dotenv_path)

# ---------------------------------------------------------------------------
# IMPORT MAIN ASYNC FUNCTION FROM THE BOT
# ---------------------------------------------------------------------------

from my_proyect.__main__ import main  # async function that sends WhatsApp messages

# ---------------------------------------------------------------------------
# ADAPTER TO RUN AN ASYNC FUNCTION INSIDE PYTHONOPERATOR
# ---------------------------------------------------------------------------

def run_async_function():
    """
    Airflow does not support async functions directly.
    This wrapper manually creates an asyncio event loop and runs main().
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    loop.close()

# ---------------------------------------------------------------------------
# DAG DEFINITION
# ---------------------------------------------------------------------------

with DAG(
    dag_id="whatsapp_daily",
    start_date=datetime(2025, 1, 1),       # Minimum start date
    schedule="33 9 * * *",                 # Exact time in cron format
    catchup=False,                         # Do not backfill missed runs
    default_args={"retries": 0},           # No automatic retries
    tags=["whatsapp", "asyncio"],          # UI categories for Airflow
) as dag:

    # -----------------------------------------------------------------------
    # MAIN TASK
    # -----------------------------------------------------------------------
    send_task = PythonOperator(
        task_id="send_whatsapp_message",
        python_callable=run_async_function
    )
