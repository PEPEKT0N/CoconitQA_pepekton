from pydantic import BaseModel, field_validator, ValidationError
from typing import Optional
from constants.roles import Roles

class User(BaseModel):
    email: str
    fullName: str
    password: str
    roles: list[Roles]
    verified: Optional[bool] = False
    banned: Optional[bool] = False

    @field_validator("email")
    def check_email(cls, value: str) -> str:
        if '@' not in value:
            raise ValidationError("Email should contain @")
        return value

    @field_validator("password")
    def check_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValidationError("Length should be 8 or greater")



def test_user_validation(test_user):
    user = User(**test_user)
    assert user.email == test_user.get('email'), "Emails doesn't match"

def test_creation_user_validation(creation_user_data):
    user = User(**creation_user_data)
    assert user.verified is True
    assert user.banned is False

def test_json_invoke_with_exclude_unset(test_user):
    user = User(**test_user)
    json_data = user.model_dump_json(exclude_unset=True)
    print()
    print(json_data)

def test_json_invoke_without_exclude_unset(creation_user_data):
    user = User(**creation_user_data)
    json_data = user.model_dump_json()
    print()
    print(json_data)

def test_my_dictionary_validator():
    user_dict = {"email": "test1@examle.com",
                 "fullName": "Rayn Gosling",
                 "password": "Qwerty123",
                 "roles": (Roles.USER.value, )
                 }

    user = User(**user_dict)