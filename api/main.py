import uvicorn
import json

# Fast API utilities
from fastapi import FastAPI, Request, Query, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Function to send and receive ml jobs
from middleware import model_predict

# Pydantic utilities
from pydantic import BaseModel, Field

# Create API
app = FastAPI()

#app.mount("/static", StaticFiles(directory="static"), name="static")

# Define templates directory
templates = Jinja2Templates(directory="templates")

#%% Models

# Application
class Application(BaseModel):
    sex: str = Form()
    # q_cars = int = Field(...,
    #                      ge=0)

@app.get("/application", response_class=HTMLResponse)
#@app.post("/application", response_class=HTMLResponse)
async def application(request: Request,
                ):

    # if request.method == "GET":
    return templates.TemplateResponse(name="index.html",
                                      context={
                                      "request": request,
                                      "genders": ["M", "F"]
                                      })

#    if request.method == "POST":
@app.post("/score", response_class=HTMLResponse)
async def score(request: Request,
                application: Application,
                ):
    data = {
        'PAYMENT_DAY': 5,
        'APPLICATION_SUBMISSION_TYPE': 'Web',
        'POSTAL_ADDRESS_TYPE': 1,
        'SEX': application.sex,
        'MARITAL_STATUS': 2,
        'QUANT_DEPENDANTS': 4,
        'STATE_OF_BIRTH': 'RJ',
        'NACIONALITY': 1,
        'RESIDENCIAL_STATE': 'RJ',
        'FLAG_RESIDENCIAL_PHONE': 'Y',
        'RESIDENCIAL_PHONE_AREA_CODE': ' ',
        'RESIDENCE_TYPE': None,
        'MONTHS_IN_RESIDENCE': 54,
        'FLAG_EMAIL': 1,
        'PERSONAL_MONTHLY_INCOME': 1200,
        'OTHER_INCOMES': 0,
        'FLAG_VISA': 1,
        'FLAG_MASTERCARD': 0,
        'FLAG_DINERS': 0,
        'FLAG_AMERICAN_EXPRESS': 0,
        'FLAG_OTHER_CARDS': 0,
        'QUANT_BANKING_ACCOUNTS': 2,
        'PERSONAL_ASSETS_VALUE': 0,
        'QUANT_CARS': 1,
        'COMPANY': 'Y',
        'PROFESSIONAL_STATE': 'RJ',
        'FLAG_PROFESSIONAL_PHONE': 'N',
        'PROFESSIONAL_PHONE_AREA_CODE': 384,
        'MONTHS_IN_THE_JOB': 40,
        'PROFESSION_CODE': 11,
        'OCCUPATION_TYPE': 1,
        'PRODUCT': 2,
        'AGE': 30,
        'RESIDENCIAL_ZIP_3': None,
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
            # return templates.TemplateResponse(name="index.html",
            #                                   context={"request":request})

        # context={
        #     "request": request,
        #     "flag_post": True,
        #     "genders": ["Male", "Female", "Non Binary"]#application.dict()["sex"],
        # }
        # return templates.TemplateResponse(name="index.html",
        #                                   context=context)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)