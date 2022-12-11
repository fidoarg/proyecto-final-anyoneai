import json
import time
from uuid import uuid4

import redis
import settings


# Connect to Redis
db = redis.Redis(
    host=settings.REDIS_IP,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB_ID,
)


def model_predict(data):
    """
    Receives a credit application queues the job into Redis.
    Will loop until getting the answer from the ML service.

    Parameters
    ----------
    data : Dict
        Data given by the user.

    Returns
    -------
    prediction, score : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """

    # Assign an unique ID for this job
    job_id = str(uuid4())

    # Create a dict with the job data
    job_data = {
        "id": job_id,
        "data": data,
    }

    # Send the job to the model service using Redis
    db.lpush(settings.REDIS_QUEUE, json.dumps(job_data))

    # Loop until we received the response from our ML model
    while True:
        # If key exists, store the results
        if db.exists(job_id):
            output = json.loads(db.get(job_id).decode('utf-8'))
            prediction = output['prediction']
            score = output['score']

        # Delete job
            db.delete(job_id)
            break

        # Sleep some time waiting for model results
        time.sleep(settings.API_SLEEP)

    return prediction, score
