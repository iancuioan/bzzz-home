from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    content = models.TextField("Feedback", max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback de la {self.user.username} - {self.created_at.date()}"