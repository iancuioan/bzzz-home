from django.contrib import admin
from .models import House, Todo, Operatiune, Pastoral

# Register your models here.
admin.site.register(House)
admin.site.register(Todo)
admin.site.register(Operatiune)
admin.site.register(Pastoral)