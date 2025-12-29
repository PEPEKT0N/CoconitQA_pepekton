import json
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
    email: str

user = User(name="Alice", age=25, email="alice@example.com")

# Сериализация
json_data = user.model_dump_json()
print(json_data)

new_user = User.model_validate_json(json_data)
print(new_user.name)

# Сериализация в файл
with open("user.json", "w") as file:
    json.dump(user.model_dump(), file)

# Десериализация из файла
with open("user.json", "r") as file:
    user_data = json.load(file)
    new_user = User(**user_data)

print(new_user)