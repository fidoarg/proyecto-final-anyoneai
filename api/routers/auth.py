import os
import json
import sqlite3

from fastapi    import APIRouter, Request, Depends, Cookie, Form, Response
from jose       import jwt
from typing     import Union, Any
from pydantic   import BaseModel
from datetime   import datetime, timedelta, date

from passlib.context        import CryptContext
from fastapi.templating     import Jinja2Templates
from fastapi.security       import OAuth2PasswordRequestForm
from fastapi.responses      import PlainTextResponse, RedirectResponse, HTMLResponse
from fastapi.exceptions     import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from pypika     import Table, Query, functions


# Fast API utilities
from fastapi import FastAPI, Request, Form, Depends

# Pydantic utilities
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

# Create API
app = FastAPI(title="Credit Risk Analysis API",
              description="Final Project of the Machine Learning Engineer Program",
              version="1.0.1")

# Define public directory
app.mount("/static",StaticFiles(directory="./public/static"), name="static")


# Opening JSON file
f = open('./public/static/json/index_attr.json')

# returns JSON object as
# a dictionary
data_index_attr = json.load(f)

# Application
@dataclass
class Data:
    username: str = Form(...)
    password: str = Form(...)    
    sex: str = Form(...)
    birth_date: str = Form(...)
    nationality: str = Form(...)
    state_of_birth: str = Form(...)
    first_name: str = Form(...)
    last_name: str = Form(...) 

users_db = dict(
    fidoaragon= {
        "username": "fidoaragon",
        "password": "$2b$12$Zo92UMElULK66o6QFcuWO.9j33hpeE.qLaRBQIL8o0jq.LEirrCja"
    }
)

router= APIRouter(
    prefix= '/auth',
    tags= ["auth"] 
)

password_context = CryptContext(
    schemes= ["bcrypt"], 
    deprecated= "auto"
)
class User(BaseModel):
    username: str
    password: str


JWT_SECRET_KEY= os.environ['JWT_SECRET_KEY']
ALGORITHM= os.environ['ALGORITHM']

def get_hash_password(password: str):
    """
    Recibes a plain text password and hashes it with bcrypt scheme

    Parameters
    ----------
    password : str
        Plain text password.

    Returns
    -------
    hash_password : str
        Hash password based on bcrypt scheme.
    """
    return password_context.hash(password)

def verify_password(password: str, hashed_pass: str) -> bool:
    """
    Recibes a plain text password and hashed encrypted password and verify if they match.

    Parameters
    ----------
    password: str
        Plain text password.
    hashed_pass : str
        Encrypted password retrieved from database

    Returns
    -------
    verification : bool
        Boolean if password is valid.
    """
    return password_context.verify(password, hashed_pass)    

def create_access_token(sub: Union[str, Any], expires_delta: int = None) -> str:

    """
    Recibes a json format string or dict and the amount of minutes a new token can last and returns a encrypted token with that data saved in a JWT.

    Parameters
    ----------
    sub: dict, str
        User data to be encrypted.
    expires_delta : int
        Number of minutes that the encrypted token is valid

    Returns
    -------
    encrypted_jwt : str
        JSON web token with the information provided.
    """

    if expires_delta is not None:
        expires_delta= datetime.utcnow() + timedelta(minutes= expires_delta)
    else:
        expires_delta= datetime.utcnow() + timedelta(minutes= 30)

    expires_delta= expires_delta.replace(microsecond= 0)

    to_encode= dict(
        expires= str(expires_delta),
        sub= str(sub)
    )

    encoded_jwt= jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def verify_user(username, password):

    """
    Recibes a plain text password and username and validates the credentials in the database

    Parameters
    ----------
    username: str
        User database.
    password : str
        Plain text password provided.

    Returns
    -------
    verification : bool
        Boolean if credentials are valid.
    """
    
    users_table= Table('users')
    get_user_query= Query\
        .from_(users_table)\
        .select(users_table.username, users_table.password)\
        .where(users_table.username == username)\
        .get_sql()

    conn= sqlite3.connect('./app.db')
    
    conn_cursor= conn.cursor() 
    query_data= conn_cursor.execute(
        get_user_query
    ).fetchall()
    conn_cursor.close()

    if len(query_data):
        
        user_data= query_data[0]
        user= user_data[0]
        hash_password= user_data[1]

        if verify_password(password= password, hashed_pass= hash_password):
            return True
        
    return False

templates= Jinja2Templates(directory='./public/templates')
@router.post('/', tags= ["auth"])
@router.get('/', tags= ["auth"])
async def render_login_form(request: Request):
    response = templates.TemplateResponse(
        name= 'signin.html',
        context= {'request': request},
        status_code= 200
    )

    return response

@router.get('/signup', tags= ["auth"])
async def render_login_form(request: Request):

    context = {
        "request": request,
        "genders": data_index_attr['sex'],
        "state_of_birth": data_index_attr['state_of_birth'],
        "nationality": data_index_attr['nacionality']
    }

    response = templates.TemplateResponse(
        name= 'signup.html',
        context= context,
        status_code= 200
    )

    return response

@router.post('/signup', tags= ["auth"])
async def check_signup_user(request: Request, form_data: Data = Depends()):
    
    users_t= Table(name= 'users')
    
    get_query= Query\
        .from_(users_t)\
        .select(users_t.username)\
        .where(users_t.username == form_data.username)\
        .get_sql()

    insert_query= str(
        Query\
            .into(users_t)\
            .insert(
                form_data.username,
                get_hash_password(form_data.password),
                form_data.first_name,                
                form_data.last_name,
                form_data.sex,
                form_data.nationality,
                form_data.birth_date,
                form_data.state_of_birth
            )
        )

    conn= sqlite3.connect('./app.db')
    
    conn_cursor= conn.cursor() 
    users= conn_cursor.execute(
        get_query
    ).fetchall()

    if not len(users):
        conn_cursor.execute(
            insert_query
        )

        conn.commit()
        #response= RedirectResponse(url="/auth")
        html_content = """
            <html>
                <head>
                    <title>Credit Risk Analysis Score</title>
                    <link rel="stylesheet" href="../static/css/signin.css"></link>
                    <script language="JavaScript">
                        function redireccionar() {
                            setTimeout("location.href='/auth'", 5000);
                        }
                    </script>
                </head>
                <body onLoad="redireccionar()">
                    <div class="container-fluid px-1 py-5 mx-auto">
                        <div class="row d-flex justify-content-center">
                            <div class=" text-center">
                                <div class="card">
                                    <h1><p class="blue-text">User Stored Successfully!!</p></h1>
                                </div>
                            </div>
                        </div>
                    </div>
                </body>
            </html>
            """
        return HTMLResponse(content=html_content, status_code=200)        
    else:
        #response= PlainTextResponse("Usuario ya existente", status_code= 400)
        html_content = """
        <html>
            <head>
                <title>Credit Risk Analysis Score</title>
                <link rel="stylesheet" href="../static/css/signin.css"></link>
                <script language="JavaScript">
                    function redireccionar() {
                        setTimeout("location.href='/auth'", 5000);
                    }
                </script>
            </head>
            <body onLoad="redireccionar()">
                <div class="container-fluid px-1 py-5 mx-auto">
                    <div class="row d-flex justify-content-center">
                        <div class=" text-center">
                            <div class="card">
                                <h1><p class="blue-text">User Already Exists in the Database!!</p></h1>
                            </div>
                        </div>
                    </div>
                </div>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=200)
    conn.commit()

    return response

@router.post('/token', tags= ["auth"])
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):

    if verify_user(form_data.username, form_data.password):
        
        users_t= Table(name= 'users')
        
        get_user_query= Query\
            .from_(users_t)\
            .select(
                users_t.username,
                users_t.password,
                users_t.first_name,
                users_t.last_name,
                users_t.gender,
                users_t.nationality,
                users_t.birth_date,
                users_t.state_birth
            )\
            .where(users_t.username == form_data.username)\
            .get_sql()
        conn= sqlite3.connect('./app.db')
        conn_cursor= conn.cursor()
        user= conn_cursor.execute(
            get_user_query
        ).fetchall()[0]
        conn.close()

        password= user[1]
        first_name= user[2]
        last_name= user[3]
        gender= user[4]
        nationality= user[5]
        birth_date= user[6]
        state_birth= user[7]

        d1 = user[6].split('-')
        year = int(d1[0])
        month = int(d1[1])
        day = int(d1[2])
        birth_date = date(year, month, day)    
        today = date.today()
        birth_date = round(((today - birth_date).days)/365)
        
        for row in data_index_attr['sex']:
            if str(row['id']).startswith(gender):
                gender_description = row['description']        

        for row in data_index_attr['nacionality']:
            if str(row['id']).startswith(nationality):
                nationality_description = row['description']        

        for row in data_index_attr['state_of_birth']:
            if str(row['id']).startswith(state_birth):
                state_of_birth_description = row['description']        

        user= dict(
            username= form_data.username,
            password= password,
            first_name= first_name,
            last_name= last_name,
            gender= gender,
            gender_description= gender_description,            
            nationality= nationality,
            nationality_description= nationality_description,
            birth_date= str(birth_date),            
            state_birth= state_birth,
            state_of_birth_description = state_of_birth_description
        )

        access_token= create_access_token(user, expires_delta= 15)
        # response= PlainTextResponse("Usuario ingresado")
        response= RedirectResponse(url="/index")
        response.set_cookie(key= "auth", value= access_token)
    
    else:
        
        #raise HTTPException(
        #    status_code= 400,
        #    detail= "Invalid username or password",
        #)

        html_content = """
        <html>
            <head>
                <title>Credit Risk Analysis Score</title>
                <link rel="stylesheet" href="../static/css/signin.css"></link>
                <script language="JavaScript">
                    function redireccionar() {
                        setTimeout("location.href='/auth'", 5000);
                    }
                </script>
            </head>
            <body onLoad="redireccionar()">
                <div class="container-fluid px-1 py-5 mx-auto">
                    <div class="row d-flex justify-content-center">
                        <div class=" text-center">
                            <div class="card">
                                <h1><p class="blue-text">Invalid username or password!!</p></h1>
                            </div>
                        </div>
                    </div>
                </div>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=200)
    return response

@router.get("/user")
def verify_user_token(request: Request):

    token= request.cookies.get('auth', None)

    if not token is None:
        decoded_token= jwt.decode(
            token= token,
            key= JWT_SECRET_KEY,
            algorithms= [ALGORITHM]
        )
        expiration_datetime= datetime.strptime(
            decoded_token.get('expires'), 
            "%Y-%m-%d %H:%M:%S"
        )
        if datetime.utcnow() < expiration_datetime:
    
            print(decoded_token)
            return request
        
        else:
            response= RedirectResponse(
                url="/",
                status_code= 300
            )
            response.delete_cookie(key= 'auth')

            return response
    
    else:
        response= HTTPException(
            status_code= 400,
            detail= "Invalid or expired Token",
        )
        raise response

if __name__ == "__main__":

    import sqlite3, textwrap

    con= sqlite3.connect('./app.db')
    c= con.cursor()
    c.execute(
        textwrap.dedent("""
        ALTER TABLE users ADD first_name text;
        """)        
    )
    con.close()
    