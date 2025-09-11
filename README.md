# Linux Monitoring Tool

A lightweight Linux monitoring tool that collects disk usage statistics and stores them in a MySQL database. Can run as a Docker container or on Kubernetes.

## Features

- Collects disk usage data from the Linux host.
- Stores data in MySQL for historical tracking.
- Deployable as Docker containers or Kubernetes pods.
- Uses Kubernetes secrets for encrypted credentials if desired.

## Requirements

- Docker  
- Kubernetes (optional)  
- Python 3.x  
- MySQL  

## Usage

### Docker

1. Build MySQL image:

cd mysql
docker build -t my-mysql:latest .


2. Build tool image:

cd ../tool
docker build -t my-tool:latest .

3. Run MySQL container:

docker run -d --name my-mysql \
  -e MYSQL_ROOT_PASSWORD=root123 \
  -e MYSQL_DATABASE=alnafi \
  -e MYSQL_USER=mysql_user \
  -e MYSQL_PASSWORD=test123 \
  -v /home/hammad/mysql-data:/var/lib/mysql \
  -p 3306:3306 \
  my-mysql:latest

4. Run tool container:

docker run -d --name my-tool \
  --network host \
  -e MYSQL_HOST=localhost \
  -e MYSQL_DATABASE=alnafi \
  -e MYSQL_USER=mysql_user \
  -e MYSQL_PASSWORD=test123 \
  my-tool:latest

## Kubernetes

1. Apply MySQL deployment and service:

kubectl apply -f k8s/mysql-deployment.yaml
kubectl apply -f k8s/mysql-service.yaml

2. Apply tool deployment and secret/configmap:

kubectl apply -f k8s/tool-secret.yaml
kubectl apply -f k8s/tool-configmap.yaml
kubectl apply -f k8s/tool-deployment.yaml

3. Check pods and logs:

kubectl get pods
kubectl logs -f <tool-pod-name>

## Data Storage
MySQL data is persisted in /home/hammad/mysql-data on host or via a Kubernetes PersistentVolume.
Table: my_df_data

## Contributing
Feel free to open issues or submit pull requests.

## License
MIT License