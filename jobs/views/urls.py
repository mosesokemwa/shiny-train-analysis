from django.urls import path
from jobs.views.JobsView import JobsView
from jobs.views.TechnologiesView import TechnologiesView

urlpatterns=[
    path("jobs",JobsView.as_view(),name="jobs-view"),
    path("tags",TechnologiesView.as_view(),name="tags-view"),
]