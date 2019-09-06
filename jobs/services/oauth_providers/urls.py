from django.urls import include
from jobs.services.oauth_providers.canvas_oauth.urls import urlpatterns as canvas_oauth2_urlpatterns
from jobs.services.oauth_providers.google_oauth2.urls import urlpatterns as google_oauth2_urlpatterns
urlpatterns = [
    
]

urlpatterns +=canvas_oauth2_urlpatterns
urlpatterns +=google_oauth2_urlpatterns
