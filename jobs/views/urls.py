from django.urls import path
from jobs.views.JobsView import JobsView

urlpatterns=[
    path("jobs",JobsView.as_view(),name="jobs-view"),
]