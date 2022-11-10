import json
import os
import time

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

# TODO: Completed
# Load your ML model and assign to variable `model`
# See https://drive.google.com/file/d/1ADuBSE4z2ZVIdn66YDSwxKv-58U7WEOn/view?usp=sharing
# for more information about how to use this model.
model = xgb.XGBClassifier()
model.load_model('./best_model.txt')


def predict(image_name):
    """
    Load image from the corresponding folder based on the image name
    received, then, run our ML model to get predictions.

    Parameters
    ----------
    image_name : str
        Image filename.

    Returns
    -------
    class_name, pred_probability : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
    # TODO: Completed
    # Load image from 'uploads' folder
    img = image.load_img(os.path.join(settings.UPLOAD_FOLDER, image_name),
                         target_size=(224, 224))

    # Convert image to array
    x = image.img_to_array(img)

    # Add extra dimension due to the presence of one only image
    x_batch = np.expand_dims(x, axis=0)
    x_batch = preprocess_input(x_batch)
    # Make predictions
    preds = model.predict(x_batch)

    # Store top=1 prediction
    top_pred = decode_predictions(preds, top=1)[0][0]

    # Get class name and its probability
    class_name = top_pred[1]
    pred_probability = round(top_pred[2], 4)

    return None


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
        # Inside this loop you should add the code to:
        #   1. Take a new job from Redis
        #   2. Run your ML model on the given data
        #   3. Store model prediction in a dict with the following shape:
        #      {
        #         "prediction": str,
        #         "score": float,
        #      }
        #   4. Store the results on Redis using the original job ID as the key
        #      so the API can match the results it gets to the original job
        #      sent
        # Hint: You should be able to successfully implement the communication
        #       code with Redis making use of functions `brpop()` and `set()`.
        # TODO: Completed
        # Get job data
        job_data = json.loads(db.brpop(settings.REDIS_QUEUE)[1].decode('utf-8'))

        # Run analysis over that image
        pred, score = predict(job_data['image_name'])
        model_pred = {
            "prediction": pred,
            "score": round(float(score), 4)
        }
        # Store prediction to Redis
        db.set(name=job_data['id'], value=json.dumps(model_pred))

        # Don't forget to sleep for a bit at the end
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    #classify_process()

