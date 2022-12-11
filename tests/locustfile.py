from locust import HttpUser, task, between
from utils import Data, create_access_token
from fastapi.encoders import jsonable_encoder

class APIUser(HttpUser):
    wait_time = between(2, 5)

    @task(1)
    def index_get(self):
        # Access token
        auth_token = create_access_token(sub={"username": "JhonDoe"})
        # GET Method
        self.client.get(
                '/index',
                cookies={"auth": auth_token}
        )


    @task(1)
    def score_post(self):
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
        self.client.post(
            "/score",
            data=data
        )
