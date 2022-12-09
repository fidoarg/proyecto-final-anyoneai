import json
from unittest import TestCase
from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder

from main import app, Data
from routers.auth import create_access_token

class TestIntegration(TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_score_bad_parameters(self):
        response = self.client.post(
            "/score",
            data=json.dumps({"not_a_form": "empty"}),
        )
        self.assertEqual(response.status_code, 422)

    @patch("main.model_predict")
    def test_score_ok(self, mock):
        # Mocks
        form_data = Data(sex="F",
                        company="N",
                        payment_day="1",
                        application_submission_type="Web",
                        postal_address_type="1",
                        marital_status="2",
                        quant_dependants=3,
                        state_of_birth="SC",
                        nacionality="1",
                        residencial_state="SC",
                        residencial_phone_area_code="50",
                        flag_residencial_phone="1",
                        residence_type="1",
                        months_in_residence="6",
                        flag_email="1",
                        personal_monthly_income="3000.0",
                        other_incomes="0.0",
                        flag_visa="0",
                        flag_mastercard="0",
                        flag_diners="0",
                        flag_american_express="0",
                        flag_other_cards="0",
                        quant_banking_accounts="0",
                        personal_assets_value="0.0",
                        quant_cars="0.0",
                        professional_state="NO_JOB",
                        flag_professional_phone="N",
                        professional_phone_area_code="NO_DATA",
                        months_in_the_job="0.0",
                        age="29.0",
                        residencial_zip_3="881",
                        first_name="Jhon",
                        last_name="Doe"
        )
        # Encode data as json so the service can understand it
        data = jsonable_encoder(form_data)
        pred_class = 1
        pred_score = 0.4770884
        mock.return_value = (pred_class, pred_score)
        response = self.client.post(
            "/score",
            data=data
        )

        self.assertEqual(response.status_code, 200)


class TestEndpointsAvailability(TestCase):
    def setUp(self):
        self.client = TestClient(app)


    def test_index(self):
        response = self.client.get(
                "/index",
                cookies={
                    "auth": create_access_token(
                            sub={"username": "JhonDoe"}
                    )
                }
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.post("/index")
        # No args == Bad Request
        self.assertEqual(response.status_code, 400)


    def test_score(self):
        response = self.client.get("/score")
        # Method not allowed
        self.assertEqual(response.status_code, 405)
        response = self.client.post("/score")
        # Bad args
        self.assertEqual(response.status_code, 422)
