import json
import os

import settings
import utils
from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from middleware import model_predict

router = Blueprint("app_router", __name__, template_folder="templates")


@router.route("/", methods=["GET", "POST"])
def index():
    """
    GET: Index endpoint, renders our HTML code.

    POST: Used in our frontend so we can upload and show an image.
    When it receives an image from the UI, it also calls our ML model to
    get and display the predictions.
    """
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        # No file received, show basic UI
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        # File received but no filename is provided, show basic UI
        file = request.files["file"]
        if file.filename == "":
            flash("No image selected for uploading")
            return redirect(request.url)

        # File received and if it's an image, we must show it and get predictions
        if file and utils.allowed_file(file.filename):
            # In order to correctly display the image in the UI and get model
            # predictions you should implement the following:
            #   1. Get an unique file name using utils.get_file_hash() function
            #   2. Store the image to disk using the new name
            #   3. Send the file to be processed by the `model` service
            #      Hint: Use middleware.model_predict() for sending jobs to model
            #            service using Redis.
            #   4. Update `context` dict with the corresponding values
            # TODO: Completed

            # Get hashed name
            file_name = utils.get_file_hash(file)

            # Store file in disk
            file.save(os.path.join(settings.UPLOAD_FOLDER, file_name))

            # Send file to model to get prediction

            prediction, score = model_predict(file_name)
            context = {
                "prediction": prediction.replace('_', ' ').upper(),
                "score": str(round(score*100, 4)),
                "filename": file_name,
            }
            # Update `render_template()` parameters as needed
            # TODO: Completed
            return render_template(
                "index.html",
                filename=file_name,
                context=context)
        # File received but it isn't an image
        else:
            flash("Allowed image types are -> png, jpg, jpeg, gif")
            return redirect(request.url)


@router.route("/display/<filename>")
def display_image(filename):
    """
    Display uploaded image in our UI.
    """
    return redirect(url_for("static", filename="uploads/" + filename), code=301)


# noinspection DuplicatedCode
@router.route("/predict", methods=["POST"])
def predict():
    """
    Endpoint used to get predictions without need to access the UI.

    Parameters
    ----------
    file : str
        Input image we want to get predictions from.

    Returns
    -------
    flask.Response
        JSON response from our API having the following format:
            {
                "success": bool,
                "prediction": str,
                "score": float,
            }

        - "success" will be True if the input file is valid and we get a
          prediction from our ML model.
        - "prediction" model predicted class as string.
        - "score" model confidence score for the predicted class as float.
    """
    # To correctly implement this endpoint you should:
    #   1. Check a file was sent and that file is an image
    #   2. Store the image to disk
    #   3. Send the file to be processed by the `model` service
    #      Hint: Use middleware.model_predict() for sending jobs to model
    #            service using Redis.
    #   4. Update and return `rpse` dict with the corresponding values
    # If user sends an invalid request (e.g. no file provided) this endpoint
    # should return `rpse` dict with default values HTTP 400 Bad Request code
    # TODO: Completed
    # Check if it is a file to work with
    rpse = {"success": False, "prediction": None, "score": None}

    if "file" not in request.files:
        response = current_app.make_response((rpse, 400))
        return response
    # Check the file has name
    file = request.files["file"]
    if file.filename == "":
        response = current_app.make_response((rpse, 400))
        return response
    # Check if file is an image
    if utils.allowed_file(file.filename):
        # Get hashed name
        file_name = utils.get_file_hash(file)
        # Store file in disk
        file.save(os.path.join(settings.UPLOAD_FOLDER, file_name))
        # Send file to model to get prediction
        prediction, score = model_predict(file_name)
        rpse.update(
            {
                "success": True,
                "prediction": prediction,
                "score": float(score),
            })
        # Update `render_template()` parameters
        return rpse
        # File received but it isn't an image
    else:
        response = current_app.make_response((rpse, 400))
        return response


@router.route("/feedback", methods=["GET", "POST"])
def feedback():
    """
    Store feedback from users about wrong predictions on a plain text file.

    Parameters
    ----------
    report : request.form
        Feedback given by the user with the following JSON format:
            {
                "filename": str,
                "prediction": str,
                "score": float
            }

        - "filename" corresponds to the image used stored in the uploads
          folder.
        - "prediction" is the model predicted class as string reported as
          incorrect.
        - "score" model confidence score for the predicted class as float.
    """

    # Store the reported data to a file on the corresponding path
    # already provided in settings.py module
    # TODO: Completed
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        report = request.form.get("report")
        # Check something was sent
        if report is None:
            return current_app.make_response(
                (
                    {
                        'message': 'No file was passed in the POST request'
                    },
                    200
                )
            )

        else:
            with open(settings.FEEDBACK_FILEPATH, 'a') as f:
                f.write(report+'\n')

            # PART 3 of Project
            # Define feedback path
            csv_path = settings.FEEDBACK_FILEPATH + '.csv'
            # Cast the 'report' string into a dict. '.replace' method used for
            # avoiding errors from data that comes from index.html template.
            # This section will handle a unique problem that raises with the
            # due to the information given by the test cause the notation for
            # number types on a JSON structure should never be like '1.'. this
            # notation is not allowed in JSON format but the test gave the Score
            # that way, so we have to handle it somehow.

            if report[report.find('.') + 1] == ' ':  # If the format is 'n.'
                aux = report.find('.')
                # Since python strings are immutable we will redefine the
                # variable report
                report = report[:aux + 1] + '0' + report[aux + 1:]

            csv_data = json.loads(report.replace("'", '"'))
            csv_data = csv_data['filename'] + ',' \
                     + csv_data['prediction'] + ',' \
                     + str(csv_data['score']) + '\n'
            headers = 'file,prediction,score'+'\n'

            if os.path.exists(csv_path):
                with open(csv_path, 'a') as csv:
                    csv.write(csv_data)

            else:
                with open(csv_path, 'w+') as csv:
                    csv.writelines([
                        headers,
                        csv_data
                    ])

            return render_template('index.html')
