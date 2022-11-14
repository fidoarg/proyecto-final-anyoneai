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

# TODO: Completed
# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(
    host=settings.REDIS_IP,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB_ID,
)

# Load preprocessor object
preprocessor = joblib.load('./preprocessor.pkl')

# Load your ML model and assign to variable `model`
model = xgb.XGBClassifier()
model.load_model('./best_model.txt')


def predict(data):
    """
    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.

    Parameters
    ----------
    data : str
        Image filename.

    Returns
    -------
    class_name, pred_probability : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
    # Cast data dict to a pandas Dataframe
    data_df = pd.DataFrame(data=data, index=[0])
    # Preprocess data
    data_processed = preprocessor.transform(data_df)

    # Make predictions
    pred  = model.predict(data_processed)[0]
    proba = model.predict_proba(data_processed)[0, 0]

    # Get class name and its probability


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

        # Run analysis over that image
        pred, score = predict(job_data["data"])
        model_pred = {
            "prediction": int(pred),
            "score": int(round(score * 1000))
        }
        # Store prediction to Redis
        db.set(name=job_data['id'], value=json.dumps(model_pred))

        # Don't forget to sleep for a bit at the end
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process()

