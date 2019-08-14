from django.urls import path
from jobs.views.JobsView import JobsView
from jobs.views.TechnologiesView import TechnologiesView
from jobs.views.ServerSyncJobsView import ServerSyncJobsView
from jobs.views.ProvidersView import ProvidersViews
urlpatterns=[
    path("jobs",JobsView.as_view(),name="jobs-view"),
    path("tags",TechnologiesView.as_view(),name="tags-view"),
    path("server-sync-jobs", ServerSyncJobsView.as_view(), name = "server-sync-jobs-view"),
    path("providers",ProvidersViews.as_view(), name="providers-view"),
]