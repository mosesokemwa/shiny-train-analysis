import abc
import datetime
import operator
from functools import reduce
from django.conf import settings
from django.db.models import Q
from jobs.models import JobListing
from jobs.services.mailer.mail_template_render import RenderjinjaMailTemplate
from jobs.services.mailer.sendgrid_mailer import SendGridMailer

class AbstractJobsMailer(abc.ABC):
    @abc.abstractmethod
    def send_weekly_jobs_reports(self):
        raise NotImplementedError("Not Implemented")

class JobsMailer(AbstractJobsMailer):

    render =  RenderjinjaMailTemplate()
    mailer =  SendGridMailer()
    def __init__(self, *args, **kwargs):
        pass

    def send_weekly_jobs_reports(self):
        today = datetime.date.today()
        seven_days_ago = today - datetime.timedelta(days = 7)
        seven_days_after = today + datetime.timedelta(days = 7)
        # querysets
        new_jobs = JobListing.objects.filter(Q(date_posted__gte=seven_days_ago)) 
        new_jobs_filtered_by_titles = new_jobs.filter(reduce(operator.or_, (Q(title__icontains=x) for x in ['developer', 'engineer'])))
        jobs_new = []
        for job in new_jobs_filtered_by_titles:
            jobs_new.append({
                "date_posted":job.date_posted.strftime("%d %b %Y"),
                "title":job.title,
                "company":job.hiring_organization.name if job.hiring_organization else "",
                "city":job.city,
                "link":job.url
            }) 
            
        new_company_jobs ={}
        for job in new_jobs:
            try:
                new_company_jobs[job.hiring_organization.name].append({
                    "deadline":job.valid_to.strftime("%d %b %Y"),
                    "title":job.title,
                    "city":job.city,
                    "link":job.url  
                })
            except KeyError:
                new_company_jobs[job.hiring_organization.name]= [{
                    "deadline":job.valid_to.strftime("%d %b %Y"),
                    "title":job.title,
                    "city":job.city,
                    "link":job.url  
                }]
        new_company_jobs2={}
        for company, jobs in new_company_jobs.items():
            if len(jobs)>=3:
                new_company_jobs2[company]=jobs
        new_company_jobs=new_company_jobs2
        upcoming_deadline_jobs = JobListing.objects.filter(Q(valid_to__gte=today),Q(valid_to__lte=seven_days_after))
        upcoming_deadline_jobs = upcoming_deadline_jobs.filter(reduce(operator.or_, (Q(title__icontains=x) for x in ['developer', 'engineer'])))
        jobs_upcoming_deadlines = []
        for job in upcoming_deadline_jobs:
            jobs_upcoming_deadlines.append({
                "deadline":job.valid_to.strftime("%d %b %Y"),
                "title":job.title,
                "company":job.hiring_organization.name if job.hiring_organization else "",
                "city":job.city,
                "link":job.url
            })
        context = {
            "jobs_upcoming_deadlines":jobs_upcoming_deadlines,
            "jobs_new":jobs_new,
            "new_company_jobs":new_company_jobs,
            "today":today.strftime("%d %b %Y"),
            "seven_before":seven_days_ago.strftime("%d %b %Y"),
            "seven_after":seven_days_after.strftime("%d %b %Y")
        }
        html_content=self.render.parse_mail_html_mail_template("emails/weekly_report.html", context)
        from_email = settings.WEEKLY_JOBS_REPORT_SENDERS_EMAIL
        to_emails = settings.WEEKLY_JOBS_REPORT_SENDERS_RECEPEINTS
        print(to_emails)
        self.mailer.send(from_email,to_emails, "Weekly Jobs Board Report {td}".format(td=today.strftime("%d %b %Y")), html_content, message_type="html")
