from django.db import models

class Newsletter_User(models.Model):
    email = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
    def __str__(self):
        return self.email