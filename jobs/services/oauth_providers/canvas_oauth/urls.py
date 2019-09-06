from django.urls import path
from .views import CanvasLoginApiView

urlpatterns = [
    path("canvas/login",CanvasLoginApiView.as_view(),name="canvas-login")
]
