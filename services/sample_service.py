from datetime import datetime

from services.errorhandlers import errorlogger
from services.util import get_db_check_initialized
from util.customerrors import InvalidDateRangeError


@errorlogger
def get_samples(sample_classes: str, start_time: str, end_time: str, quant_method: str):
    if not (start_time is None):
        start_time = datetime.utcfromtimestamp(int(start_time))
    if not (end_time is None):
        end_time = datetime.utcfromtimestamp(int(end_time))
    if start_time and end_time and start_time > end_time:
        raise InvalidDateRangeError(
            "Error while getting the samples: \"start_time\" parameter was greater than \"end_time\" parameter."
        )
    if sample_classes:
        sample_classes = sample_classes.split(",")
    if quant_method:
        quant_method = quant_method.split(",")
    try:
        sample_list = get_db_check_initialized().get_samples(sample_classes, start_time, end_time, quant_method)
    except InterruptedError:
        sample_list = []
    return sample_list
