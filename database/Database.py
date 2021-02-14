def get_samples(mongo, sample_classes, start_time, end_time):
    if start_time > end_time:
        raise ValueError
    try:
        find_dict = {
            "start_time": {"$ge": start_time},
            "end_time": {"$le": end_time}
        }
        if not(sample_classes is None or len(sample_classes) == 0):
            find_dict["sample_classes"] = {"$in": sample_classes}
        mongo.samples.find(find_dict)
    except:
        raise InterruptedError


def get_classes(mongo):
    try:
        class_list = mongo.classes.find({})
        return class_list
    except:
        raise InterruptedError


def get_class(mongo, class_id):
    try:
        class_obj = mongo.classes.find({"_id": class_id})
        return class_obj
    except:
        raise InterruptedError
