from django.contrib import admin
from .models import *
# Register your models here.
models = [  
    User,
    Post,
    Profile,
    Follow 
]

for model in models:
    admin.site.register(model)
