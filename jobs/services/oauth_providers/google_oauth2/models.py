from django.db import models
from jobs.models import AbstractModel
from django.conf import settings

class GoogleOuth2AccessToken(AbstractModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='google_oauth2_token',
    )
    email = models.EmailField(max_length=255, unique = True)
    access_token = models.TextField(unique=True)
    refresh_token = models.TextField()
    expires = models.DateTimeField()

    class Meta:
        db_table="google_oauth_token"
