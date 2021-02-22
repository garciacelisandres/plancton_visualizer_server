from pymongo import MongoClient


class Database:
    def __init__(self, url, db_name):
        self.conn = MongoClient(url)
        self.db = self.conn.get_database(db_name)

    def __del__(self):
        self.conn.close()

    def insert_sample(self, name, date_retrieved, sample_dict):
        try:
            db_classes = self.get_classes()
            classes_dict = self._join_classes(db_classes, sample_dict)
            sample = {
                "name": name,
                "date_retrieved": date_retrieved,
                "sample_classes": [{
                    "class_id": classes_dict[class_name],
                    "value": sample_dict[class_name]
                } for class_name in sample_dict]
            }
            self.db.samples.insert_one(sample)
        except Exception as e:
            print("Error while inserting sample.")
            print(e)

    def _join_classes(self, db_classes: list, sample_dict):
        classes_dict = {}
        db_class_names = [class_item["name"] for class_item in db_classes]
        for class_name in sample_dict.keys():
            if class_name in db_class_names:
                classes_dict[class_name] = next(
                    db_class["_id"] for db_class in db_classes if db_class["name"] == class_name
                )
            else:
                class_id = self.insert_class(class_name)
                classes_dict[class_name] = class_id
        return classes_dict

    def get_samples(self, sample_classes, start_time, end_time):
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
            samples_list = [sample for sample in self.db.samples.find(find_dict)]
            return samples_list
        except Exception:
            raise InterruptedError

    def insert_class(self, class_name):
        try:
            inserted = self.db.classes.insert_one({"name": class_name})
            return inserted.inserted_id
        except Exception:
            raise InterruptedError

    def get_classes(self):
        try:
            class_list = [class_obj for class_obj in self.db.classes.find({})]
            return class_list
        except Exception:
            raise InterruptedError

    def get_class(self, class_id):
        try:
            class_obj = self.db.classes.find_one({"_id": class_id})
            return class_obj
        except Exception:
            raise InterruptedError


def init_db(url: str, db_name: str) -> Database:
    db = Database(url, db_name)
    return db
