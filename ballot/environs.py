import os
import environ
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, '.var_envs'))
env = environ.Env(
    # set casting, default value
    LOCAL_DB_NAME=(str, ''),
    LOCAL_DB_USER=(str, ''),
    LOCAL_DB_HOST=(str, ''),
    LOCAL_DB_PORT=(str, ''),
    LOCAL_DB_PASSWORD=(str, ''),
    PROJECT_NAME=(str, ''),
    WORKER_CONCURRENCY=(str, ''),
    WORKER_AUTOSCALE=(str, ''),
    WORKER_HOSTNAME=(str, ''),
    WORKER_CRON_QUEUE_NAME=(str, ''),

)

DB_CONFIG_ENVS = {
    'name': env('LOCAL_DB_NAME'),
    'user': env('LOCAL_DB_USER'),
    'host': env('LOCAL_DB_HOST'),
    'port': env('LOCAL_DB_PORT'),
    'password': env('LOCAL_DB_PASSWORD'),
}

WORKER_ENVS = {
    "project_name":env('PROJECT_NAME'),
    "concurency":env('WORKER_CONCURRENCY'),
    "hostname":env('WORKER_HOSTNAME'),
    "worker_cron_queue_name":env('WORKER_CRON_QUEUE_NAME'),

}