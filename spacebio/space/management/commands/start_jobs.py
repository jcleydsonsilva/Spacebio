from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, DjangoJob, register_events
from space.jobs import fetch_and_insert_news_job, fetch_and_insert_launches_job
import logging

class Command(BaseCommand):
    help = 'Starts the job scheduler'

    def handle(self, *args, **kwargs):
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)

        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), 'default')

        def remove_job_if_exists(job_id):
            try:
                existing_job = DjangoJob.objects.get(id=job_id)
                existing_job.delete()
                print(f"Removed existing job with ID '{job_id}'.")
            except DjangoJob.DoesNotExist:
                pass

        remove_job_if_exists('fetch_and_insert_news_job')
        remove_job_if_exists('fetch_and_insert_launches_job')

        scheduler.add_job(fetch_and_insert_news_job, 'interval', hours=6, id='fetch_and_insert_news_job')
        scheduler.add_job(fetch_and_insert_launches_job, 'interval', hours=6, id='fetch_and_insert_launches_job')

        register_events(scheduler)
        scheduler.start()

        print("Scheduled jobs:")
        jobs = scheduler.get_jobs()
        for job in jobs:
            print(f"Job ID: {job.id}, Next Run Time: {job.next_run_time}")

        fetch_and_insert_news_job()
        fetch_and_insert_launches_job()
