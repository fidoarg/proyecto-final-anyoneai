import json
import os
import time

import joblib
import pandas as pd
import numpy as np
import redis
import settings

# TODO
# Connect to Redis and assign to variable `db``
# Make use of settings.py module to get Redis settings like host, port, etc.
db = redis.Redis(
    host=settings.REDIS_IP ,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB_ID
)

# TODO
# Load your ML model and assign to variable `model`
# See https://drive.google.com/file/d/1ADuBSE4z2ZVIdn66YDSwxKv-58U7WEOn/view?usp=sharing
# for more information about how to use this model.
#model = resnet50.ResNet50(include_top=True, weights="imagenet")
model = joblib.load('./baseline_RFClassifier.pkl')
#model = model.best_estimator_
preprocessor_loaded = joblib.load('./preprocessor.pkl')


# Read training data
data_test_aux = pd.read_csv('./tests/X_test_api.csv', index_col=0)

def predict(data):
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
    class_name = None
    pred_probability = None

    # TODO
    #path=os.path.join(settings.UPLOAD_FOLDER, image_name)
    #img = image.load_img(path, target_size=(224, 224))

    data_pre = preprocessor_loaded.transform(X=data)

    # We need to convert the PIL image to a Numpy
    # array before sending it to the model
    #x = image.img_to_array(img)

    # Also we must add an extra dimension to this array
    # because our model is expecting as input a batch of images.
    # In this particular case, we will have a batch with a single
    # image inside
    #x_batch = np.expand_dims(x, axis=0)

    # Now we must scale pixels values
    #x_batch = resnet50.preprocess_input(x_batch)

    # Run model on batch of images
    #preds = model.predict(x_batch)
    preds = model.predict(data_pre)[0]
    proba = model.predict_proba(data_pre)[0,0]

    # We can get and print the predicted label
    # with the highest probability
    #pred = resnet50.decode_predictions(preds, top=1)



    return preds, proba


def classify_process(data_test_aux):
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
        q = db.brpop(settings.REDIS_QUEUE)[1]
        #   2. Run your ML model on the given data
        data_test = json.loads(q.decode("utf-8"))
        
        
        
        #class_name, pred_probability = predict(q["image_name"])
        class_name, pred_probability = predict(data_test_aux)
        
        #   3. Store model prediction in a dict with the following shape:
        #      {
        #         "prediction": str,
        #         "score": float,
        #      }
        pred = {
            "prediction": int(class_name),
            "score": int(round(pred_probability*1000)),
        }
        #   4. Store the results on Redis using the original job ID as the key
        #      so the API can match the results it gets to the original job
        #      sent
        # Hint: You should be able to successfully implement the communication
        #       code with Redis making use of functions `brpop()` and `set()`.
        # TODO
        job_id = data_test["id"]
        db.set(job_id, json.dumps(pred))   

        # Don't forget to sleep for a bit at the end
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    # Now launch process
    print("Launching ML service...")
    classify_process(data_test_aux)
