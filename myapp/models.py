from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    name = models.CharField(max_length=100)  # Název položky
    rocnik = models.IntegerField(default=2000)  # Ročník
    description = models.TextField()  # Popis turnaje

    def __str__(self):
        return self.name

class Comment(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Komentář od {self.user.username} k {self.item.name}"
