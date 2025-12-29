from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool

    # def __init__(self, name, price, in_stock):
    #     self.name = name
    #     self.price = price
    #     self.in_stock = in_stock

product1 = Product(name="Phone", price="987.99", in_stock="true")
json_product1 = product1.model_dump_json()
print(json_product1)

product2 = Product.model_validate_json(json_product1)
print(product2)