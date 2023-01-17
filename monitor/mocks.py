from monitor.models import CeleryTask, CeleryWorker
from django.utils import timezone
from uuid import uuid4
from time import sleep


def _get_sample_celery_task_data(name=None, uuid=None, status=None,
                                 args=None, result=None, started=None,
                                 received=None, retries=None, exception=None,
                                 worker=None, root_id=None, parent_id=None,
                                 succeeded=None, runtime=None, traceback=None,
                                 queue=None, children=None, published=None):
    sleep(0.05)
    data = {
        "name": "operation.tasks.function" if name is None else name,
        "uuid": str(uuid4()) if uuid is None else uuid,
        "args": "this is a test argument" if args is None else args,
        "kwargs": "" if args is None else args,
        "result": "" if result is None else result,
        "received": timezone.now() if received is None else received,
        "started": timezone.now() if started is None else started,
        "succeeded": timezone.now() if succeeded is None else succeeded,
        "retries": 0 if retries is None else retries,
        "runtime": 1.14053136 if runtime is None else runtime,
        "exception": "no exception" if exception is None else exception,
        "traceback": "no error" if traceback is None else traceback,
        "worker": "woker_1" if worker is None else worker,
        "root_id": str(uuid4()) if root_id is None else root_id,
        "parent_id": str(uuid4()) if parent_id is None else parent_id,
        "queue": "test_queue" if queue is None else queue,
        "children": f'[{str(uuid4())}, {str(uuid4())}]' if children is None else children
    }
    if status is not None:
        data["status"] = status
    if published is not None:
        data["published"] = published
    return data


def get_sample_celery_task_data(name=None, uuid=None, status=None,
                                args=None, result=None, started=None,
                                received=None, retries=None, exception=None,
                                worker=None, root_id=None, parent_id=None,
                                succeeded=None, runtime=None, traceback=None,
                                queue=None, children=None, published=None):
    data = _get_sample_celery_task_data(name=name, uuid=uuid, status=status,
                                        args=args, result=result, started=started,
                                        received=received, retries=retries, exception=exception,
                                        worker=worker, root_id=root_id, parent_id=parent_id,
                                        succeeded=succeeded, runtime=runtime, traceback=traceback,
                                        queue=queue, children=children, published=published)
    return data


def get_sample_celery_task_model(name=None, uuid=None, status=None,
                                 args=None, result=None, started=None,
                                 received=None, retries=None, exception=None,
                                 worker=None, root_id=None, parent_id=None,
                                 succeeded=None, runtime=None, traceback=None,
                                 queue=None, children=None, published=None):

    data = _get_sample_celery_task_data(name=name, uuid=uuid, status=status,
                                        args=args, result=result, started=started,
                                        received=received, retries=retries, exception=exception,
                                        worker=worker, root_id=root_id, parent_id=parent_id,
                                        succeeded=succeeded, runtime=runtime, traceback=traceback,
                                        queue=queue, children=children, published=published)
    return CeleryTask.objects.create(**data)


def _get_sample_celery_worker_data(name=None, status=None, active=None, processed=None):
    data = {
        "name": f'celery@{str(uuid4())[:8]}' if name is None else name,
        "status": 0 if status is None else status,
    }
    if active is not None:
        data["active"] = active
    if processed is not None:
        data["processed"] = processed
    return data


def get_sample_celery_worker_model(name=None, status=None, active=None, processed=None):
    data = _get_sample_celery_worker_data(
        name=name, status=status, active=active, processed=processed)
    return CeleryWorker.objects.create(**data)


def get_sample_celery_worker_data(name=None, status=None, active=None, processed=None):
    data = _get_sample_celery_worker_data(
        name=name, status=status, active=active, processed=processed)
    return data
