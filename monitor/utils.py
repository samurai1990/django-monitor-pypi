from celery.result import AsyncResult
from logging import getLogger
from pytz import utc
from distutils.util import strtobool
from datetime import datetime
from django.utils import timezone

logger = getLogger("monitor")


def add_timezone_to_timestamp(time):
    parsed_date = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%f')
    current_tz = timezone.get_current_timezone()
    return current_tz.localize(parsed_date)


def _update_data(instance_model):
    data = {}
    try:
        params = AsyncResult(str(instance_model.uuid))._get_task_meta()
        for param_key, param_value in params.items():
            if param_key == 'date_done':
                data["succeeded"] = add_timezone_to_timestamp(param_value)
            elif param_key == "children":
                data["children"] = [obj.id for obj in param_value]
            elif param_key == "task_id":
                pass
            else:
                data[param_key] = param_value
    except TypeError as exp:
        pass
    finally:
        if params.get("status") == "SUCCESS":
            data["published"] = False
        instance_model.__dict__.update(**data)
        instance_model.save()


def sync_status_task(instance, unic=False):
    count = 0
    try:
        if unic:
            _update_data(instance)
        else:
            queries = instance.objects.filter(
                published__in=[strtobool('True')])
            if queries is not None:
                for query in queries:
                    _update_data(query)
                    count += 1
    except Exception as exp:
        logger.error(f'during exception : {exp}')
        return 0
    return count


def timestamp_to_datatime(time):
    return datetime.utcfromtimestamp(time).replace(tzinfo=utc)
