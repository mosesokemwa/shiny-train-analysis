from django.urls import path
from jobs.views.JobsView import JobsView
from jobs.views.TechnologiesView import TechnologiesView
from jobs.views.ServerSyncJobsView import ServerSyncJobsView
from jobs.views.ProvidersView import ProvidersViews
from jobs.views.JobsLocationView import JobsLocationView
from jobs.views.UserView import UserView
urlpatterns=[
    path("jobs",JobsView.as_view(),name="jobs-view"),
    path("tags",TechnologiesView.as_view(),name="tags-view"),
    path("server-sync-jobs", ServerSyncJobsView.as_view(), name = "server-sync-jobs-view"),
    path("providers",ProvidersViews.as_view(), name="providers-view"),
    path("locations",JobsLocationView.as_view(),name="jobs-location-view"),
    path("user",UserView.as_view(),name="user-view"),
]