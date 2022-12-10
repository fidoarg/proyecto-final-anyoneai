
# Credit risk analysis using Deep Learning

## Description
The main objective of this project is  to build a service capable of predicting the credit scores of people based on financial transactional information. 

### Technology Stack
- Python3
- Scikit-learn
- FastAPI
- Redis
- JavaScript
- JinJa2
- HTML/CSS
- Docker
- Pytest
- Locust
- SQLite
- Keras
- Pytorch-Lightning
- Optuna

## How to Install and Run the Project
1. Install Docker
2. Download and extract the repository
3. Build and run using the following command:
```bash
$ docker-compose up --build
```
> You can set a different port for the project in the docker-compose.yml file

## How to use:
1. In a browser go to `localhost:80`, or the port you assigned to the project.
2. Sign Up or sign in if you already have an account.
3. Fill the form with the required data and request a credit.
4. Your score will be displayed.


### Run Pytest tests
1. Install the requirements:
```bash
$ pip install -r tests/requirements.txt
```
2. from the project root folder run:
```bash
$ python tests/test_integration.py
```
3. Run API module test:
```bash
$ cd api/
$ docker build -t fastapi_api_test --progress=plain --target test .
```
4. Run API module test:
```bash
$ cd model/
$ docker build -t model_test --progress=plain --target test .
```