from .core import Item
from django.db import models
from django.utils.translation import gettext_lazy as _

class DocumentType(models.Model):

    class Type(models.TextChoices):
        DNI = "DNI", _("DNI")
        NIE = "NIE", _("DNI")
        NIF = "NIF",_( "NIF")        
        PASSPORT = "PASSPORT", _("Passport")

    value = models.CharField(max_length=20, choices=Type.choices, default=Type.DNI)

class LicenseType(models.Model):

    class Type(models.TextChoices):
        AUTO = "Autonomical", _("Autonomical")
        NATI = "National", _("National")        
        FORE = "Foreign", _("Foreign")

    value = models.CharField(max_length=20, choices=Type.choices, default=Type.AUTO)


class Club(Item):
    name = models.CharField(max_length=125)
    document_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT)
    document_id = models.CharField(max_length=20)
    adr_street_type = models.CharField(max_length=255)
    adr_street_name = models.CharField(max_length=255)
    adr_street_number = models.CharField(max_length=255)    
    adr_apartment_floor = models.CharField(max_length=255)    
    adr_apartment_number = models.CharField(max_length=255)
    adr_postalcode = models.CharField(max_length=255)
    adr_city =  models.CharField(max_length=255)
    adr_council = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    web = models.CharField(max_length=255)


class Competition(Item):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    date_start = models.DateField()
    date_end = models.DateField()

class DisciplineCategory(Item):
    name = models.CharField(max_length=125)


class Discipline(Item):
    category = models.ForeignKey(DisciplineCategory, on_delete=models.PROTECT)
    name = models.CharField(max_length=125)

class Athlet(Item):
    nickname = models.CharField(max_length=125)
    first_name = models.CharField(max_length=125)
    last_name_1 = models.CharField(max_length=125)
    last_name_2 = models.CharField(max_length=125)
    document_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT)
    document_id = models.CharField(max_length=20)
    license_type = models.ForeignKey(LicenseType, on_delete=models.PROTECT)
    license_id = models.CharField(max_length=20)
    adr_street_type = models.CharField(max_length=255)
    adr_street_name = models.CharField(max_length=255)
    adr_street_number = models.CharField(max_length=255)    
    adr_apartment_floor = models.CharField(max_length=255)    
    adr_apartment_number = models.CharField(max_length=255)
    adr_postalcode = models.CharField(max_length=255)
    adr_city =  models.CharField(max_length=255)
    adr_council = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    phone_mobile = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    date_of_birth = models.CharField(max_length=255)
    date_start_athletics = models.CharField(max_length=255)
    date_start_santi = models.CharField(max_length=255)    
    sex = models.CharField(max_length=255)
    discipline_category = models.ManyToManyField(DisciplineCategory)    
    club = models.ForeignKey(Club, on_delete=models.PROTECT)
    photo = models.ImageField()

class AthletDetail(Item):
    athlet = models.ForeignKey(Athlet, on_delete=models.CASCADE)
    height = models.CharField(max_length=255)
    weight = models.CharField(max_length=255)

