from flask_mongoengine import MongoEngine
from datetime import datetime, timedelta, date
import googlemaps
from email_validator import validate_email, EmailNotValidError
GM_API_KEY = 'YOUR_API_KEY'

db = MongoEngine()


class DB_Customer(db.Document):
    first_name = db.StringField(required=True)
    last_name = db.StringField(required=True)
    password = db.StringField(required=True)
    email = db.EmailField(required=True, unique=True)
    phone = db.StringField(required=True)
    communication_preferences = db.StringField(required=True)
    finances = db.StringField(required=True)
    

class DB_Contract(db.Document):
    customer = db.ReferenceField(DB_Customer, required=True, unique=True)
    contract = db.StringField(required=True)
    pricing = db.StringField(required=True)
    agreements = db.StringField(required=True)
    renewal_time = db.FloatField(required=True)
    contracted_in = db.DateTimeField(required=True)
    renewal_day = db.DateTimeField(required=True)


class DB_Address(db.Document):
    customer = db.ReferenceField(DB_Customer, required=True, unique=True)
    address_line1 = db.StringField(required=True)
    address_line2 = db.StringField()
    address_line3 = db.StringField()
    city = db.StringField(required=True)
    state = db.StringField(required=True)
    country = db.StringField(required=True)
    zip_code = db.StringField(required=True)
    geo = db.StringField(required=True)
    latitude = db.StringField(required=True)
    longitude = db.StringField(required=True)
    formatted_address = db.StringField(required=True)


class Address():
    def __init__(self, add_line1: str, add_line2: str, add_line3: str, city: str, state: str, country: str, zip_code: str):
        self.address_line1 = add_line1
        self.address_line2 = add_line2
        self.address_line3 = add_line3
        self.city = city
        self.state = state
        self.country = country
        self.zip_code = zip_code
        self._geo = self.get_enhanced_geolocation
        self._latitude = self._geo["Latitude"]
        self._longitude = self._geo["Longitude"]
        self._formatted_address = self._geo["Formatted_Address"]

    def get_enhanced_geolocation(self):
        gmaps = googlemaps.Client(GM_API_KEY)
        geocode_result = gmaps.geocode(self.address_line1)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            return {"Latitude": location['lat'], "Longitude": location['lng'], "Formatted_Address": geocode_result[0]['formatted_address']}
        else:
            raise ValueError, "Geolocation data not found"
    
    @property
    def latitude(self):
        return self._latitude
    
    @property
    def longitude(self):
        return self._longitude
    
    @property
    def formatted_address(self):
        return self._formatted_address
    
    @property
    def address_line1(self):
        return self._address_line1
    
    @address_line1.setter
    def address_line1(self, address_line1: str):
        self._address_line1 = address_line1
        self._geo = self.get_enhanced_geolocation
        self._latitude = self._geo["Latitude"]
        self._longitude = self._geo["Longitude"]
        self._formatted_address = self._geo["Formatted_Address"]    


class Contract():
    def __init__(self, contract: str, pricing: float, agreements: str, renewal_time: int):
        self.contract = contract
        self.pricing = pricing
        self.agreements = agreements
        self.renewal_time = renewal_time
        self._contracted_in = datetime.now()
        self._renewal_day = date(self.contracted_in + timedelta(days=self.renewal_time))
    
    @property
    def contract(self):
        return self._contract
    
    @contract.setter
    def contract(self, contract: str):
        with open(contract, 'r') as reader:
            self._contract = reader.read()
    
    @property
    def pricing(self):
        return self._pricing
    
    @pricing.setter
    def pricing(self, pricing: float):
        try:
            self._pricing = float(pricing)
        except ValueError:
            raise ValueError, "Pricing must be a number"
    
    @property
    def agreements(self):
        return self._agreements
    
    @agreements.setter
    def agreements(self, agreements: str):
        with open(agreements, 'r') as reader:
            self._agreements = reader.read()

    @property
    def renewal_time(self):
        return self._renewal_time
    
    @renewal_time.setter
    def renewal_time(self, renewal_time: int):
        try:
            self._renewal_time = int(renewal_time)
        except ValueError:
            raise ValueError, "Renewal time must be an integer number"

    @property
    def contracted_in(self):
        return self._contracted_in

    @property
    def renewal_day(self):
        return self._renewal_day
    
    @property
    def renewed(self):
        return self._renewed
    
    @renewal_day.setter
    def renewal_day(self, renewal_day: date):
        self._renewed = datetime.now()
        if type(renewal_day) == date:
            self._renewal_day = renewal_day
        else:
            raise TypeError, "Renewal day must be a datetime.date object"
    
    def renew(self):
        self.renewal_day = date(self.renewal_day + timedelta(days=self.renewal_time))
    

class Customer():
    def __init__(self, first_name: str, last_name: str, password: str, email: str, phone: str, address:Address, contract: Contract, communication_preferences: str, finances: str):
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.email = email
        self.phone = phone
        self.address = address
        self.communication_preferences = communication_preferences
        self.finances = finances
        self.contract = contract
    
    @property
    def contract(self):
        return self._contract
    
    @contract.setter
    def contract(self, contract: Contract):
        if type(self.contract) == Contract:
            self._contract = contract
        else:
            raise TypeError, "The contract of a user must be an Contract object"
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email_address: str):
        validate_email(email_address)
        self._email = email_address
    
    @property
    def address(self):
        return self._address
    
    @address.setter
    def address(self, address: Address):
        if type(address) == Address:
            self._address = address
        else:
            raise TypeError, "The address of a user must be an Address object"
    
    def save(self):
        customer = DB_Customer(
            first_name=self.first_name,
            last_name=self.last_name,
            password=self.password,
            email=self.email,
            phone=self.phone,
            communication_preferences=self.communication_preferences,
            finances=self.finances
        )
        address = DB_Address(
            customer = self.email,
            address_line1=self.address.address_line1,
            address_line2=self.address.address_line2,
            address_line3=self.address.address_line3,
            city=self.address.city,
            state=self.address.state,
            country=self.address.country,
            zip_code=self.address.zip_code,
            geo=self.address._geo,
            latitude=self.address._latitude,
            longitude =self.address._longitude,
            formatted_address=self.address._formatted_address
        )
        contract = DB_Contract(
            customer=self.email,
            contract=self.contract.contract,
            pricing=self.contract.pricing,
            agreements=self.contract.agreements,
            renewal_time=self.contract.renewal_time,
            contracted_in=self.contract._contracted_in,
            renewal_day=self.contract._renewal_day
        )
        customer.save()
        address.save()
        contract.save()
    