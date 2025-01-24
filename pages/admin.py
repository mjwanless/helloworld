from django.contrib import admin

from .models import ToDoList
admin.site.register(ToDoList)

from .models import Item
admin.site.register(Item)