from dynaconf import Dynaconf


redis_client = None
def FakeRedisClient(*args, **kwargs):
    global redis_client
    if not redis_client:
        redis_client = _FakeRedisClient(*args, **kwargs)
    return redis_client


class _FakeRedisClient:

    def __init__(self, *args, **kwargs):
        self.values = {}
        self._args = args
        self._kwargs = kwargs

    def _clear(self):
        self.values = {}

    def _add(self, key, value):
        self.values[key] = value

    def exists(self, key):
        return key in self.values

    def get(self, key):
        return self.values[key]

    def set(self, key, value):
        self.values[key] = value

    def delete(self, key):
        if not key in self.values:
            return 0
        del self.values[key]
        return 1

    def expire(self, key, time):
        pass

    def pipeline(self):
        return self

    def execute(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        pass


class FakeFlaskApp:

    def __init__(self, *args, **kwargs):
        pass

    @property
    def config(self):
        return Dynaconf(
            settings_files=['settings.toml']
        )['default']


class FakeMongoQuery:

    def __init__(self, result_set):
        self.result_set = result_set

    def distinct(self, key):
        self.result_set = list(set(x[key] for x in self.result_set))
        return self

    def find_one(self, query):
        for elem in self.result_set:
            ok = True
            for key in query.keys():
                if key not in elem or elem[key] != query[key]:
                    ok = False
                    break
            if ok:
                return elem

    def __iter__(self):
        return iter(self.result_set)


class FakeMongoTable:

    def __init__(self, *args, **kwargs):
        self.elements = []

    def find(self):
        return FakeMongoQuery(self.elements)

    def find_one(self, query):
        return FakeMongoQuery(self.elements).find_one(query)

    def insert_one(self, item):
        self._add(item)

    def _find_index_of(self, query):
        for idx, elem in enumerate(self.elements):
            keys = query.keys()
            matches = all(key in elem and elem[key] == query[key] for key in keys)
            if matches:
                return idx

    def delete_one(self, query):
        matching_index = self._find_index_of(query)
        if isinstance(matching_index, int):
            del self.elements[matching_index]

    def _add(self, element):
        self.elements.append(element)


class FakeMongoDb:

    def __init__(self, *args, **kwargs):
        pass

    def _add_table(self, name):
        setattr(self, name, FakeMongoTable())


mongo_client = None
def FakeMongoClient(*args, **kwargs):
    global mongo_client
    if mongo_client is None:
        mongo_client = _FakeMongoClient(*args, **kwargs)
    return mongo_client

class _FakeMongoClient:

    def __init__(self, *args, **kwargs):
        self.db_mapping = {}

    def __getitem__(self, key):
        if not key in self.db_mapping:
            self.db_mapping[key] = FakeMongoDb()
        return self.db_mapping[key]
