from django.db import models
from user.models import User

class Storage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    files = models.FileField(upload_to="storage/%Y/%m/%d")
    urls = models.URLField(max_length=220, unique=True, blank=True, db_index=True)
    deskipsi = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    kunci = models.CharField(max_length=100)

    def __str__(self):
        return self.user.email