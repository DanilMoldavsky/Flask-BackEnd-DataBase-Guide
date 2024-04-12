from elasticsearch import Elasticsearch, helpers
import csv

es = Elasticsearch(hosts='http://127.0.0.1:9200')

with open('cities.csv', 'r') as f:
    reader = csv.DictReader(f)
    helpers.bulk(es, reader, index='city')
    
resp = es.search(
    index="city",
    query={
        "match":{
            "name": "Petersburg",
        }
    }
)

print(resp)
print(type(resp))
print(resp.body)