from logging import getLogger
from django.db.models import ProtectedError
from rest_framework import serializers
from monitor.exceptions import InternalError
from monitor.models import CeleryTask, CeleryWorker
from monitor.utils import sync_status_task
from distutils.util import strtobool
from django.db.utils import DatabaseError
from django.conf import settings
instance_app = __import__(settings.ROOT_URLCONF.split(
    ".")[0]+".celery", globals(), locals(), ['app'], 0)
celery_app = instance_app.app

logger = getLogger("monitor")


class CeleryTaskCreateRequest(serializers.ModelSerializer):

    class Meta:
        model = CeleryTask
        fields = ['id', 'name', 'uuid', 'status', 'args',
                  'kwargs', 'result', 'received', 'started', 'succeeded',
                  'retries', 'runtime', 'exception', 'traceback', 'worker',
                  'root_id', 'parent_id', 'children', 'queue', 'published']


class CeleryTaskCreateResponse(serializers.ModelSerializer):
    class Meta:
        model = CeleryTask
        fields = ['id', 'name', 'uuid', 'status', 'args', 'kwargs', 'result',
                  'received', 'started', 'succeeded', 'retries', 'runtime', 'exception', 'traceback',
                  'worker', 'root_id', 'parent_id', 'queue', 'children', 'queue', 'published']


class CeleryTaskListResponse(CeleryTaskCreateResponse):
    class Meta(CeleryTaskCreateResponse.Meta):
        pass


class CeleryTaskRetrieveResponse(CeleryTaskCreateResponse):

    def __init__(self, instance=None, data=..., *args, **kwargs):
        sync = kwargs.pop("sync", 'False')
        if sync[0].capitalize() in ("True", '1'):
            sync_status_task(instance, unic=True)
        return super(CeleryTaskRetrieveResponse, self).__init__(instance=instance)

    class Meta(CeleryTaskCreateResponse.Meta):
        pass


class CeleryTaskUpdateRequest(CeleryTaskCreateResponse):
    class Meta(CeleryTaskCreateResponse.Meta):
        pass


class CeleryTaskUpdateResponse(CeleryTaskCreateResponse):
    class Meta(CeleryTaskCreateResponse.Meta):
        pass


class CeleryTaskRevokeRequest(serializers.Serializer):
    ides = serializers.ListField(child=serializers.UUIDField())

    class Meta:
        fields = ['ides']

    def revoke_task(self):
        try:
            celery_app.control.revoke(self.validated_data.get(
                'ides'), terminate=True, signal='SIGKILL')
        except Exception as exp:
            logger.error(f'revoke |  Error occured during: {exp}')
            raise InternalError("revoked failed!!")


class CeleryTaskRevokeResponse(CeleryTaskRevokeRequest):
    class Meta(CeleryTaskRevokeRequest):
        pass

    def list_revoked_tasks():
        return {"list_revokes": celery_app.control.inspect().revoked()}


class CeleryTaskSyncResponse(serializers.Serializer):

    def sync(instance):

        syncronize = sync_status_task(instance)
        return syncronize


class CeleryTaskDashboardResponse(serializers.Serializer):

    @property
    def get_status(self):
        try:
            total_worker = {}
            total_task = {}
            data = {}
            num_active = 0
            num_processed = 0
            for worker in CeleryWorker.objects.all():
                num_active += worker.active
                num_processed += worker.processed
            total_worker["worker_online"] = CeleryWorker.objects.filter(
                status__in=[strtobool("True")]).count()
            total_worker["worker_offline"] = CeleryWorker.objects.filter(
                status__in=[strtobool("False")]).count()
            total_worker["worker_task_active"] = num_active
            total_worker["worker_task_processed"] = num_processed
            total_task["task_pending"] = CeleryTask.objects.filter(
                status="PENDING").count()
            total_task["task_received"] = CeleryTask.objects.filter(
                status="RECEIVED").count()
            total_task["task_started"] = CeleryTask.objects.filter(
                status="STARTED").count()
            total_task["task_success"] = CeleryTask.objects.filter(
                status="SUCCESS").count()
            total_task["task_failed"] = CeleryTask.objects.filter(
                status="FAILED").count()
            total_task["task_revoked"] = CeleryTask.objects.filter(
                status="REVOKED").count()
            total_task["task_retried"] = CeleryTask.objects.filter(
                status="RETRY").count()
            data["worker"] = total_worker
            data["task"] = total_task
            return data
        except DatabaseError as exp:
            logger.error(f'monitor dashboard | Error occured during: {exp}')
            raise InternalError("Error establishing a database connection")
        except Exception as exp:
            logger.error(f'monitor dashboard | Error occured during: {exp}')
            raise InternalError("Error establishing a database connection")


class CeleryWorkerCreateRequest(serializers.ModelSerializer):
    class Meta:
        model = CeleryWorker
        fields = ['id', 'name',  'status']


class CeleryWorkerCreateResponse(serializers.ModelSerializer):
    class Meta:
        model = CeleryWorker
        fields = ['id', 'name',  'status',
                  'active', 'processed', 'last_modified']


class CeleryWorkerListResponse(CeleryWorkerCreateResponse):
    class Meta(CeleryWorkerCreateResponse.Meta):
        pass


class CeleryWorkerRetrieveResponse(CeleryWorkerCreateResponse):
    class Meta(CeleryWorkerCreateResponse.Meta):
        pass


class CeleryWorkerUpdateRequest(CeleryWorkerCreateRequest):
    class Meta(CeleryWorkerCreateRequest.Meta):
        pass


class CeleryWorkerUpdateResponse(CeleryWorkerCreateResponse):
    class Meta(CeleryWorkerCreateResponse.Meta):
        pass


class CeleryWorkerRefreshResponse(CeleryWorkerListResponse):
    class Meta(CeleryWorkerListResponse.Meta):
        pass

    def clean_db_worker():
        try:
            CeleryWorker.objects.all().delete()
        except ProtectedError:
            raise InternalError(
                "refresh failed , This object can't be deleted!!")


class CeleryWorkerShutdownRequest(serializers.Serializer):
    names = serializers.ListField(child=serializers.CharField())

    class Meta():
        fields = ['names']

    def shutdown_worker(self):
        try:
            celery_app.control.shutdown(
                destination=self.validated_data.get('names'))
            stat = celery_app.control.inspect(
                destination=self.validated_data.get('names')).ping()
            status = {}
            for name in self.validated_data.get('names'):
                try:
                    status[name] = stat[name]
                except TypeError:
                    status[name] = 'shutdown'
            return {'names': [status]}
        except ProtectedError:
            raise InternalError("shutdown failed.")
        except Exception as exp:
            raise InternalError("shutdown failed.")


class CeleryWorkerShutdownResponse(CeleryWorkerShutdownRequest):
    class Meta(CeleryWorkerShutdownRequest.Meta):
        pass
