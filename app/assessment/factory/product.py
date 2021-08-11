import random
from assessment.models.product import Product
from typing import List, Optional
from faker import Faker

class ProductFactory(object):

    def __init__(self, locale:List[str]=['en_GB']) -> None:
        self.faker = Faker(locale)

    def create(
        self,
        name:Optional[str]=None,
        description:Optional[str]=None,
        price:Optional[int]=None
    ) -> Product:

        p = {
            'name': name or '-'.join(self.faker.words(nb=2)),
            'description': description or self.faker.text(max_nb_chars=160),
            'price': price or int(random.uniform(3000, 12000))
        }
        product = Product(**p)
        return product
