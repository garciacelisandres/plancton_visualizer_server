from datetime import datetime

from services.util import get_db_check_initialized


def get_samples(sample_classes: str, start_time: str, end_time: str, quant_method: str):
    if not (start_time is None):
        start_time = datetime.utcfromtimestamp(int(start_time))
    if not (end_time is None):
        end_time = datetime.utcfromtimestamp(int(end_time))
    if start_time and end_time and start_time > end_time:
        raise ValueError
    if sample_classes:
        sample_classes = sample_classes.split(",")
    try:
        sample_list = get_db_check_initialized().get_samples(sample_classes, start_time, end_time, quant_method)
    except InterruptedError:
        sample_list = []
    return sample_list
