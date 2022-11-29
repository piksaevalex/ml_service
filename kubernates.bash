#!/bin/bash

#minikube start

kubectl apply -f kube/postgres/pg-config.yaml
kubectl apply -f kube/postgres/pg-storage.yaml
kubectl apply -f kube/postgres/pg-deploy.yaml
kubectl apply -f kube/postgres/pg-ip-service.yaml
kubectl apply -f kube/ml-service.yaml
kubectl apply -f kube/ml-service-ip.yaml
kubectl apply -f kube/ml-service-lb.yaml

# wait service started
sleep 15

minikube service ml-service-lb
