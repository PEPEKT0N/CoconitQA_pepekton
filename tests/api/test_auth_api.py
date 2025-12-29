import pytest
from api.api_manager import ApiManager
from model.TestUser import RegisterUserResponse

class TestAuthAPI:
    def test_register_user(self, api_manager: ApiManager, registration_user_data):
        """
        Тест на регистрацию пользователя.
        """
        response = api_manager.auth_api.register_user(user_data=registration_user_data)
        registration_user_response = RegisterUserResponse(**response.json())
        assert registration_user_response.email == registration_user_data.email, "Email не совпадает"
        assert registration_user_response.fullName == registration_user_data.fullName, "Имена не совпадают"

    def test_register_and_login_user(self, api_manager: ApiManager, registered_user, login_data_user):
        """
        Тест на регистрацию и авторизацию пользователя.
        """

        response = api_manager.auth_api.login_user(login_data_user)
        response_data = response.json()
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"

    @pytest.mark.slow
    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data).json()

        assert response.get('id') and response['id'] != ''
        assert response.get('email') == creation_user_data['email']
        assert response.get('fullName') == creation_user_data['fullName']
        assert response.get('roles') == creation_user_data['roles']
        assert response.get('verified') is True



    @pytest.mark.slow
    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user_response = super_admin.api.user_api.create_user(creation_user_data).json()
        response_by_id = super_admin.api.user_api.get_user_info(created_user_response['id']).json()
        response_by_email = super_admin.api.user_api.get_user_info(creation_user_data['email']).json()

        assert response_by_id == response_by_email, "Содержание ответов должно быть идентичным"
        assert response_by_id.get('id') and response_by_id['id'] != '', "ID должен быть не пустым"
        assert response_by_id.get('email') == creation_user_data['email']
        assert response_by_id.get('fullName') == creation_user_data['fullName']
        assert response_by_id.get('roles', []) == creation_user_data['roles']
        assert response_by_id.get('verified') is True

    @pytest.mark.slow
    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user_info(common_user.email, expected_status=403)

    # def test_wrong_pass_auth(self, api_manager: ApiManager, registered_user, auth_with_wrong_password):
    #     """
    #     Тест на авторизацию с неправильным паролем.
    #     """
    #     response = api_manager.auth_api.login_user(auth_with_wrong_password, 401)
    #     response_data = response.json()
    #
    #     assert "message" in response_data or "error" in response_data, "Сообщение об ошибке отсутствует"
    #     assert response_data.get("statusCode") == 401, "Неверный код ошибки в теле ответа"
    #
    # def test_auth_with_empty_body(self, api_manager: ApiManager):
    #     """
    #     Тест на авторизацию с пустым телом запроса.
    #     """
    #     auth_data = {}
    #     response = api_manager.auth_api.login_user(auth_data, 401)
    #     response_data = response.json()
    #
    #     assert "error" in response_data or "message" in response_data, "Отсутствует описание ошибки"
    #     assert response_data.get("statusCode") == 401, "Неверный код ошибки в теле ответа"
    #
    # def test_incorrect_data_auth(self, api_manager: ApiManager, incorrect_auth_data):
    #     """
    #     Тест на авторизацию с некорректными данными.
    #     """
    #     response = api_manager.auth_api.login_user(incorrect_auth_data, 401)
    #     response_data = response.json()
    #
    #     assert "error" in response_data or "message" in response_data, "Отсутствует описание ошибки"
    #     assert response_data.get("statusCode") == 401, "Неверный код ошибки в теле ответа"

