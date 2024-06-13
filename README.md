Dockerfile
  ```sh
Le Dockerfile pour créer l'image Docker de l'application.

## Utiliser l'image de base Python
FROM python:3.11-slim

## Définir le répertoire de travail dans le conteneur
WORKDIR /app

## Copier les fichiers locaux main.py et requirements.txt dans le répertoire du conteneur /app
COPY main.py requirements.txt /app/

## Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

## Exposer le port 8000 vers l'extérieur
EXPOSE 8000

## Commande pour exécuter l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
  ```
Main.py

  ```sh
from fastapi import FastAPI
import redis
import os

app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
redis_client = redis.StrictRedis(host=REDIS_HOST, port=6379, db=0)

@app.get("/")
def status():
    return {"status": "OK"}

@app.get("/get_data_from_redis/{key}")
def read_item(key: str):
    value = redis_client.get(key)
    if value:
        return {"key": key, "value": value.decode('utf-8')}
    else:
        return {"key": key, "value": "Key not found"}

@app.post("/set_item/{key}/{value}")
def set_item(key: str, value: str):
    redis_client.set(key, value)
    return {"message": "Item set successfully", "key": key, "value": value}
  ```

requierement.txt

  ```sh
fastapi==0.95
redis==5.0.1
uvicorn==0.24.0
  ```

fastapi-deployment.yaml

  ```sh
fastapi-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-redis-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: fastapi-redis
  template:
    metadata:
      labels:
        app: fastapi-redis
    spec:
      containers:
      - name: fastapi-redis
        image: kl8n/python-redis:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "128Mi"
            cpu: "500m"
        readinessProbe:
          httpGet:
            path: /
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
        livenessProbe:
          httpGet:
            path: /
            port: 8000
          initialDelaySeconds: 15
          periodSeconds: 20
---
apiVersion: v1
kind: Service
metadata:
  name: fastapi-redis-service
spec:
  selector:
    app: fastapi-redis
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
  type: ClusterIP
  ```

redis-deployment.yaml

  ```sh
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:alpine
        ports:
        - containerPort: 6379
---
apiVersion: v1
kind: Service
metadata:
  name: redis-service
spec:
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379
  type: ClusterIP
  ```

fastapi-redis-service.yaml

  ```sh
apiVersion: v1
kind: Service
metadata:
  name: fastapi-redis-service
spec:
  selector:
    app: fastapi-redis
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
  type: ClusterIP
  ```
