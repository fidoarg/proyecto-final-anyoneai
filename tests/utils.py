import os

from jose       import jwt
from typing     import Union, Any
from datetime   import datetime, timedelta

# Fast API utilities
from fastapi import Form

from typing import Optional

from pydantic.dataclasses import dataclass

# Global constants needed for encryption
JWT_SECRET_KEY = '060b4cc4e1ccf551e131e0c495939514006d257a16aab75580b37d4b898eb237'
ALGORITHM = 'HS256'

# Data class to pass the person's information
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


def create_access_token(sub: Union[str, Any], expires_delta: int = None) -> str:

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