import uvicorn
import json

# Fast API utilities
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Function to send and receive ml jobs
from middleware import model_predict

# Pydantic utilities
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

# Create API
app = FastAPI(title="Credit Risk Analysis API",
              description="Final Project of the Machine Learning Engineer Program",
              version="1.0.1")

# Define public directory
app.mount("/static",StaticFiles(directory="./public/static"), name="static")

# Define templates directory
templates = Jinja2Templates(directory="./public/templates")

# Opening JSON file
f = open('./public/static/json/index_attr.json')

# returns JSON object as
# a dictionary
data_index_attr = json.load(f)

#%% Models


# Application
@dataclass
class Data:
    sex: str = Form(...)
    company: str = Form(...)
    payment_day: str = Form(...)
    application_submission_type: str = Form(...)
    postal_address_type: str = Form(...)
    marital_status: str = Form(...)
    quant_dependants: int = Form(...)
    state_of_birth: str = Form(...)
    nacionality: str = Form(...)
    residencial_state: str = Form(...)
    residencial_phone_area_code: str = Form(...)
    flag_residencial_phone: str = Form(...)
    residence_type: str = Form(...)
    months_in_residence: str = Form(...)
    flag_email: str = Form(...)
    personal_monthly_income: str = Form(...)
    other_incomes: str = Form(...)
    flag_visa: str = Form(...)
    flag_mastercard: str = Form(...)
    flag_diners: str = Form(...)
    flag_american_express: str = Form(...)
    flag_other_cards: str = Form(...)
    quant_banking_accounts: str = Form(...)
    personal_assets_value: str = Form(...)
    quant_cars: str = Form(...)
    professional_state: str = Form(...)
    flag_professional_phone: str = Form(...)
    professional_phone_area_code: str = Form(...)
    months_in_the_job: str = Form(...)
    # profession_code: str = Form(...)
    # occupation_type: str = Form(...)
    # product: str = Form(...)
    age: str = Form(...)
    residencial_zip_3: str = Form(...)

@app.get("/index", response_class=HTMLResponse)
async def index(request: Request,):

    context = {
        "request": request,
        "genders": data_index_attr['sex'],
        "company": data_index_attr['company'],
        "payment_day": data_index_attr['payment_day'],
        "postal_address_type": data_index_attr['postal_address_type'],
        "marital_status": data_index_attr['marital_status'],
        "state_of_birth": data_index_attr['state_of_birth'],
        "nacionality": data_index_attr['nacionality'],
        "residencial_state": data_index_attr['residencial_state'],
        "residence_type": data_index_attr['residence_type'],
        "flag_email": data_index_attr['flag_email'],
        "professional_state": data_index_attr['professional_state'],
        "profession_code": data_index_attr['profession_code'],
        "occupation_type": data_index_attr['occupation_type'],
        "product": data_index_attr['product'],
    }


    return templates.TemplateResponse(name="index.html",
                                      context=context)


@app.post("/score")#, response_class=HTMLResponse)
async def score(request: Request,
                form_data: Data = Depends(),
                ):


    data = {
        'PAYMENT_DAY': form_data.payment_day,
        'APPLICATION_SUBMISSION_TYPE': form_data.application_submission_type,
        'POSTAL_ADDRESS_TYPE': form_data.postal_address_type,
        'SEX': form_data.sex,
        'MARITAL_STATUS': form_data.marital_status,
        'QUANT_DEPENDANTS': form_data.quant_dependants,
        'STATE_OF_BIRTH': form_data.state_of_birth,
        'NACIONALITY': form_data.nacionality,
        'RESIDENCIAL_STATE': form_data.residencial_state,
        'FLAG_RESIDENCIAL_PHONE': form_data.flag_residencial_phone,
        'RESIDENCIAL_PHONE_AREA_CODE': form_data.residencial_phone_area_code,
        'RESIDENCE_TYPE': form_data.residence_type,
        'MONTHS_IN_RESIDENCE': form_data.months_in_residence,
        'FLAG_EMAIL': form_data.flag_email,
        'PERSONAL_MONTHLY_INCOME': form_data.personal_monthly_income,
        'OTHER_INCOMES': form_data.other_incomes,
        'FLAG_VISA': form_data.flag_visa,
        'FLAG_MASTERCARD': form_data.flag_mastercard,
        'FLAG_DINERS': form_data.flag_diners,
        'FLAG_AMERICAN_EXPRESS': form_data.flag_american_express,
        'FLAG_OTHER_CARDS': form_data.flag_other_cards,
        'QUANT_BANKING_ACCOUNTS': form_data.quant_banking_accounts,
        'PERSONAL_ASSETS_VALUE': form_data.personal_assets_value,
        'QUANT_CARS': form_data.quant_cars,
        'COMPANY': form_data.company,
        'PROFESSIONAL_STATE': form_data.professional_state,
        'FLAG_PROFESSIONAL_PHONE': form_data.flag_professional_phone,
        'PROFESSIONAL_PHONE_AREA_CODE': form_data.professional_phone_area_code,
        'MONTHS_IN_THE_JOB': form_data.months_in_the_job,
        # 'PROFESSION_CODE': form_data.profession_code,
        # 'OCCUPATION_TYPE': form_data.occupation_type,
        # 'PRODUCT': form_data.product,
        'PROFESSION_CODE': None,
        'OCCUPATION_TYPE': None,
        'PRODUCT': None,
        'AGE': form_data.age,
        'RESIDENCIAL_ZIP_3': form_data.residencial_zip_3,
    }

    # Send job to ml_service and receive results
    prediction, score = model_predict(data)
    context = {
        "request": request,
        "prediction": prediction,
        "score": score
    }

    # return {"Prediction": prediction, "Score": score}
    return templates.TemplateResponse(name="score.html",
                                      context=context
                                      )

# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)