import pytest
import allure
from sqlalchemy.orm import Session

from db_requester.models import AccountTransactionTemplate
from utils.data_generator import DataGenerator


@pytest.mark.parametrize("parameter_name", ["value1", "value2"])
class TestParametrizeClass:
    def test_first(self, parameter_name):
        print(f"Test 1 progon: {parameter_name}")
        assert True

    def test_second(self, parameter_name):
        print(f"Test 2 progon: {parameter_name}")
        assert True

@allure.epic("Тестирование транзакций")
@allure.feature("Тестирование транзакций между счетами")
class TestAccountTransactionTemplate:

    @allure.story("Корректность перевода денег между двумя счетами")
    @allure.description("""
    Этот тест проверяет корректность перевода денег между двумя счетами.
    Шаги:
    1. Создание двух счетов: Stan и Bob.
    2. Перевод 200 единиц от Stan к Bob.
    3. Проверка изменения балансов.
    4. Очистка тестовых данных.
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Ivan Petrovich")
    @allure.title("Тест перевода между счетами 200 рублей")
    def test_account_transaction_template(self, db_session: Session):
        # ====================================================================== Подготовка к тесту
        with allure.step("Создание тестовых данных в БД: счета Stan и Bob"):
            stan = AccountTransactionTemplate(user=f"Stan", balance=1000)
            bob = AccountTransactionTemplate(user=f"Bob", balance=500)
            # Добавляем записи в сессию
            db_session.add_all([stan, bob])
            db_session.commit()

        @allure.step("Функция перевода денег: transfer_money")
        @allure.description("""
        функция выполняющая транзакцию, имитация вызова функции на стороне тестируемого сервиса
        и вызывая метод transfer_money, мы как-будто бы делаем запрос в api_manager.movies_api.transfer_money
        """)
        def transfer_money(session, from_account, to_account, amount):
            with allure.step("Получаем счета"):
                from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
                to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()

            with allure.step("Проверяем, что на счете достаточно средств"):
                if from_account.balance < amount:
                    raise ValueError("Недостаточно средств")

            with allure.step("Выполняем перевод"):
                from_account.balance -= amount
                to_account.balance += amount

            with allure.step("Сохраняем изменения"):
                session.commit()

        # ====================================================================== Тест
        with allure.step("Проверяем начальные балансы"):
            assert stan.balance == 1000
            assert bob.balance == 500

        try:
            with allure.step("Выполняем перевод 200 единиц от стэна к бобу"):
                transfer_money(db_session, from_account=stan.user, to_account=bob.user, amount=200)

            with allure.step("Проверяем, что балансы изменились"):
                assert stan.balance == 800
                assert bob.balance == 700

        except Exception as e:
            with allure.step("ОШИБКА откаты транзакций"):
                db_session.rollback()

        finally:
            with allure.step("Удаляем данные для тестирования из БЛ"):
                db_session.delete(stan)
                db_session.delete(bob)
                db_session.commit()

