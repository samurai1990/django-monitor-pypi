## worker event without run task:

```json
{
    "hostname": "celery@2f2fc4a1c195",
    "utcoffset": 0,
    "pid": 1,
    "clock": 16146,
    "freq": 2.0,
    "active": 0,
    "processed": 24,
    "loadavg": [
        1.13,
        1.24,
        1.08
    ],
    "sw_ident": "py-celery",
    "sw_ver": "5.2.7",
    "sw_sys": "Linux",
    "timestamp": 1661786667.0285149,
    "type": "worker-heartbeat",
    "local_received": 1661761467.0304306
}
```


## worker event task-started:

```json
{
    "hostname": "celery@2f2fc4a1c195",
    "utcoffset": 0,
    "pid": 1,
    "clock": 28645,
    "uuid": "5c523254-3400-4caf-914c-eaae67b823f3",
    "timestamp": 1661771881.6648102,
    "type": "task-started",
    "local_received": 1661771881.6679735
}
```


## worker event task-received:

```json
{
    "hostname": "celery@2f2fc4a1c195",
    "utcoffset": 0,
    "pid": 1,
    "clock": 28644,
    "uuid": "5c523254-3400-4caf-914c-eaae67b823f3",
    "name": "scan.tasks.port_enumerate",
    "args": "["499555d5-bc88-4b32-b415-3243a24b46fa", [{"packet": UUID("209c14f7-b36f-4efb-8b72-e45ce612bd85"), "ports": [...]}], None]",
    "kwargs": "{}",
    "root_id": "5c523254-3400-4caf-914c-eaae67b823f3",
    "parent_id": None,
    "retries": 0,
    "eta": None,
    "expires": None,
    "timestamp": 1661771881.6616628,
    "type": "task-received",
    "local_received": 1661771881.6672893
}
```


## worker event task-succeeded:

```json
{
    "hostname": "celery@2f2fc4a1c195",
    "utcoffset": 0,
    "pid": 1,
    "clock": 28649,
    "uuid": "5c523254-3400-4caf-914c-eaae67b823f3",
    "result": "'enumeration successful! 2 enumerated with priority: 5 | Started_time: 2022-08-29 11: 18: 01.664987,succeeded_time: 2022-08-29 11: 18: 01.674585'",
    "runtime": 0.029637871000886662,
    "timestamp": 1661771881.6955085,
    "type": "task-succeeded",
    "local_received": 1661771881.7000241
}
```


## worker event task-failed:

```json
{
    "hostname": "celery@2f2fc4a1c195",
    "utcoffset": 0,
    "pid": 1,
    "clock": 112,
    "uuid": "89abc381-de5c-4959-a700-eb113a02b2e1",
    "exception": "UnboundLocalError('local variable \"host\" referenced before assignment')", 
    "traceback": "Traceback (most recent call last):\n  File '/usr/local/lib/python3.10/site-packages/django/db/models/fields/__init__.py', line 2434, in to_python\n",
    "timestamp": 1661805101.3329527,
    "type": "task-failed",
    "local_received": 1661779901.3365095
}
```

## worker event task-revoked:

```json
{
    "hostname": "celery@5c5f14cc05d7",
    "utcoffset": 0,
    "pid": 1,
    "clock": 5791,
    "uuid": "5cd25849-b7e8-40e0-b812-ab64c0e48f17",
    "terminated": True,
    "signum": 9,
    "expired": False,
    "timestamp": 1662471930.0537322,
    "type": "task-revoked",
    "local_received": 1662471933.1290903
}
```
---


# tasks App API Document

## celery task
### Create CeleryTask
* permission: `Authenticated`

* endpoint: `monitor/tasks/`

* HTTP method: `POST`

* request:
```json
{
    "name": "function name",
    "uuid": UUID("2acef619-cb56-4f7b-9777-936dc5cb371b"),
    "args": "["ebe9105c-ce19-4753-835d-293c35139dd3", [{"packet": "91242d1a-0c2d-4298-913d-b8a0c9a52f35", "ports": [{"number": 8800, "proto": "http"}]}], None]",
    "kwargs": "",
    "result": "",
    "received": datetime.datetime(2022,8,30,10,43,46,758455, tzinfo=<UTC>),
    "started": datetime.datetime(2022,8,30,10,43,46,758469, tzinfo=<UTC>),
    "succeeded": datetime.datetime(2022,8,30,10,43,46,758474, tzinfo=<UTC>),
    "retries": 0,
    "runtime": 1.14053136,
    "exception": "no exception",
    "traceback": "no error",
    "worker": "woker_1",
    "root_id": UUID("05baf5b4-090a-42de-9f92-766512fd3d9e"),
    "parent_id": UUID("e46aeb77-5b92-4b51-9f7f-fb734f705763")
}
```

* ok Response
```json
{
    "err": false,
    "err_code": 0,
    "err_msg": null,
    "data": {
        "celerytask": {
            "id": "b7b2cab4-44ce-42ce-ba19-35f1db9dba1b",
            "name": "function name",
            "uuid": "2acef619-cb56-4f7b-9777-936dc5cb371b",
            "status": "p",
            "args": "["ebe9105c-ce19-4753-835d-293c35139dd3", [{"packet": "91242d1a-0c2d-4298-913d-b8a0c9a52f35", "ports": [{"number": 8800, "proto": "http"}]}], None]",
            "kwargs": "",
            "result": "",
            "received": "2022-08-30T10:43:46.758455Z",
            "started": "2022-08-30T10:43:46.758469Z",
            "succeeded": "2022-08-30T10:43:46.758474Z",
            "retries": 0,
            "runtime": 1.14053136,
            "exception": "no exception",
            "traceback": "no error",
            "worker": "woker_1",
            "root_id": "05baf5b4-090a-42de-9f92-766512fd3d9e",
            "parent_id": "e46aeb77-5b92-4b51-9f7f-fb734f705763"
        }
    }
}
```

### Parial Update CeleryTask
* permission: `Authenticated`

* endpoint: `monitor/tasks/<id>/`

* HTTP method: `PATCH`

* request:
```json
{
    "status": "s"
}
```

* ok Response
```json
{
    "err": false,
    "err_code": 0,
    "err_msg": null,
    "data": {
        "celerytask": {
            "id": "f8b3b9d9-b062-4d78-97d3-78c8ba3cc9c0",
            "name": "function name",
            "uuid": "8c3e2c5e-ebf0-4d9d-abcf-1a4a2be29e5c",
            "status": "s",
            "args": "["ebe9105c-ce19-4753-835d-293c35139dd3", [{"packet": "91242d1a-0c2d-4298-913d-b8a0c9a52f35", "ports": [{"number": 8800, "proto": "http"}]}], None]",
            "kwargs": "",
            "result": "",
            "received": "2022-08-30T10:58:43.787112Z",
            "started": "2022-08-30T10:58:43.787116Z",
            "succeeded": "2022-08-30T10:58:43.787118Z",
            "retries": 0,
            "runtime": 1.14053136,
            "exception": "no exception",
            "traceback": "no error",
            "worker": "woker_1",
            "root_id": "25804ed9-e0fa-492b-91f8-1074d6474e1d",
            "parent_id": "b72a153f-1034-49d6-98c4-961f214b3ed9"
        }
    }
}
```

### Retrieve CeleryTask
* permission: `Authenticated`

* endpoint: `monitor/tasks/<id>/`

* query_params: `sync`

* HTTP method: `GET`

* ok Response
```json
{
    "err": false,
    "err_code": 0,
    "err_msg": null,
    "data": {
        "celerytask": {
            "id": "a2c44f27-2126-45b7-b505-3d0f9f0a9158",
            "name": null,
            "uuid": "81933c68-b4b2-4bf2-bc48-50998ce0873c",
            "status": "SUCCESS",
            "args": "['ad3ead73-aa95-44fc-9e40-c252a7b44042', 8888, 'http', '1eb2e2a8-3d87-4aea-b466-b1d04f4ed159', None]",
            "kwargs": null,
            "cidr_id": "ad3ead73-aa95-44fc-9e40-c252a7b44042",
            "cidr_ip_network": "192.168.10.8/29",
            "asn_id": "91117477-bfde-4d0f-8a48-fe10ee90c64f",
            "asn_number": 123456,
            "result": "None",
            "received": null,
            "started": null,
            "succeeded": "2022-11-22T16:40:55.792000Z",
            "retries": null,
            "runtime": 25.596107771998504,
            "exception": null,
            "traceback": null,
            "worker": "celery@5b6fa28ac4b7",
            "root_id": null,
            "parent_id": null,
            "children": "[]"
        }
    }
}
```

### List CeleryTask
* permission: `Authenticated`

* endpoint: `monitor/tasks/`

* HTTP method: `GET`

* query_params: `uuid` , `status`

* ok Response
```json
{
    "err": False,
    "err_code": 0,
    "err_msg": None,
    "data": {
        "celery_tasks": [
            {
                "id": "e265f75f-9e0a-4d1a-9f2b-08f2345bbf7f",
                "name": null,
                "uuid": "70470c08-4d95-4191-bf18-85694247de24",
                "status": "SUCCESS",
                "args": "['ad3ead73-aa95-44fc-9e40-c252a7b44042', [{'packet': '1eb2e2a8-3d87-4aea-b466-b1d04f4ed159', 'ports': [{'number': 2222, 'proto': 'http'}, {'number': 8888, 'proto': 'http'}]}], None]",
                "kwargs": null,
                "cidr_id": "ad3ead73-aa95-44fc-9e40-c252a7b44042",
                "cidr_ip_network": "192.168.10.8/29",
                "asn_id": "91117477-bfde-4d0f-8a48-fe10ee90c64f",
                "asn_number": 123456,
                "result": "'nubmer: 2 enumeration successfully!  with priority: 5'",
                "received": null,
                "started": null,
                "succeeded": "2022-11-23T09:20:11.205000Z",
                "retries": null,
                "runtime": 0.005472685999848181,
                "exception": null,
                "traceback": null,
                "worker": "celery@372f72dcbc19",
                "root_id": null,
                "parent_id": null,
                "children": "['4c63f80e-1ead-41a1-af98-029b5e9d8721', '512c2699-c20f-4b99-aff5-fd7e26359829']"
            },
            {
                "id": "a2c44f27-2126-45b7-b505-3d0f9f0a9158",
                "name": null,
                "uuid": "81933c68-b4b2-4bf2-bc48-50998ce0873c",
                "status": "SUCCESS",
                "args": "['ad3ead73-aa95-44fc-9e40-c252a7b44042', 8888, 'http', '1eb2e2a8-3d87-4aea-b466-b1d04f4ed159', None]",
                "kwargs": null,
                "cidr_id": "ad3ead73-aa95-44fc-9e40-c252a7b44042",
                "cidr_ip_network": "192.168.10.8/29",
                "asn_id": "91117477-bfde-4d0f-8a48-fe10ee90c64f",
                "asn_number": 123456,
                "result": "None",
                "received": null,
                "started": null,
                "succeeded": "2022-11-22T16:40:55.792000Z",
                "retries": null,
                "runtime": 25.596107771998504,
                "exception": null,
                "traceback": null,
                "worker": "celery@5b6fa28ac4b7",
                "root_id": null,
                "parent_id": null,
                "children": "[]"
            }
        ]
    }
}
```

## Example CeleryTask filter params: 
```
filter by uuid:
`{'uuid': '2d983ed1-56e0-4e43-92d7-0f27061660fb'}`

filter by status:
`{'status': 'SUCCESS'}`

filter by cidr id:
`{'cidr_id': '9a132304-d63b-432a-9dd5-1c6cd8d70ad6'}`

filter by cidr ip network:
`{'cidr_ip_network': '192.168.255.0/24'}`

filter by asn id:
`{'asn_id': '17106365-28e4-402e-a1d0-4e43e23ec579'}`

filter by asn number:
`{'asn_number': 99999}`

filter by parent id:
`{'parent_id': '7f6630d0-89b7-420a-b75a-2e06008630ff'}`

filter by queue:
`{'queue': 'unic_queue'}`

filter by published:
`{'published': False}`
```

### Delete CeleryTask
* permission: `Authenticated`

* endpoint: `monitor/tasks/<id>/`

* HTTP method: `DELETE`

* http status code: `204`


### Revoke CeleryTask
* permission: `Authenticated`

* endpoint: `monitor/tasks/revoke/`

* HTTP method: `POST`

* http status code: `200`

* request:
```json
{
    "ides": [
        "00895719-cd65-4927-9934-2f749de24acc",
        "00895719-cd65-4927-9934-2f749de24abc",
        "00895719-cd65-4927-9934-2f749de24aac"
    ]
}
```

* ok Response
```json
{
    "err": false,
    "err_code": 0,
    "err_msg": null,
    "data": {
        "list_revokes": {
            "celery@23449ff1aad0": [
                "00895719-cd65-4927-9934-2f749de24acc",
                "00895719-cd65-4927-9934-2f749de24aac",
                "00895719-cd65-4927-9934-2f749de24abc"
            ],
            "celery@560711da82a0": [
                "00895719-cd65-4927-9934-2f749de24acc",
                "00895719-cd65-4927-9934-2f749de24aac",
                "00895719-cd65-4927-9934-2f749de24abc"
            ]
        }
    }
}
```

### Synchronized CeleryTask
* permission: `Authenticated`

* endpoint: `monitor/tasks/sync/`

* HTTP method: `GET`

* ok Response
```json
{
    "err": false,
    "err_code": 0,
    "err_msg": null,
    "data": "5 numbers were synchronized."
}
```
---


## celery worker
### Create CeleryWorker

* permission: `Authenticated`

* endpoint: `monitor/workers/`

* HTTP method: `POST`

* request:
```json
{
    "name": "celery@5414",
    "status": 0
}
```

* ok Response
```json
{
    "err": false,
    "err_code": 0,
    "err_msg": null,
    "data": {
        "celeryworker": {
            "id": "52bdd980-0542-450f-a9fb-31937db0dbad",
            "name": "celery@5414",
            "status": 0
        }
    }
}
```

### Parial Update CeleryWorker
* permission: `Authenticated`

* endpoint: `monitor/workers/<id>/`

* HTTP method: `PATCH`

* request:
```json
{
    "status": 1
}
```

* ok Response
```json
{
    "err": false,
    "err_code": 0,
    "err_msg": null,
    "data": {
        "celeryworker": {
            "id": "d7bb2e0d-05db-41fa-bc15-08b794630493",
            "name": "celery@5306",
            "status": 1
        }
    }
}
```

### Retrieve CeleryWorker
* permission: `Authenticated`

* endpoint: `monitor/workers/<id>/`

* HTTP method: `GET`

* ok Response
```json
{
    "err": false,
    "err_code": 0,
    "err_msg": null,
    "data": {
        "celeryworker": {
            "id": "9bdc8575-5e04-4df5-bd1d-7b4dc0f3b1d7",
            "name": "celery@5828",
            "status": false
        }
    }
}
```

### List CeleryWorker
* permission: `Authenticated`

* endpoint: `monitor/workers/`

* HTTP method: `GET`

* query_params: `name` , `status`

* ok Response
```json
{
    "err": false,
    "err_code": 0,
    "err_msg": null,
    "data": {
        "celery_workers": [
            {
                "id": "c0b7d51a-a698-499c-8640-6931da969764",
                "name": "celery@5146",
                "status": false
            },
            {
                "id": "64aea3f8-463f-4231-a71c-0e8b5efcf2fe",
                "name": "celery@5954",
                "status": true
            }
        ]
    }
}
```
## Example CeleryWorker filter params:
```
filter by name:
`{'name': 'celery@t5022'}`

filter by status:
`{'status': 0}`
```

### Delete CeleryWorker
* permission: `Authenticated`

* endpoint: `monitor/workers/<id>`

* HTTP method: `DELETE`

* http status code: `204`


### Refresh CeleryWorker
* permission: `Authenticated`

* endpoint: `monitor/workers/refresh`

* HTTP method: `GET`

* http status code: `205`


### Shutdown CeleryWorker
* permission: `Authenticated`

* endpoint: `monitor/workers/shutdown`

* HTTP method: `POST`

* http status code: `200`

* request:
```json
{
    "names": [
        "celery@560711da82a0",
        "celery@560711da821"
    ]
}
```

* ok Response
```json
{
    "err": false,
    "err_code": 0,
    "err_msg": null,
    "data": {
        "names": [
            "{'celery@560711da82a0': 'shutdown', 'celery@560711da821': 'shutdown'}"
        ]
    }
}
```
---
### Dashboard Monitor
* permission: `Authenticated`

* endpoint: `/monitor/tasks/dashboard/`

* HTTP method: `GET`

* ok Response
```json
{
    "err": false,
    "err_code": 0,
    "err_msg": null,
    "data": {
        "worker": {
            "worker_online": 9,
            "worker_offline": 4,
            "worker_task_active": 180,
            "worker_task_processed": 920
        },
        "task": {
            "task_pending": 19,
            "task_received": 14,
            "task_started": 5,
            "task_success": 17,
            "task_failed": 29,
            "task_revoked": 19,
            "task_retried": 2
        }
    }
}
```