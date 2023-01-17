from threading import Thread
from logging import getLogger
from celery import Celery
from uuid import UUID
from django.core.management.base import BaseCommand
from monitor.models import CeleryTask, CeleryWorker
from django.conf import settings
from time import sleep
from celery.result import AsyncResult
from _thread import start_new_thread
from monitor.utils import sync_status_task, timestamp_to_datatime
from django.conf import settings

logger = getLogger("monitor")


def _destroy_worker():
    try:
        CeleryWorker.objects.all().delete()
        logger.warning("destroy db worker")
    except Exception as exp:
        logger.error(exp)
        exit(3)


def update_db(data, worker=True):
    sleep(0.05)
    try:
        if worker:
            object, created = CeleryWorker.objects.get_or_create(
                name=data.get("name"))
        else:
            object, created = CeleryTask.objects.get_or_create(
                uuid=data.get("uuid"))
        object.__dict__.update(**data)
        object.save()
    except Exception as exp:
        logger.error(f'during exception with message: : {exp} , data:{data}')
        pass


class MonitorThread(Thread):
    def __init__(self, celery_app):
        Thread.__init__(self)
        self.celery_app = celery_app
        self.state = self.celery_app.events.State()

    def worker_heartbeat(self, event):
        self.state.event(event)
        data = {
            "name": event.get("hostname"),
            "status": 1,
            "active": event.get("active"),
            "processed": event.get("processed"),
        }
        update_db(data)

    def worker_online(self, event):
        self.state.event(event)
        data = {
            "name": event.get("hostname"),
            "status": 1
        }
        update_db(data)
        logger.info(f'worker_online:{event}')

    def worker_offline(self, event):
        self.state.event(event)
        data = {
            "name": event.get("hostname"),
            "status": 0
        }
        update_db(data)
        logger.info(f'worker_offline:{event}')

    def task_received(self, event):
        self.state.event(event)
        data = {
            "uuid": event.get("uuid"),
            "name": event.get("name"),
            "args": event.get("args"),
            "kwargs": event.get("kwargs"),
            "retries": event.get("retries"),
            "worker": event.get("hostname"),
            "status": event.get("state"),
            "root_id": event.get("root_id"),
            "received": timestamp_to_datatime(event.get("local_received")),
        }
        if event.get("parent_id") is not None:
            data['parent_id'] = UUID(event.get("parent_id"))
        update_db(data, 0)
        logger.info(data)

    def task_started(self, event):
        self.state.event(event)
        data = {
            "uuid": event.get("uuid"),
            "worker": event.get("hostname"),
            "started": timestamp_to_datatime(event.get("local_received")),
            "status": event.get("state"),
        }
        update_db(data, 0)
        logger.info(data)

    def task_succeeded(self, event):
        try:
            self.state.event(event)
            sleep(0.05)
            params = AsyncResult(event.get("uuid"))._get_task_meta()
            data = {
                "uuid": event.get("uuid"),
                "status": event.get("state"),
                "result": event.get("result"),
                "runtime": event.get("runtime"),
                "worker": event.get("hostname"),
                "succeeded": timestamp_to_datatime(event.get("local_received")),
            }
            if params.get("args", None):
                data["args"] = params.get("args")
            if params.get("queue", None):
                data["queue"] = params.get("queue")
            if params.get("children", None):
                data["children"] = [obj.id for obj in params.get("children")]
            start_new_thread(update_db, (data, 0,))
            logger.info(data)
        except TypeError as exp:
            logger.error(
                f"terminate program with exception : {exp}| data:{data} | event:{event}")
            start_new_thread(update_db, (data, 0,))
            logger.warning(
                f'task id: {data["uuid"]} not included argument... but saved ')
        except Exception as exp:
            logger.error(f"terminate program with exception : {exp}")
            logger.error(f"Trying again in 10.00 seconds...")
            sleep(10)
            pass

    def task_failed(self, event):
        self.state.event(event)
        data = {
            "uuid": event.get("uuid"),
            "status": event.get("state"),
            "exception": event.get("exception"),
            "traceback": event.get("traceback"),
            "worker": event.get("hostname")
        }
        logger.info(data)
        update_db(data, 0)

    def task_revoked(self, event):
        self.state.event(event)
        data = {
            "uuid": event.get("uuid"),
            "status": event.get("state"),
        }
        logger.info(data)
        update_db(data, 0)

    def task_retried(self, event):
        self.state.event(event)
        data = {
            "uuid": event.get("uuid"),
            "status": event.get("state"),
            "exception": event.get("exception"),
            "traceback": event.get("traceback"),
            "worker": event.get("hostname")
        }
        logger.info(data)
        update_db(data, 0)

    def run(self):
        while True:
            try:
                with self.celery_app.connection() as connection:
                    recv = self.celery_app.events.Receiver(connection, handlers={
                        'worker-heartbeat': self.worker_heartbeat,
                        'worker-online': self.worker_online,
                        'worker-offline': self.worker_offline,
                        'task-received': self.task_received,
                        'task-started': self.task_started,
                        'task-succeeded': self.task_succeeded,
                        'task-failed': self.task_failed,
                        'task-revoked': self.task_revoked,
                        'task-retried': self.task_retried
                    })
                    recv.capture(limit=None, timeout=None, wakeup=True)

            except (KeyboardInterrupt, SystemExit) as exp:
                logger.error(f"terminate program with exception : {exp}")
                exit(1)
            except Exception as exp:
                logger.error(f"terminate program with exception : {exp}")
                logger.error(f"Trying again in 10.00 seconds...")
                sleep(10)
                pass


class SyncThread(Thread):
    def run(self) -> None:
        logger.info('starting synchronize ...')
        while True:
            try:
                synchronize = sync_status_task(CeleryTask)
                logger.info(f'{synchronize} numbers were synchronized.')
                sleep(3600)
            except Exception as exp:
                logger.error(f'during exception with message: {exp}')
                pass


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            logger.info("test")
            _destroy_worker()
            app = Celery(broker=settings.CELERY_BROKER_URL)
            thread1 = MonitorThread(celery_app=app)
            thread1.start()
            thread2 = SyncThread()
            thread2.start()

        except Exception as exp:
            logger.error(f"terminate program with exception : {exp}")
            logger.error(f"Trying again in 10.00 seconds...")
            sleep(10)
            pass
