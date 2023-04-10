from django.db import models

class ExceptionTracker(models.Model):
    occured = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    exception = models.CharField(max_length=300)
    unread = models.BooleanField(default=True)

    class Meta:ordering = ['-occured']
    def __str__(self): return self.title

    @classmethod
    def get_exceptions(cls): return cls.objects.filter()

    @classmethod
    def get_unread_exceptions(cls): return cls.objects.filter(unread=True)
