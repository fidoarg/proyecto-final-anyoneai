## Anyone-ai final project - Group 5
# Credit risk analysis using Deep Learning

### This project consists of a series of Main Deliverables:
1. Exploratory Dataset Analysis (EDA) Jupyter notebooks and dataset
2. Scripts used for data pre-processing and data preparation
3. Training scripts and trained models. Description of how to reproduce results
4. The model trained for a credit score prediction
5. API with a basic UI interface for demo (upload user's transactional data and return a score prediction)
6. Everything must be Dockerized and ready to be deployed to AWS

### And Additional Optional Deliverables:
- Service should be properly secured with token-based authentication
- Ability to retrain the model "online" with new data added by users

### This project will be approach by this milestone plan: 
|Milestones | Description |
| ----------- | ----------- |
| Setup repository and project structure | Access Github repo. Organize the project, create sub-folders, and prep/mock as much project structure necessary for the final project deliverables. Prepare the AWS server for dataset evaluation. |
| Download and evaluate the dataset. Normalize data | Download data and start with EDA over our dataset. Get metrics about categorical and numerical columns, compute percentiles, max, min, mean, median, and NaN values. If nan values are found, decide about the criteria to handle them. Normalize input and encapsulate all cleaning steps into a preprocessing function/script.  
| Create a training dataset | Create a database and save cleaned data. |
| Credit Score Classifier model training | Evaluate different classifiers such as LightGBM, Xgboost, Catboot, RandomForest, Ensemble, and stacked variants. Additionally, train an MLP classifier. |
| Evaluate/test initial classifier | Compare performance (accuracy, AUC, training time, inference time, etc) of previous classifiers vs MLP classifiers using cleaned data. Choose the best model according to experiments prioritizing AUC and inference time. |
| Setup an API for Credit Risk Classification | It’s time to put the model into production. Our goal is to build an API service as we did for Sprint 4 so we make this model accessible to other components. Although not mandatory, instead of Flask, this time you can use FastAPI (one of the most used frameworks to deploy ML models these days). The API should be containerized using Docker. |
| Integrate a basic UI and secure the API | Create a basic UI that can drive the API service and allow the user to submit the "credit application" data and get a prediction as a result. It should have a web UI for making demos but also an endpoint so others can use our API to interact with our model and integrate it with third-party services. |
| Fine-tune model / Train additional models | After the evaluation of the initial classifier, accuracy can be improved. Keep training more models and see if you can improve the baseline accuracy. |
| Add API tests (Optional) | You should add some tests to the API main components. |
| Preview service to other teams | Demo the project to other teams and gather their feedback for final adjustments |
| Build final presentation and prep for demo | Build your presentation and prepare your project for the Demo Day |

### Directories:
The project its distributed in the following folders:
- data: no presented in the github, contains the dataset files.
- notebooks: contains the notebooks for EDA, Feature Enginering and Models.