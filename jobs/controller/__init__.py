from django.views import View
from django.http import JsonResponse
from jobs.entities.JobListing import JobListing

class JobListingView(View):
    def get(request,*args, **kwargs):
        return JsonResponse({"data":[ i.meta for i in JobListing.objects.all()]})
