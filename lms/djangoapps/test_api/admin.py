from django.contrib import admin
from .models import UserGreeting


@admin.register(UserGreeting)
class UserGreetingAdmin(admin.ModelAdmin):
    pass