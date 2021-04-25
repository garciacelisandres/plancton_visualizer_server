from bson import ObjectId


def filter_samples_apply_filters(**kwargs) -> list:
    filter_list = []
    # Filter dates
    filter_list.append(filter_samples_dates(start_time=kwargs["start_time"], end_time=kwargs["end_time"]))
    # Filter sample classes
    filter_list.append(filter_samples_sample_classes(sample_classes=kwargs["sample_classes"]))
    # Filter quantification methods
    filter_list.extend(filter_samples_quant_method(quant_method=kwargs["quant_method"]))
    return list(filter(lambda d: len(d) > 0, filter_list))


def filter_samples_dates(start_time, end_time) -> dict:
    dates_list = []  # holds the date filters as a list
    find_dict = {}  # holds the combined date filters as a dict
    if not (start_time is None):
        dates_list.append({"date_retrieved": {"$gte": start_time}})
    if not (end_time is None):
        dates_list.append({"date_retrieved": {"$lte": end_time}})
    if len(dates_list) > 0:
        find_dict["$and"] = dates_list
    return {"$match": find_dict}


def filter_samples_sample_classes(sample_classes) -> dict:
    if not (sample_classes is None or len(sample_classes) == 0):
        return {"$project": {
            "name": 1,
            "date_retrieved": 1,
            "sample_classes": {
                "$filter": {
                    "input": "$sample_classes",
                    "as": "sample_class",
                    "cond": {
                        "$in": ["$$sample_class.class_id",
                                [ObjectId(sample_class) for sample_class in sample_classes]]
                    }
                }
            }
        }}
    else:
        return {}


def filter_samples_quant_method(quant_method) -> list:
    if not (quant_method is None or len(quant_method) == 0):
        return [{
            "$unwind": "$sample_classes"
        },
            {
                "$project": {
                    "name": 1,
                    "date_retrieved": 1,
                    "sample_classes.class_id": 1,
                    "sample_classes.values": {
                        "$filter": {
                            "input": "$sample_classes.values",
                            "as": "quant_method",
                            "cond": {
                                "$in": [
                                    "$$quant_method.method",
                                    quant_method
                                ]
                            }
                        }
                    }
                }
            },
            {
                "$group": {
                    "_id": "$_id",
                    "name": {
                        "$first": "$name"
                    },
                    "date_retrieved": {
                        "$first": "$date_retrieved"
                    },
                    "sample_classes": {
                        "$push": "$sample_classes"
                    }
                }
            }]
    else:
        return []
