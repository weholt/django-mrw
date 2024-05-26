from django.db import models


class Prompt(models.Model):
    name = models.CharField(max_length=100)
    prompt = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
