from django.core.management.base import BaseCommand
from jobs.services.mailer.jobs_report_mailer import JobsMailer
class Command(BaseCommand):
    service=JobsMailer()
    help = 'Send weekly report'

    def add_arguments(self, parser):
        parser.add_argument("option",type=str,help="defaults")
        
    def handle(self, *args, **kwargs):
        option=kwargs["option"]
        if option=="defaults":
            self.service.send_weekly_jobs_reports()
