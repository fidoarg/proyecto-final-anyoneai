import json
from unittest import TestCase
from fastapi.testclient import TestClient


from main import app

# app = main.app

class TestIntegration(TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_score_bad_parameters(self):
        response = self.client.post(
            "/score",
            data=json.dumps({"not_a_form": "empty"}),
        )
        self.assertEqual(response.status_code, 422)

    def test_score_ok(self):
        # Mocks
        pred_class = 1
        pred_score = 0.9346
        response = self.client.post(
            "/predict",
            data=data,
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data.keys()), 3)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["prediction"], pred_class)
        self.assertAlmostEqual(data["score"], pred_score, 5)

    # def test_feedback(self):
    #     import os
    #
    #     import settings
    #
    #     # Check current status for feedback folder
    #     if os.path.exists(settings.FEEDBACK_FILEPATH):
    #         curr_feedback_lines = len(
    #             open(settings.FEEDBACK_FILEPATH).read().splitlines()
    #         )
    #     else:
    #         curr_feedback_lines = 0
    #
    #     data = {
    #         "report": "{'filename': 'test', 'prediction': 'test-pred', 'score': 1. }"
    #     }
    #     response = self.client.post(
    #         "/feedback",
    #         data=data,
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(os.path.exists(settings.FEEDBACK_FILEPATH))
    #
    #     # Check the feedback file was written
    #     new_feedback_lines = len(open(settings.FEEDBACK_FILEPATH).read().splitlines())
    #     self.assertEqual(curr_feedback_lines + 1, new_feedback_lines)
    #
    #     # Check the content is correct
    #     new_line = open(settings.FEEDBACK_FILEPATH).read().splitlines()[-1]
    #     self.assertEqual(data["report"], new_line)


class TestEndpointsAvailability(TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_application(self):
        response = self.client.get("/application")
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/application")
        # Method not allowed
        self.assertEqual(response.status_code, 405)


    def test_score(self):
        response = self.client.get("/score")
        # Method not allowed
        self.assertEqual(response.status_code, 405)
        response = self.client.post("/score")
        # Bad args
        self.assertEqual(response.status_code, 422)

    # def test_feedback(self):
    #     response = self.client.get("/feedback")
    #     self.assertEqual(response.status_code, 200)
    #     response = self.client.post("/feedback")
    #     self.assertEqual(response.status_code, 200)
