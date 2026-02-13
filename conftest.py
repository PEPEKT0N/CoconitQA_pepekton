from faker import Faker
import requests
import pytest
from playwright.sync_api import sync_playwright

from constants.constants import BASE_URL, REGISTER_ENDPOINT, HEADLESS
from model.cinescope_login_page import CinescopeLoginPage
from utils.data_generator import DataGenerator
from custom_requester.custom_requester import CustomRequester
from api.api_manager import ApiManager
from entities.user import User
from resources.user_creds import SuperAdminCreds
from constants.roles import Roles
from model.TestUser import TestUser, RegisterUserResponse
from sqlalchemy.orm import Session
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper

faker = Faker()

@pytest.fixture(scope="function")
def test_user() -> TestUser:
    """
        Генерация случайного пользователя для тестов.
    """
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER]
    )

@pytest.fixture(scope="function")
def registered_user(requester, test_user: TestUser):
    """
        Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
    register_user_response = RegisterUserResponse(**response.json())
    yield test_user, register_user_response

@pytest.fixture(scope="function")
def login_data_user(registered_user):
    test_user, _ = registered_user
    return {
        "email": test_user.email,
        "password": test_user.password
    }

@pytest.fixture(scope="function")
def auth_with_wrong_password(registered_user):
    reg_data, _ = registered_user
    return {
        "email": reg_data.email,
        "password": f"!{reg_data.password}"
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
        creation_user_data.email,
        creation_user_data.password,
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
        roles = [Roles.USER]
    )

@pytest.fixture(scope="module")
def db_session() -> Session:
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных
    После завершения теста сессия автоматически закрывается
    """
    db_session = get_db_session()
    yield db_session
    db_session.close()

@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    """
    Фикстура для экземпляра хелпера
    """
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope="function")
def created_test_user(db_helper):
    """
    Фикстура, которая создает тестового пользователя в БД
    и удаляет его после завершения теста
    """
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    # Cleanup после теста
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)

@pytest.fixture(scope="function")
def created_test_movie(db_helper):
    """
    Фикстура, которая создает тестовый фильм в БД
    и удаляет его после завершения теста
    """
    movie = db_helper.create_test_movie(DataGenerator.generate_movie_data())
    yield movie
    if db_helper.get_movie_by_name(movie.name):
        db_helper.delete_movie(movie)

@pytest.fixture(scope="function")
def review_movie():
    return DataGenerator.generate_random_description()

@pytest.fixture
def page():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=HEADLESS)
        page = browser.new_page()
        yield page
        browser.close()

@pytest.fixture
def authorized_page(page, login_data_user):
    login_page = CinescopeLoginPage(page)
    login_page.open()
    login_page.login(login_data_user["email"], login_data_user["password"])
    login_page.assert_was_redirect_to_home_page()
    return page