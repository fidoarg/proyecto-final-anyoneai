
# Interact with OS
import os

# Fast API utilities
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Function to send and receive ml jobs
from middleware import model_predict

# Pydantic utilities
from pydantic.dataclasses import dataclass

# Authentication and encryption utilities
from routers import auth
from jose import jwt
JWT_SECRET_KEY= os.environ['JWT_SECRET_KEY']
ALGORITHM= os.environ['ALGORITHM']

# Others
from typing import Optional
import json

# Create API
app = FastAPI(title="Credit Risk Analysis API",
              description="Final Project of the Machine Learning Engineer Program",
              version="1.0.1")

# Include authentication router
app.include_router(auth.router)

# Define public directory
app.mount("/static",StaticFiles(directory="./public/static"), name="static")

# Define templates directory
templates = Jinja2Templates(directory="./public/templates")

# Opening JSON file
f = open('./public/static/json/index_attr.json')

# Returns JSON object as a dictionary
data_index_attr = json.load(f)

#%% Models


# Application Form Data Class
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
    age: str = Form(...)
    residencial_zip_3: str = Form(...)
    first_name: Optional[str] = Form()
    last_name: Optional[str] = Form()

# Endpoint to avoid 
@app.get("/")
async def redirect():
    response = RedirectResponse(url="/auth")
    return response


@app.post("/index", response_class=HTMLResponse)
@app.get("/index", response_class=HTMLResponse)
async def index(request: Request = Depends(auth.verify_user_token)):

    # Verify that the user is logged in by means of token
    token= request.cookies.get('auth')
    decoded_token= jwt.decode(
        token= token,
        key= JWT_SECRET_KEY,
        algorithms= [ALGORITHM]
    # If it is not logged in, it redirects the user to an error message
    ) if token is not None else None

    user= json.loads(decoded_token.get('sub').replace("\'", "\"")) if decoded_token is not None else decoded_token

    # The data set is loaded from the json dictionary to be sent by get a registration form
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
        "user_data": user
    }

    # It is redirected to the registration form
    return templates.TemplateResponse(name="index.html",
                                      context=context)

# Post method published to obtain the data from the registration form and send it to the model service
@app.post("/score")#, response_class=HTMLResponse)
async def score(request: Request,
                form_data: Data = Depends(),
                ):

    # The data is assembled to be sent in json format to the ml_service
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
        'PROFESSION_CODE': None,
        'OCCUPATION_TYPE': None,
        'PRODUCT': None,
        'AGE': form_data.age,
        'RESIDENCIAL_ZIP_3': form_data.residencial_zip_3,
    }

    # Send job to ml_service and receive results
    prediction, score = model_predict(data)

    # The calculated score range is checked to select the correct color to plot
    if 0 <= score <= 846: 
        color = "#F50B0B"
        type_client = "Very Low"
    if 847 <= score <= 926: 
        color = "#D25C5C" 
        type_client = "Bass"
    if 927 <= score <= 950: 
        color = "#FFFF33" 
        type_client = "Regular"
    if 951 <= score <= 972: 
        color = "#99FF99" 
        type_client = "Okay"
    if 973 <= score <= 1000: 
        color = "#00CCCC" 
        type_client = "Excellent"

    # Formatting of data to be sent to the score form
    context = {
        "request": request,
        "prediction": prediction,
        "score": score/10,
        "first_name":form_data.first_name,
        "last_name":form_data.last_name,
        "color": color        
    }

    # It is redirected to graph the score obtained by the applicant
    return templates.TemplateResponse(name="score.html",
                                      context=context
                                      )