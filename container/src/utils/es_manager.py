from elasticsearch import Elasticsearch


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ESConnection(metaclass=MetaSingleton):
    es = None

    def __init__(self, username=None, password=None,
                 port=None, host=None,
                 timeout=30):

        assert isinstance(host, str), "host should be a string"
        assert isinstance(port, int), "port should be an integer"
        assert 1 <= port <= 65535, "port must be a value between [1-65535]"

        self.host = host
        self.port = port
        self.index = None
        self.username = username
        self.password = password
        self.timeout = timeout

    def get_es_instance(self):
        http_auth = None

        if self.username and self.password:
            http_auth = (self.username, self.password)

        if self.es is None:
            self.es = Elasticsearch(self.host, http_auth=http_auth, port=self.port,
                                    timeout=self.timeout,
                                    ssl=True,
                                    dead_timeout=10, retry_on_timeout=10)
        return self.es

    def request_data(self, index=None, query=None):
        """
        retrieve result of elasticsearch query
        :param index:
        :param query: elasticsearch query
        :return: query result
        """
        assert isinstance(index, str), "index should be a string"

        es = self.get_es_instance()
        result = es.search(index=index,
                           body=query,
                           request_timeout=10)
        return result


if __name__ == '__main__':
    esA = ESConnection(username="changeme", password="changeme",
                       port=80, host="https://connido.com/services/es/v2/",
                       timeout=30)

    esB = ESConnection(username="changeme", password="changeme",
                       port=80, host="https://connido.com/services/es/v2/",
                       timeout=30)
    print("Elastic search  connection object esA", esA)
    print("Elastic search  connection object esB", esB)

    query: str = '{"query": {"match": {"doc.deviceId": "123456789"}}, "aggs": {"avgValues":' \
                 '{"filter": {"range": {"doc.startAt": {"gte": 1625582145, "lte": 1625586645}}}, ' \
                 '"aggs": {"avgActivity": {"avg": {"field": "doc.activity"}}, "avgSteps": {"avg": {"field": ' \
                 '"doc.steps"}}}}}}'
    index = "parent.*.summary-2021"

    print(esA.request_data(index, query))
    print(esB.request_data(index, query))
