from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_question = models.TextField(max_length=225)
    bot_response = models.TextField(max_length=225)
    status = models.BooleanField(True)
    date = models.DateField(auto_now_add=True)