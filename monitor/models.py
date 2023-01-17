from django.db import models
from monitor.core.base_model import BaseModel


class CeleryTask(BaseModel):

    STATUS_TASK = [
        ('PENDING', 'pending'),
        ('RECEIVED', 'received'),
        ('STARTED', 'started'),
        ('SUCCESS', 'success'),
        ('FAILED', 'failed'),
        ('REVOKED', 'revoked'),
        ('RETRY', 'retried'),
    ]
    name = models.CharField(max_length=200, null=True, blank=True)
    uuid = models.UUIDField(unique=True)
    status = models.CharField(
        max_length=9, choices=STATUS_TASK, default='PENDING')
    args = models.TextField(null=True, blank=True)
    kwargs = models.CharField(max_length=200, null=True, blank=True)
    result = models.CharField(max_length=200, null=True, blank=True)
    received = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    started = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    succeeded = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    retries = models.PositiveIntegerField(null=True, blank=True)
    runtime = models.FloatField(null=True, blank=True)
    exception = models.TextField(null=True, blank=True)
    traceback = models.TextField(null=True, blank=True)
    worker = models.CharField(max_length=200, null=True, blank=True)
    root_id = models.UUIDField(null=True, blank=True)
    parent_id = models.UUIDField(null=True, blank=True)
    children = models.TextField(null=True, blank=True)
    asn_id = models.UUIDField(null=True, blank=True)
    asn_number = models.IntegerField(null=True, blank=True)
    queue = models.CharField(max_length=200, null=True, blank=True)
    published = models.BooleanField(default=1)

    class Meta:
        verbose_name = 'celery_task'
        db_table = 'celery_tasks'
        verbose_name_plural = 'celery_tasks'
        ordering = ['-last_modified']


class CeleryWorker(BaseModel):

    name = models.CharField(max_length=200, unique=True)
    status = models.BooleanField(default=0)
    active = models.PositiveIntegerField(default=0)
    processed = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'celery_worker'
        db_table = 'celery_workers'
        verbose_name_plural = 'celery_workers'
        ordering = ['-last_modified']
