from sqlalchemy.orm import declarative_base
from sqlalchemy import INTEGER, VARCHAR, SmallInteger, DATETIME, Table

from typing import Optional
from datetime import datetime

from . import engine

Base = declarative_base()


class User(Base):
    __table__ = Table('users', Base.metadata, autoload=True, autoload_with=engine)

    def __init__(self, username: str, password: str, role_id: int, is_active: int):
        self.username = username
        self.password = password
        self.role_id = role_id
        self.is_active = is_active

    def __repr__(self):
        return f'<User {self.user_id} ({self.username})>'


class Role(Base):
    __table__ = Table('role', Base.metadata, autoload=True, autoload_with=engine)

    def __init__(self, role_name: str):
        self.role_name = role_name

    def __repr__(self):
        return f'<Role {self.role_id} ({self.role_name})>'


class Site(Base):
    __table__ = Table('site', Base.metadata, autoload=True, autoload_with=engine)

    def __init__(self, site_name: str, is_active: int):
        self.site_name = site_name
        self.is_active = is_active

    def __repr__(self):
        return f'<Site {self.site_id} ({self.site_name})>'


class Profile(Base):
    __table__ = Table('profile', Base.metadata, autoload=True, autoload_with=engine)

    def __init__(self, person_type_id: Optional[int], inn: Optional[str], last_name: Optional[str], first_name: Optional[str], middle_name: Optional[str], last_update: datetime, birth_date: Optional[datetime] = None, parent_person_id: Optional[int] = None, ):

        self.person_type_id = person_type_id
        self.inn = inn
        self.birth_date = birth_date
        self.parent_person_id = parent_person_id
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_update = last_update

    def __repr__(self):
        return f'<Profile {self.person_id} ({self.inn})>'


class PersonType(Base):
    __table__ = Table('person_type', Base.metadata, autoload=True, autoload_with=engine)

    def __init__(self, type_name: str):
        self.type_name = type_name

    def __repr__(self):
        return f'<PersonType {self.person_type_id} ({self.type_name})>'


class Link(Base):
    __table__ = Table('link', Base.metadata, autoload=True, autoload_with=engine)

    def __init__(self, site_id: int, person_id: int, link: Optional[str] = "nan", probability: Optional[float] = 1.0):
        self.site_id = site_id
        self.person_id = person_id
        self.link = link
        self.probability = probability

    def __repr__(self):
        return f'<Link {self.site_id} (person_id={self.person_id})>'


class EntityType(Base):
    __table__ = Table('entity_type', Base.metadata, autoload=True, autoload_with=engine)

    def __init__(self, type_name: str, translation: str):
        self.type_name = type_name
        self.translation = translation

    def __repr__(self):
        return f'<EntityType {self.entity_type_id} ({self.type_name})>'


class EntityLink(Base):
    __table__ = Table('entity_link', Base.metadata, autoload=True, autoload_with=engine)

    def __init__(self, entity_id: int, link_id: int, entity_type_id: int):
        self.entity_id = entity_id
        self.link_id = link_id
        self.entity_type_id = entity_type_id

    def __repr__(self):
        return f'<EntityLink {self.entity_link_id} (entity_id={self.entity_id})>'


class D_Work(Base):
    __table__ = Table('d_work', Base.metadata, autoload=True, autoload_with=engine)

    def __init__(self, organization_name: Optional[str], address_id: Optional[int],
                 contact_id: Optional[int], description: Optional[str]):
        self.organization_name = organization_name
        self.address_id = address_id
        self.contact_id = contact_id
        self.description = description

    def __repr__(self):
        return f'<D_Work {self.work_id}>'


class D_SiteCheck(Base):
    __table__ = Table('d_site_check', Base.metadata, autoload=True, autoload_with=engine)

    def __init__(self, site_id: int, description: Optional[str]):
        self.site_id = site_id
        self.description = description

    def __repr__(self):
        return f'<D_SiteCheck {self.site_check_id} (site_id={self.site_id})>'


class D_PropertyType(Base):
    __table__ = Table('d_property_type', Base.metadata, autoload=True, autoload_with=engine)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'<D_PropertyType {self.property_type_id}>'


class D_PropertyCategory(Base):
    __table__ = Table('d_property_category', Base.metadata, autoload=True, autoload_with=engine)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'<D_PropertyCategory {self.property_category_id}>'


class D_Property(Base):
    __table__ = Table('d_property', Base.metadata, autoload=True, autoload_with=engine)

    def __init__(self, property_category_id: int, property_type_id: int,
                 address_id: Optional[int], description: Optional[str]):
        self.property_category_id = property_category_id
        self.property_type_id = property_type_id
        self.address_id = address_id
        self.description = description

    def __repr__(self):
        return f'<D_Property {self.property_id}>'


class D_Passport(Base):
    __table__ = Table('d_passport', Base.metadata, autoload=True, autoload_with=engine)

    def __init__(self, passport_number: Optional[str], issued_by: Optional[str], issued_date: Optional[datetime]):
        self.passport_number = passport_number
        self.issued_by = issued_by
        self.issued_date = issued_date

    def __repr__(self):
        return f'<D_Passport {self.passport_id}>'


class D_OtherLink(Base):
    __table__ = Table('d_other_link', Base.metadata, autoload=True, autoload_with=engine)

    def __init__(self, site_id: int, value: Optional[str]):
        self.site_id = site_id
        self.value = value

    def __repr__(self):
        return f'<D_OtherLink {self.other_link_id} (site_id={self.site_id})>'


class D_Education(Base):
    __table__ = Table('d_education', Base.metadata, autoload=True, autoload_with=engine)

    def __init__(self, place_name: Optional[str], type_name: Optional[str], end_year: Optional[str]):
        self.place_name = place_name
        self.type_name = type_name
        self.end_year = end_year

    def __repr__(self):
        return f'<D_Education {self.education_id}>'


class D_ContactType(Base):
    __table__ = Table('d_contact_type', Base.metadata, autoload=True, autoload_with=engine)

    def __init__(self, contact_type_name: str):
        self.contact_type_name = contact_type_name

    def __repr__(self):
        return f'<D_ContactType {self.contact_type_id} ({self.contact_type_name})>'


class D_ContactCategory(Base):
    __table__ = Table('d_contact_category', Base.metadata, autoload=True, autoload_with=engine)

    def __init__(self, category_name: str):
        self.category_name = category_name

    def __repr__(self):
        return f'<D_ContactCategory {self.contact_category_id} ({self.category_name})>'


class D_Contact(Base):
    __table__ = Table('d_contact', Base.metadata, autoload=True, autoload_with=engine)

    def __init__(self, value: str, contact_category_id: int, contact_type_id: int):
        self.value = value
        self.contact_category_id = contact_category_id
        self.contact_type_id = contact_type_id

    def __repr__(self):
        return f'<D_Contact {self.contact_id} ({self.value})>'


class D_Business(Base):
    __table__ = Table('d_business', Base.metadata, autoload=True, autoload_with=engine)

    def __init__(self, kved: Optional[str], address_id: Optional[int], business_type: Optional[str],
                 edrpou: Optional[str], status_name: Optional[str]):
        self.kved = kved
        self.address_id = address_id
        self.business_type = business_type
        self.edrpou = edrpou
        self.status_name = status_name

    def __repr__(self):
        return f'<D_Business {self.business_id}>'


class D_Address(Base):
    __table__ = Table('d_address', Base.metadata, autoload=True, autoload_with=engine)

    def __init__(self, address_region: Optional[str], address_index: Optional[str], address_city: Optional[str],
                 address_street: Optional[str], address_building: Optional[str], address_apartment: Optional[str],
                 address_description: Optional[str], address_house: Optional[str], address_street_type: Optional[str],
                 address_raion: Optional[str]):
        self.address_region = address_region
        self.address_index = address_index
        self.address_city = address_city
        self.address_street = address_street
        self.address_building = address_building
        self.address_apartment = address_apartment
        self.address_description = address_description
        self.address_house = address_house
        self.address_street_type = address_street_type
        self.address_raion = address_raion

    def __repr__(self):
        return f'<D_Address {self.address_id}>'
