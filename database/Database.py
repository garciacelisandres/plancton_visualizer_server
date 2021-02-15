def get_samples(mongo, sample_classes, start_time, end_time):
    if start_time > end_time:
        raise ValueError
    try:
        find_dict = {
            "$and": [
                {"date_retrieved": {"$gte": start_time}},
                {"date_retrieved": {"$lte": end_time}}
            ]
        }
        if not (sample_classes is None or len(sample_classes) == 0):
            find_dict["sample_classes"] = {"$in": sample_classes}
        samples_list = [sample for sample in mongo.samples.find(find_dict)]
        return samples_list
    except Exception as e:
        raise InterruptedError


def get_classes(mongo):
    try:
        class_list = [class_obj for class_obj in mongo.classes.find({})]
        return class_list
    except Exception:
        raise InterruptedError


def get_class(mongo, class_id):
    try:
        class_obj = mongo.classes.find_one({"_id": class_id})
        return class_obj
    except Exception:
        raise InterruptedError
