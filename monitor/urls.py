from rest_framework.routers import DefaultRouter
from monitor.views import CeleryTaskViewSet, CeleryWorkerViewSet
router = DefaultRouter()
router.register(r'tasks', CeleryTaskViewSet, basename='task')
router.register(r'workers', CeleryWorkerViewSet, basename='worker')

urlpatterns = router.urls
