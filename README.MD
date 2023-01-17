=====
Monitor
=====

Monitor is a Django app to conduct Web-based monitor. For each question,
visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------


1. install package:

pip install ./django-monitor-0.1.tar.gz

2. Add "monitor" to your INSTALLED_APPS setting like this::

    ```
    INSTALLED_APPS = [
        ...
        'monitor',
    ]
    ```

3. Include the monitor URLconf in your project urls.py like this::

    ```
    path('monitor/', include('monitor.urls')),
    ```

4. write in file dbrouter.py ::
    ```
    from monitor.models import CeleryTask, CeleryWorker

    class DbRouter:
        def db_for_read(self, model, **hints):
            if model == CeleryTask or model == CeleryWorker:
                return 'monitor'
            return 'default'

        def db_for_write(self, model, **hints):
            if model == CeleryTask or model == CeleryWorker:
                return 'monitor'
            return 'default'

        def allow_relation(self, obj1, obj2, **hints):
            return True

        def allow_migrate(self, db, app_label, model_name=None, **hints):
            if app_label == 'monitor':
                return db == 'monitor'
            return True
    ```

5. set config db router and config monitor databse in settings.py :
    `DATABASE_ROUTERS = ('${projects name}.dbrouter.DbRouter',)`

6. config databse :

    ```
    DATABASES = {
        ...,
        'monitor': {
            'ENGINE': 'djongo',
            'NAME': 'monitor',
            'CLIENT': {
                'host': getenv('DJANGO_MONGO_HOST'),
            },
        },
    }
    ```
6. confing logging:

    ```
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '[%(asctime)s] %(levelname)s | %(funcName)s | %(name)s | %(lineno)s | %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'handlers': {
            'logfile': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': f'{BASE_DIR}/api.log',
                'formatter': 'standard',
            },
            'contract_info_monitor': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': f'{BASE_DIR}/monitor.log',
                'formatter': 'standard',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['logfile'],
            },
        'monitor': {
                'handlers': ['contract_info_monitor'],
                'level': 'INFO',
            },
        }
    }
    ```

7. Run ``python manage.py migrate`` to create the monitor models.

8. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

9.  Visit http://127.0.0.1:8000/monitor/ to participate in the poll.

10. for run monitoring celery event run command:
`python manage.py monitor` 


Note:
The worker has the ability to send a message whenever some event happens. These events are then captured by tools like Flower, and celery events to monitor the cluster:

`run worker with -E switch option`

##### Note: How to write reusable apps
https://docs.djangoproject.com/en/3.2/intro/reusable-apps/


building monitor package with `python3 setup.py sdist` (run from inside django-monitor)