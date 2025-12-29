from faker import Faker
import requests
from constants.constants import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT
import pytest
from utils.data_generator import DataGenerator
from custom_requester.custom_requester import CustomRequester
from api.api_manager import ApiManager
from entities.user import User
from resources.user_creds import SuperAdminCreds
from constants.roles import Roles
from model.TestUser import TestUser

faker = Faker()

@pytest.fixture(scope="function")
def test_user():
    """
        Генерация случайного пользователя для тестов.
    """
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )

@pytest.fixture(scope="function")
def registered_user(requester, test_user):
    """
        Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    yield registered_user

@pytest.fixture(scope="function")
def login_data_user(registered_user):
    return {
        "email": registered_user["email"],
        "password": registered_user["password"]
    }

@pytest.fixture(scope="function")
def auth_with_wrong_password(registered_user):
    return {
        "email": registered_user["email"],
        "password": f"!{registered_user["password"]}"
    }

@pytest.fixture(scope="function")
def incorrect_auth_data():
    return {
        "firstname": "Rayn",
        "lastname": "Gosling"
    }

@pytest.fixture(scope="session")
def requester():
    """
       Фикстура для создания экземпляра CustomRequester.
   """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)

@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session
    )

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture(scope="function")
def creation_user_data(test_user: TestUser) -> TestUser:
    return test_user.model_copy(
        update={
            "verified": True,
            "banned": False
        }
    )

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        list(Roles.USER.value),
        new_session
    )

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture
def registration_user_data():
    random_password = DataGenerator.generate_random_password()

    return TestUser (
        email = DataGenerator.generate_random_email(),
        fullName = DataGenerator.generate_random_name(),
        password = random_password,
        passwordRepeat = random_password,
        roles = [Roles.USER.value]
    )