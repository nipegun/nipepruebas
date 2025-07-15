docker-compose up --build --remove-orphans -d
docker exec -it n8n /usr/bin/python3.12 /opt/social-api.py
