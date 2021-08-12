from assessment.models.customer import Customer
from typing import List, Optional
from faker import Faker

class CustomerFactory(object):

    def __init__(self, locale:List[str]=['en_GB']) -> None:
        self.faker = Faker(locale)

    def create(
        self,
        title:Optional[str]=None, first_name:Optional[str]=None,
        last_name:Optional[str]=None, username:Optional[str]=None,
        email:Optional[str]=None, password:Optional[str]=None, house_number:Optional[str]=None,
        street:Optional[str]=None, town:Optional[str]=None, county:Optional[str]=None,
        postcode:Optional[str]=None
    ) -> Customer:

        c = {
            'title': title or self.faker.prefix().lower().replace('.',''),
            'first_name': first_name or self.faker.first_name(),
            'last_name': last_name or self.faker.last_name(),
            'password': password or self.faker.password(),
            'house_number': house_number or self.faker.building_number(),
            'street': street or self.faker.street_address().replace("\n", " "),
            'town': town or self.faker.city(),
            'county': county or self.faker.county(),
            'postcode': postcode or self.faker.postcode().replace(' ',''),
        }
        c.update( {
            'username': username or f'{c["first_name"].lower()}{c["last_name"].lower()}',
            'email': email or '{}.{}@{}'.format(
                c["first_name"].lower(),
                c["last_name"].lower(),
                self.faker.domain_name()
            )
        } )
        customer = Customer(**c)
        return customer
