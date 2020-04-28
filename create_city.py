#!/usr/bin/python3
from models import storage
from models.city import City


my_model = City()
my_model.name = "Akron"
my_model.state_id = "f65237d7-04e3-4667-9a05-b48049c913c0"
my_model.save()

my_model2 = City()
my_model2.name = "Babbie"
my_model2.state_id = "f65237d7-04e3-4667-9a05-b48049c913c0"
my_model2.save()

my_model3 = City()
my_model3.name = "Calera"
my_model3.state_id = "f65237d7-04e3-4667-9a05-b48049c913c0"
my_model3.save()

my_model4 = City()
my_model4.name = "Fairfield"
my_model4.state_id = "f65237d7-04e3-4667-9a05-b48049c913c0"
my_model4.save()

my_model5 = City()
my_model5.name = "Fairfield"
my_model5.state_id = "f65237d7-04e3-4667-9a05-b48049c913c0"
my_model5.save()

