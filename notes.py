#cmd
enter_redis = 'redis-cli'
delete_allcash_redis = 'flushall'
postgres_to_csv = "\COPY city TO 'cities.csv' CSV HEADER"
docker_elastic_server = 'docker run --rm -p 9200:9200 -e "xpack.security.enabled=false" -e "discovery.type=single-node" elasticsearch:8.10.2'