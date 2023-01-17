from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from uuid import uuid4
from monitor.mocks import (get_sample_celery_task_data,
                           get_sample_celery_task_model,
                           get_sample_celery_worker_data,
                           get_sample_celery_worker_model)

from monitor.models import CeleryWorker
import json


class TaskTestCase(TestCase):
    databases = {'default', 'monitor'}

    def test_create_celery_task(self):
        task = get_sample_celery_task_model()
        self.assertIsNotNone(task)

    def test_create_celery_worker(self):
        worker = get_sample_celery_worker_model()
        self.assertIsNotNone(worker)


class TaskAPITestCase(APITestCase):
    databases = {'default', 'monitor'}

    def setUp(self):
        self.parent_id = str(uuid4())

    def _create_sample_celery_task(self):
        for i in range(10):
            if i % 2 == 0:
                self.instance_task = get_sample_celery_task_model(
                    status='SUCCESS', published=False)
            else:
                get_sample_celery_task_model(
                    parent_id=self.parent_id, published=True)

    def test_create_celery_task(self):
        url = reverse('task-list')
        data = get_sample_celery_task_data(
            status="SUCCESS", queue='unic_queue')
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.json().get('celerytask'))
        return response.json().get('celerytask')

    def test_partial_update_celery_task(self):
        task = self.test_create_celery_task()
        url = reverse('task-detail', args={task.get('id')})
        data = {'status': "REVOKED"}
        response = self.client.patch(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get(
            'celerytask').get('status'), "REVOKED")

    def test_retrieve_celery_task(self):
        task = self.test_create_celery_task()
        url = reverse('task-detail', args={task.get('id')})
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.json().get('celerytask')

    def test_list_celery_task(self):
        self._create_sample_celery_task()
        url = reverse('task-list')
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.json().get('celery_tasks')), 10)

    def test_delete_celery_task(self):
        task = self.test_create_celery_task()
        url = reverse('task-detail', args={task.get('id')})
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_uuid(self):
        self._create_sample_celery_task()
        url = reverse('task-list')
        params = {'uuid': str(self.instance_task.uuid)}
        response = self.client.get(path=url, data=params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.json().get('celery_tasks')), 1)
        self.assertEqual(response.json().get('celery_tasks')
                         [0].get("uuid"), params["uuid"])

    def test_filter_status(self):
        self._create_sample_celery_task()
        url = reverse('task-list')
        params = {'status': 'SUCCESS'}
        response = self.client.get(path=url, data=params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.json().get('celery_tasks')), 5)
        self.assertEqual(
            response.json().get('celery_tasks')[0].get("status"), params["status"])

    def test_filter_task_by_parent_id(self):
        task = self.test_create_celery_task()
        self._create_sample_celery_task()
        url = reverse('task-list')
        params = {'parent_id': self.parent_id}
        response = self.client.get(path=url, data=params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.json().get('celery_tasks')), 5)
        self.assertEqual(
            response.json().get("celery_tasks")[0].get("parent_id"), params["parent_id"])

    def test_filter_task_by_queue(self):
        task = self.test_create_celery_task()
        self._create_sample_celery_task()
        url = reverse('task-list')
        params = {'queue': task.get("queue")}
        response = self.client.get(path=url, data=params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.json().get('celery_tasks')), 1)
        self.assertEqual(
            response.json().get("celery_tasks")[0].get("queue"), params["queue"])

    def test_filter_task_by_published(self):
        self._create_sample_celery_task()
        url = reverse('task-list')
        params = {'published': False}
        response = self.client.get(path=url, data=params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.json().get('celery_tasks')), 5)
        self.assertEqual(
            response.json().get("celery_tasks")[0].get("published"), params["published"])

    def test_sync_tasks(self):
        self._create_sample_celery_task()
        url = reverse('task-sync')
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dashboard(self):
        for i in range(0, 9):
            if i == 0:
                [get_sample_celery_worker_model(status=1, active=20, processed=100)
                 for i in range(1, 10)]
            elif i == 1:
                [get_sample_celery_task_model(status="PENDING")
                 for i in range(1, 20)]
            elif i == 2:
                [get_sample_celery_task_model(status="RECEIVED")
                 for i in range(1, 15)]
            elif i == 3:
                [get_sample_celery_task_model(status="STARTED")
                 for i in range(1, 6)]
            elif i == 4:
                [get_sample_celery_task_model(status="SUCCESS")
                 for i in range(1, 18)]
            elif i == 5:
                [get_sample_celery_task_model(status="FAILED")
                 for i in range(1, 30)]
            elif i == 6:
                [get_sample_celery_task_model(status="REVOKED")
                 for i in range(1, 20)]
            elif i == 7:
                [get_sample_celery_task_model(status="RETRY")
                 for i in range(1, 3)]
            else:
                [get_sample_celery_worker_model(
                    processed=5) for i in range(1, 5)]
        url = reverse('task-dashboard')
        response = self.client.get(path=url)
        true_response = {"worker": {"worker_online": 9, "worker_offline": 4, "worker_task_active": 180, "worker_task_processed": 920}, "task": {
            "task_pending": 19, "task_received": 14, "task_started": 5, "task_success": 17, "task_failed": 29, "task_revoked": 19, "task_retried": 2}}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertJSONEqual(json.dumps(
            response.json()), json.dumps(true_response))


class WorkerAPITestCase(APITestCase):
    databases = {'default', 'monitor'}

    def _create_sample_celery_worker(self):
        for i in range(10):
            if i % 2 == 0:
                self.instance_worker = get_sample_celery_worker_model(status=1)
            else:
                get_sample_celery_worker_model()

    def test_create_celery_worker(self):
        url = reverse('worker-list')
        data = get_sample_celery_worker_data()
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.json().get('celeryworker'))
        return response.json().get('celeryworker')

    def test_partial_update_celery_worker(self):
        worker = self.test_create_celery_worker()
        url = reverse('worker-detail', args={worker.get('id')})
        data = {'status': 1}
        response = self.client.patch(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_celery_worker(self):
        worker = self.test_create_celery_worker()
        url = reverse('worker-detail', args={worker.get('id')})
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_celery_worker(self):
        self._create_sample_celery_worker()
        url = reverse('worker-list')
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.json().get('celery_workers')), 10)

    def test_delete_celery_worker(self):
        worker = self.test_create_celery_worker()
        url = reverse('worker-detail', args={worker.get('id')})
        response = self.client.delete(path=url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_name(self):
        self._create_sample_celery_worker()
        url = reverse('worker-list')
        params = {'name': self.instance_worker.name}
        response = self.client.get(path=url, data=params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.json().get('celery_workers')), 1)
        self.assertEqual(response.json().get(
            'celery_workers')[0].get("name"), params["name"])

    def test_filter_status(self):
        self._create_sample_celery_worker()
        url = reverse('worker-list')
        params = {'status': 0}
        response = self.client.get(path=url, data=params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.json().get('celery_workers')), 5)
        self.assertEqual(response.json().get(
            'celery_workers')[0].get("status"), params["status"])

    def test_refresh_worker(self):
        self._create_sample_celery_worker()
        url = reverse('worker-refresh')
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        nimber_worker = CeleryWorker.objects.all().count()
        self.assertEqual(nimber_worker, 0)
