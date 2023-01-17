from rest_framework.filters import BaseFilterBackend
from distutils.util import strtobool


class CeleryTaskUUIDFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        try:
            uuid = request.query_params.get('uuid', None)
            if uuid is not None:
                return queryset.filter(uuid=uuid)
            else:
                return queryset
        except Exception:
            return queryset


class CeleryTaskStatusFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        try:
            status = request.query_params.get('status', None)
            if status is not None:
                return queryset.filter(status=status)
            else:
                return queryset
        except Exception:
            return queryset


class CeleryTaskParentIdFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        try:
            parent_id = request.query_params.get('parent_id', None)
            if parent_id is not None:
                return queryset.filter(parent_id=parent_id)
            else:
                return queryset
        except Exception:
            return queryset


class CeleryTaskQueueFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        try:
            queue = request.query_params.get('queue', None)
            if queue is not None:
                return queryset.filter(queue=queue)
            else:
                return queryset
        except Exception:
            return queryset


class CeleryTaskPublishedFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        try:
            published = request.query_params.get('published', None)
            if published is not None:
                return queryset.filter(published__in=[strtobool(published.capitalize())])
            else:
                return queryset
        except Exception:
            return queryset


class CeleryWorkerNameFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        try:
            name = request.query_params.get('name', None)
            if name is not None:
                return queryset.filter(name=name)
            else:
                return queryset
        except Exception:
            return queryset


class CeleryWorkerStatusFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        try:
            status = request.query_params.get('status', None)
            if status is not None:
                return queryset.filter(status__in=[strtobool(status.capitalize())])
            else:
                return queryset
        except Exception:
            return queryset
