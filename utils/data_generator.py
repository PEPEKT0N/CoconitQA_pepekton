import random
import string
from faker import Faker
faker = Faker()
import datetime
from constants.roles import Roles
from datetime import datetime, timedelta

class DataGenerator:

    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_movie_title():
        words_count = random.choice([1, 3])
        words = faker.words(nb=words_count)
        number = random.randint(1, 10)
        title = " ".join(w.capitalize() for w in words)
        return f"{title} {number}"

    @staticmethod
    def generate_random_password():
        letters = random.choice(string.ascii_letters)
        digits = random.choice(string.digits)

        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return''.join(password)

    @staticmethod
    def generate_random_description():
        return faker.text(50)

    @staticmethod
    def generate_random_url():
        return f"https://{faker.text(10).strip()}.com"

    @staticmethod
    def generate_random_datetime() -> datetime:
        start = datetime(1990, 1, 1)
        end = datetime.now()

        delta = end - start
        random_seconds = random.uniform(0, delta.total_seconds())

        return start + timedelta(seconds=random_seconds)

    @staticmethod
    def generate_user_data() -> dict:
        """Генерирует данные для тестового пользователя"""
        from uuid import uuid4

        return {
            'id': f'{uuid4()}',
            'email': DataGenerator.generate_random_email(),
            'full_name': DataGenerator.generate_random_name(),
            'password': DataGenerator.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': False,
            'banned': False,
            'roles': [Roles.USER.value]
        }

    @staticmethod
    def generate_movie_data() -> dict:
        return {
            'name': DataGenerator.generate_random_movie_title(),
            'price': round(random.uniform(100, 500), 2),
            'description': DataGenerator.generate_random_description(),
            'image_url': DataGenerator.generate_random_url(),
            'location': random.choice(['MSK', 'SPB']),
            'published': True,
            'rating': round(random.uniform(0, 5), 2),
            'genre_id': random.randint(1, 10),
            'created_at': DataGenerator.generate_random_datetime()
        }

