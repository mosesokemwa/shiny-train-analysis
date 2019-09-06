from jobs.models import AbstractModel
from django.db import models
from django.conf import settings

class CanvasOauthToken(AbstractModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='canvas_oauth2_token',
    )
    canvas_id = models.CharField(max_length=255, unique = True)
    access_token = models.TextField(unique=True)
    refresh_token = models.TextField()
    expires = models.DateTimeField()

    class Meta:
        db_table="canvas_oauth_token"
