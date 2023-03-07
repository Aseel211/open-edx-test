from django.db import models
from django.contrib.auth.models import User

class UserGreeting(models.Model):
    """
    User Greeting Model
    """
    user = models.ForeignKey(User, db_index=True, related_name="user", on_delete=models.CASCADE)
    greeting_word = models.CharField(max_length=255, db_index=True)


