# standard imports
import logging
import tempfile

# external imports
from celery import current_app as current_celery_app
from celery.result import AsyncResult
from confini import Config

# local imports
from .celery_config import settings

logg = logging.getLogger()


def create_celery_app(config: Config):
    celery_app = current_celery_app
    celery_app.config_from_object(settings)

    # handle dev env configs
    broker_url = config.get('CELERY_BROKER_URL')
    if broker_url[:4] == "file":
        broker_queue = tempfile.mkdtemp()
        broker_processed = tempfile.mkdtemp()
        celery_app.conf.update({
            'broker_transport_options': {
                'broker_url': broker_url,
                'data_folder_in': broker_queue,
                'data_folder_out': broker_queue,
                'data_folder_processed': broker_processed
            },
        })
        logg.warning(
            f'celery broker dirs queue i/o {broker_queue} processed {broker_processed}, will NOT be deleted on shutdown')
    else:
        celery_app.conf.update({'broker_url': broker_url})

    result_backend = config.get('CELERY_RESULT_URL')
    if result_backend[:4] == "file":
        result_queue = tempfile.mkdtemp()
        celery_app.conf.update({'result_backend': f'file://{result_queue}'})
        logg.warning(f'celery backend store dir {result_queue} created, will NOT be deleted on shutdown')
    else:
        celery_app.conf.update({'result_backend': result_backend})

    celery_app.conf.update(task_track_started=True)
    celery_app.conf.update(task_serializer='pickle')
    celery_app.conf.update(result_serializer='pickle')
    celery_app.conf.update(accept_content=['pickle', 'json'])
    celery_app.conf.update(result_persistent=True)
    celery_app.conf.update(worker_send_task_events=False)
    celery_app.conf.update(worker_prefetch_multiplier=1)

    return celery_app


def get_task_info(task_id):
    """
    return task info for the given task_id
    """
    task_result = AsyncResult(task_id)
    return {"task_id": task_id, "task_status": task_result.status, "task_result": task_result.result}
