from monitor.core.base_viewset import BaseViewSet
from monitor.core.base_viewset import BaseViewSet
from monitor import serializers as ser
from monitor.filters import (CeleryTaskStatusFilterBackend, CeleryTaskUUIDFilterBackend,
                             CeleryWorkerNameFilterBackend, CeleryWorkerStatusFilterBackend,
                             CeleryTaskParentIdFilterBackend, CeleryTaskPublishedFilterBackend,
                             CeleryTaskQueueFilterBackend)
from monitor.models import CeleryTask, CeleryWorker
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_205_RESET_CONTENT
from rest_framework.permissions import AllowAny


class CeleryTaskViewSet(BaseViewSet):
    queryset = CeleryTask.objects.all()
    serializer_action_classes = {
        'create': {
            'req': ser.CeleryTaskCreateRequest,
            'res': ser.CeleryTaskCreateResponse,
        },
        'update': {
            'req': ser.CeleryTaskUpdateRequest,
            'res': ser.CeleryTaskUpdateResponse
        },
        'partial_update': {
            'req': ser.CeleryTaskUpdateRequest,
            'res': ser.CeleryTaskUpdateResponse
        },
        'retrieve': {
            'res': ser.CeleryTaskRetrieveResponse
        },
        'list': {
            'res': ser.CeleryTaskListResponse,
        },
        'revoke': {
            'req': ser.CeleryTaskRevokeRequest,
            'res': ser.CeleryTaskRevokeResponse,
        },
        'sync': {
            'res': ser.CeleryTaskSyncResponse,
        },
        'dashboard': {
            'res': ser.CeleryTaskDashboardResponse,
        },
    }
    permission_action_classes = {
        'create': [AllowAny, ],
        'update': [AllowAny, ],
        'partial_update': [AllowAny, ],
        'retrieve': [AllowAny, ],
        'list': [AllowAny, ],
        'destroy': [AllowAny, ],
        'revoke': [AllowAny, ],
        'sync': [AllowAny, ],
    }
    filter_backends = [CeleryTaskUUIDFilterBackend, CeleryTaskStatusFilterBackend,
                       CeleryTaskParentIdFilterBackend, CeleryTaskPublishedFilterBackend,
                       CeleryTaskQueueFilterBackend]

    @action(detail=False, methods=['POST'],
            url_name='revoke', url_path='revoke')
    def revoke(self, request, *args, **kwargs):
        reqser = self.get_serializer(data=request.data)
        reqser.is_valid(raise_exception=True)
        reqser.revoke_task()
        resser = self.get_serializer_response()
        list_revokes = resser.list_revoked_tasks()
        return Response(data=list_revokes)

    @action(detail=False, methods=['GET'],
            url_name='sync', url_path='sync')
    def sync(self, request, *args, **kwargs):
        resser = self.get_serializer_response()
        num_sync = resser.sync(self.queryset.model)
        return Response(data=f'{num_sync} numbers were synchronized.')

    @action(detail=False, methods=['GET'],
            url_name='dashboard', url_path='dashboard')
    def dashboard(self, request, *args, **kwargs):
        resser = self.get_serializer_response()()
        data = resser.get_status
        return Response(data=data)


class CeleryWorkerViewSet(BaseViewSet):
    queryset = CeleryWorker.objects.all()
    serializer_action_classes = {
        'create': {
            'req': ser.CeleryWorkerCreateRequest,
            'res': ser.CeleryWorkerCreateResponse,
        },
        'update': {
            'req': ser.CeleryWorkerUpdateRequest,
            'res': ser.CeleryWorkerUpdateResponse
        },
        'partial_update': {
            'req': ser.CeleryWorkerUpdateRequest,
            'res': ser.CeleryWorkerUpdateResponse
        },
        'retrieve': {
            'res': ser.CeleryWorkerRetrieveResponse
        },
        'list': {
            'res': ser.CeleryWorkerListResponse,
        },
        'refresh': {
            'res': ser.CeleryWorkerRefreshResponse,
        },
        'shutdown': {
            'req': ser.CeleryWorkerShutdownRequest,
            'res': ser.CeleryWorkerShutdownResponse
        },
    }

    permission_action_classes = {
        'create': [AllowAny, ],
        'update': [AllowAny, ],
        'partial_update': [AllowAny, ],
        'retrieve': [AllowAny, ],
        'list': [AllowAny, ],
        'destroy': [AllowAny, ],
        'refresh': [AllowAny, ],
        'shutdown': [AllowAny, ],
    }
    filter_backends = [CeleryWorkerNameFilterBackend,
                       CeleryWorkerStatusFilterBackend]

    @action(detail=False, methods=['GET'],
            url_name='refresh', url_path='refresh')
    def refresh(self, request, *args, **kwargs):
        reqser = self.get_serializer_response()
        reqser.clean_db_worker()
        return Response(data={}, status=HTTP_205_RESET_CONTENT)

    @action(detail=False, methods=['POST'],
            url_name='shutdown', url_path='shutdown')
    def shutdown(self, request, *args, **kwargs):
        reqser = self.get_serializer(data=request.data)
        reqser.is_valid(raise_exception=True)
        status = reqser.shutdown_worker()
        resser = self.get_serializer_response()(status)
        return Response(data=resser.data)
