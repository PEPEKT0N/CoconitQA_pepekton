import psycopg2
from resources.db_creds import DbCreds

def connect_topostgres():
    """
    Функция для подключения к PostgreSQL БД
    """

    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(
            dbname="db_movies",
            user=DbCreds.DB_USER,
            password=DbCreds.DB_PASSWORD,
            host="80.90.191.123",
            port="31200"
        )

        print("Подключчение успешно установлено")

        cursor = connection.cursor()

        print("Информация о сервере PostgreSQL:")
        print(connection.get_dsn_parameters(), "\n")

    except Exception as error:
        print("Ошибка при работе с БД:", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

        print("Соединение с БД закрыто")

if __name__ == "__main__":
    connect_topostgres()