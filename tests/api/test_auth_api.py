import pytest
import requests

from constants import BASE_URL, HEADERS, REGISTER_ENDPOINT, LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from api.api_manager import ApiManager

class TestAuthAPI:
    def test_register_user(self, api_manager: ApiManager, test_user):
        """
        Тест на регистрацию пользователя.
        """
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()

        assert response_data["email"] == test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    def test_register_and_login_user(self, api_manager: ApiManager, registered_user, login_data_user):
        """
        Тест на регистрацию и авторизацию пользователя.
        """        

        response = api_manager.auth_api.login_user(login_data_user)
        response_data = response.json()
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"

    def test_wrong_pass_auth(self, api_manager: ApiManager, registered_user, auth_with_wrong_password):   
        """
        Тест на авторизацию с неправильным паролем.
        """     
        response = api_manager.auth_api.login_user(auth_with_wrong_password, 401)
        response_data = response.json()
        
        assert "message" in response_data or "error" in response_data, "Сообщение об ошибке отсутствует"
        assert response_data.get("statusCode") == 401, "Неверный код ошибки в теле ответа"        

    def test_auth_with_empty_body(self, api_manager: ApiManager):
        """
        Тест на авторизацию с пустым телом запроса.
        """
        auth_data = {}
        response = api_manager.auth_api.login_user(auth_data, 401)
        response_data = response.json()
        
        assert "error" in response_data or "message" in response_data, "Отсутствует описание ошибки"
        assert response_data.get("statusCode") == 401, "Неверный код ошибки в теле ответа"        

    def test_incorrect_data_auth(self, api_manager: ApiManager, incorrect_auth_data):
        """
        Тест на авторизацию с некорректными данными.
        """
        response = api_manager.auth_api.login_user(incorrect_auth_data, 401)
        response_data = response.json()
        
        assert "error" in response_data or "message" in response_data, "Отсутствует описание ошибки"
        assert response_data.get("statusCode") == 401, "Неверный код ошибки в теле ответа"        

