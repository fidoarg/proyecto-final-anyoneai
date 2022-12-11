import json
import os
import time
import joblib
import sklearn

import pandas as pd
import numpy as np
import redis
import xgboost as xgb
import settings


# Connect to Redis
db = redis.Redis(
    host=settings.REDIS_IP,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB_ID,
)

# Load preprocessor object
preprocessor = joblib.load('./preprocessor.pkl')
# Read the numerical and categorical features txt files
num_features = []
with open('./numerical_features_names.txt', 'r') as f:
    for line in f:
        # Read line by line and append top empty list
        num_features.append(line.split('\n')[0])

cat_features = []
with open('./categorical_features_names.txt', 'r') as f:
    for line in f:
        # Read line by line and append top empty list
        cat_features.append(line.split('\n')[0])

# Load ML model
model = xgb.XGBClassifier()
model.load_model('./best_model.txt')

def predict(data):
    """
    Load dictionary with the application data received from redis, then, run our
    ML model to get predictions.

    Parameters
    ----------
    data : Dict
        Applicant Data.

    Returns
    -------
    class_name, pred_probability : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """

    # Cast data dict to a pandas Dataframe
    data_df = pd.DataFrame(data=data, index=[0])

    # Preprocess data
    data_df = data_df.convert_dtypes()
    # Use the lists with categorical and numerical feature names
    for col in cat_features:
        # First to string
        data_df[col] = data_df[col].astype('string')
        data_df[col] = pd.Categorical(data_df[col])

    # As Pandas could introduce pd.NA values in some features when converting
    # them to categorical, let's replace them with np.nan by casting
    # int columns to float32
    cols_to_float = data_df.select_dtypes(include='int').columns
    data_df[cols_to_float] = data_df[cols_to_float].astype(dtype='float32')

    data_processed = preprocessor.transform(data_df)

    # Make predictions
    pred  = model.predict(data_processed)[0]
    proba = model.predict_proba(data_processed)[0, 0]


    return pred, proba


def classify_process():
    """
    Loop indefinitely asking Redis for new jobs.
    When a new job arrives, takes it from the Redis queue, uses the loaded ML
    model to get predictions and stores the results back in Redis using
    the original job ID so other services can see it was processed and access
    the results.

    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.
    """
    while True:
        # Get job data
        job_data = json.loads(db.brpop(settings.REDIS_QUEUE)[1].decode('utf-8'))

        # Run analysis over the application data
        pred, score = predict(job_data["data"])
        model_pred = {
            "prediction": int(pred),
            "score": int(round(score * 1000))
        }
        # Store prediction to Redis
        db.set(name=job_data['id'], value=json.dumps(model_pred))

        # Little sleep on server
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()

