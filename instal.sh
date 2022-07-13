docker-compose up -d db_pgsql_master_auth db_pgsql_replica_service
docker-compose run master_auth ./manage.py makemigrations
docker-compose run master_auth ./manage.py migrate
docker-compose run replica_service ./manage.py makemigrations
docker-compose run replica_service ./manage.py migrate
docker-compose up -d
docker-compose run master_auth ./manage.py cqrs_sync --cqrs-id=user -f={}
docker-compose run master_auth ./manage.py cqrs_sync --cqrs-id=group -f={}