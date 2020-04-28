#!/usr/bin/python3
from models import storage
from models.state import State


my_model = State()
my_model.name = "Alabama"
my_model.save()

my_model2 = State()
my_model2.name = "Arizona"
my_model2.save()

my_model3 = State()
my_model3.name = "Colorado"
my_model3.save()

my_model4 = State()
my_model4.name = "Florida"
my_model4.save()

