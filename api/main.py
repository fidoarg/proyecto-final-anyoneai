import json

# Fast API utilities
from fastapi import FastAPI, Request, Query, Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Pydantic tilities
from pydantic import BaseModel, Field

# Create API
app = FastAPI()

#app.mount("/static", StaticFiles(directory="static"), name="static")

# Define templates directory
templates = Jinja2Templates(directory="templates")

#%% Models

# Application
class Application(BaseModel):
    sex: str = Query("Male", enum=["Male", "Female", "Non Binary"])





@app.get("/application", response_class=HTMLResponse)
@app.post("/application")#, response_class=HTMLResponse)
async def application(request: Request,
                #application: Application,
                ):

    if request.method == "GET":
        return templates.TemplateResponse(name="index.html",
                                          context={
                                          "request": request,
                                          "genders": ["Male", "Female", "Non Binary"]
                                          })

    if request.method == "POST":
        data = {
            "Age": 20,
            "Sex": "M",

        }
        return data

            # return templates.TemplateResponse(name="index.html",
            #                                   context={"request":request})

        # context={
        #     "request": request,
        #     "flag_post": True,
        #     "genders": ["Male", "Female", "Non Binary"]#application.dict()["sex"],
        # }
        # return templates.TemplateResponse(name="index.html",
        #                                   context=context)

