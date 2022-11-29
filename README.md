# ML Service

### Обязательные действия перед запуском 
или не такие уж и обязательные

- создай в корне проекта папку `secrets`;
- создай файл `ml_service_db_password` без расширения с паролем от БД (`postgres`).

## Способы запустить сервис

### 1. Docker
```commandline
docker-compose up -d
```
если образ автоматически не стянулся, то можно стянуть вручную
```commandline
docker pull digibro/ml_service
```
### 2. Kubernates
Тестировался с minikube, поэтому для начала 
```commandline
minikube start
```
Конфиги описания кластера описаны в папке kube
```commandline
chmod u+x kubernates.bash
./kubernates.bash
```
### 3. CMD
#### 1. Для установки зависимостей использовать **poetry**
```commandline
poetry install
```
#### 2. Для запуска кода запустить main.py
```commandline
python3 main.py
```

## Примеры взаимодействия с сервисом

#### 1. Возвращает список доступных для обучения типов моделей  
**GET**  
> http://localhost:5000/api/v1/model_classes  

#### 2. Возвращает список обученных моделей готовых для предсказаний  
**GET**  
> http://localhost:5000/api/v1/models  

#### 3. Обучение модели  
**POST**  
> http://localhost:5000/api/v1/models/fit  
> 
body:  
```
{  
    "model_type": "Ridge",  
    "params": "{"alpha": 0.001}",  
    "x": [[0.0,0.0],[1.0,0.0],[2.0,3.0]],  
    "y": [0.0,1.0,2.0]  
}  
```

#### 4. Предсказание обученной моделью  
**POST**  
> http://localhost:5000/api/v1/models/predict  
> 
body: 
``` 
{  
    "model_name": "Ridge(alpha=0.001)",  
    "x": [[0.0,0.0],[1.0,0.0],[2.0,3.0]]  
}  
```

#### 5. Удаление обученной модели  
**DELETE**  
> http://localhost:5000/api/v1/models  
> 
body:  
```
{  
    "model_name": "Ridge(alpha=0.001)"  
}  
```
