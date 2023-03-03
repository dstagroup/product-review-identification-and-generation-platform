from elasticsearch import Elasticsearch



if __name__ == '__main__':
    es = Elasticsearch(["http://localhost:9200"], http_auth = ('root', 'Renke09076029'), verify_certs=False)

    indexs = es.indices.get(index="*")
    print(indexs)