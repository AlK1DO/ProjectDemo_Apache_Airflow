# 🚀 Demo Project: Automation with Apache Airflow 
This repository is a practical demonstration of how to use Apache Airflow as a task orchestration platform.
It includes an automated workflow that integrates Airflow with a bot built using Playwright, capable of interacting with WhatsApp Web.

The project runs entirely inside WSL + Ubuntu 22.04, using PDM for environment and dependency management.

# 📌 What is Apache Airflow?
Apache Airflow is a platform used to schedule, build, and monitor workflows.

It allows you to:
- 🕒 Schedule tasks (similar to cron jobs)
- 🔗 Chain tasks with dependencies
- 📊 View execution logs and task status
- 🔄 Automatically retry failed tasks
- 🖥 Access a comprehensive web-based interface


# Requirements
To run this demo project, you need the following environment:
1. Python 3.10:
This version is used for compatibility with Airflow 2.7.2 and to avoid installation issues.
2. Apache Airflow 2.7.2:
A stable version tested together with Playwright and PDM in this environment.
3. WSL + Ubuntu 22.04:
Airflow does not run reliably on native Windows, so it is recommended to use WSL with Ubuntu.
Playwright also requires a Linux environment to properly install browsers.

Note: The project runs entirely within WSL.

📁 Project Structure
```txt
whatsapp_agent/
├── airflow/                ← Internal Airflow configuration
│   ├── dags/
│   │   └── whatsapp_dag.py
│   ├── logs/
│   ├── airflow.cfg
│   └── airflow.db
├── src/
│   └── whatsapp_agent/
│       ├── __main__.py         ← Automated WhatsApp bot (Playwright)
│       └── __init__.py
├── tests/
├── example.env     ← Environment variables for the bot
├── README.md
└── pdm.lock
└── pyproject.toml
```

# Installation and Setup

1. Install WSL + Ubuntu:
This project uses Ubuntu inside WSL to ensure Airflow runs correctly.

1.1 Install WSL on Windows:
Open PowerShell as Administrator and run:
```bash
wsl --install
```

1.2 Install Ubuntu:
From the Microsoft Store, install Ubuntu 22.04.5 LTS.
Open it to start the environment.

2. Prepare the Project in Ubuntu (WSL)
2.1 Navigate to the project directory
``` bash
cd /mnt/c/Users/YOUR_USER/Downloads/tarea
``` 
Replace:
YOUR_USER → your Windows username
project_folder → the folder containing your project

3. Configure PDM (Project-Specific Environment)
3.1 Disable external virtual environments

PDM will manage its own environment:
```bash
pdm config python.use_venv false
```

3.2 Initialize the Project
``` bash
  pdm init
```
Select Python 3.10.

4. Install Dependencies
Install Airflow along with the required dependencies:
```bash
pdm add "apache-airflow==2.7.2" playwright python-dotenv pydantic "pendulum==2.1.2" "Flask-Session==0.4.0" "connexion==2.14.2" https://github.com/AlK1DO/WhatsApp-bot.git --no-self
```
4.1 Install Playwright Browser
```bash
pdm run playwright install chromium
```
4.2 Verify Installation
```bash
pdm run python --version 
pdm run airflow version
```

5. Create the Apache Airflow Structure
```bash
mkdir airflow
cd airflow
mkdir dags
```
Place the file containing your workflow definitions (DAGs) in the dags/ folder,
for example: whatsapp_dag.py.

6. Initialize Airflow
6.1 Create the Database
```bash
pdm run airflow db init
```

6.2 Create an Admin User
```bash
pdm run airflow users create \
  --username admin \
  --password admin \
  --firstname admin \
  --lastname admin \
  --role Admin \
  --email test@example.com

```

7. Run Apache Airflow
7.1 Start the Webserver
```bash
pdm run airflow webserver
```
Open it in your browser:
http://localhost:8080/

7.2 Start the Scheduler (in another terminal)
```bash
cd /mnt/c/Users/TU_USUARIO/Downloads/tarea/airflow
```
```bash
pdm run airflow scheduler
```
8. Activate the DAG
Within the Airflow interface, activate the DAG so it starts running.

9. Configure Timezone (IMPORTANT)

If the WhatsApp DAG does not run at the scheduled time, edit:
airflow/airflow.cfg

Find and change:
default_timezone = America/Lima

You can adjust it according to your region.
Common examples:
- America/Lima
- America/Bogota
- America/Mexico_City
- America/Santiago
- America/Argentina/Buenos_Aires
- Europe/Madrid
- UTC

Airflow uses the IANA timezone database.
Reference: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones