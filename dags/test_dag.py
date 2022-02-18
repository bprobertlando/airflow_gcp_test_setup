import time
from datetime import datetime, date, timedelta
import pandas as pd
import json
import re
import os
import glob
import airflow
import logging

from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.models import DAG, Variable, DagRun
from airflow.operators.dummy_operator import DummyOperator

print("\n\nSTART DAG\n\n")

args = {
    'owner': 'airflow',
    # 'start_date': datetime(2021,2,2),
    'email': [],
    'email_on_failure': False,
    'email_on_retry': False,
}

# Instantiate a DAG object
dag = DAG(
    dag_id='basic_dag',
    default_args=args,
    start_date = datetime(2021,6,5)
)

METADATA = {
    'DAG_ID':'{{dag.dag_id}}',
    'RUN_ID':'{{run_id}}',
    'PREV_EXEC_DATE_SUCCESS': '{{prev_execution_date_success}}'
    }




##### Tasks #####

start = DummyOperator(task_id="start", dag=dag)

basic = KubernetesPodOperator(
        # The ID specified for the task.
        task_id='basic',
        # Name of task you want to run, used to generate Pod ID.
        name='basic',
        # Entrypoint of the container, if not specified the Docker container's
        # entrypoint is used. The cmds parameter is templated.
        cmds=['echo'],
        # The namespace to run within Kubernetes, default namespace is
        # `default`. There is the potential for the resource starvation of
        # Airflow workers and scheduler within the Cloud Composer environment,
        # the recommended solution is to increase the amount of nodes in order
        # to satisfy the computing requirements. Alternatively, launching pods
        # into a custom namespace will stop fighting over resources.
        namespace='default',
        # Docker image specified. Defaults to hub.docker.com, but any fully
        # qualified URLs will point to a custom repository. Supports private
        # gcr.io images if the Composer Environment is under the same
        # project-id as the gcr.io images and the service account that Composer
        # uses has permission to access the Google Container Registry
        # (the default service account has permission)
        image='gcr.io/gcp-runtimes/ubuntu_18_0_4',
        dag = dag,
        get_logs = True
)

end = DummyOperator(task_id="end", dag=dag)


## Define task dependencies

start >> basic >> end
