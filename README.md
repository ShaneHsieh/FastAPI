
# FastAPI Function




## Docker

Build and run docker

```bash
  docker compose up --build -d api db
```

Test api(use pytest) 

```bash
  docker compose up --build -d test
```

Check docker status

```bash
  docker ps
```

Check image log
```bash
  docker logs -f fastapi_app
  docker logs -f postgres_db
```

Close docker

```bash
  docker compose down
  
  #for close and delete docker volume's data
  docker compose down -v 
```
