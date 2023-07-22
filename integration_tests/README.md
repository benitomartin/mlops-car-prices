 ## With Only Docker Image
 
 docker build -t my-app .

 docker run --rm -p 9696:9696 -v C:\Users\bmart\OneDrive\11_MLOps\mlops-car-prices\data:/app/data --name my-app my-app

 docker exec -it my-app pytest test_integration.py


## With docker-compose.yml

docker build -t my-app .

docker-compose up -d or docker-compose up --build

integration_tests-my-app-1 is the name shown after running docker-compose up -d. Change it accordingly

docker exec -it integration_tests-my-app-1 pytest test_integration.py

docker-compose down or docker-compose down --volumes
