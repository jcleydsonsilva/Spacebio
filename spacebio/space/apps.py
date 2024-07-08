import os
from django.apps import AppConfig

class SpaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'space'
    
    def ready(self):
        
        # This condition ensures that the tasks will not be executed every time the server
        # updates due to the modification of any file, but only when the server starts for the
        # first time.
        if os.environ.get('RUN_MAIN') != 'true':
            from apscheduler.schedulers.background import BackgroundScheduler
            from django_apscheduler.jobstores import DjangoJob, DjangoJobStore, register_events
            from .jobs import fetch_and_insert_news_job, fetch_and_insert_launches_job
            import logging
            # Configure the logger
            logging.basicConfig(level=logging.DEBUG)
            logging.getLogger('apscheduler').setLevel(logging.DEBUG)

            # Initialize the scheduler
            scheduler = BackgroundScheduler()
            scheduler.add_jobstore(DjangoJobStore(), "default")

            # Auxiliary function to remove existing jobs
            def remove_job_if_exists(job_id):
                try:
                    existing_job = DjangoJob.objects.get(id=job_id)
                    existing_job.delete()
                    print(f"Removed existing job with ID '{job_id}'.")
                except DjangoJob.DoesNotExist:
                    pass

            # Remove existing jobs
            remove_job_if_exists('fetch_and_insert_news_job')
            remove_job_if_exists('fetch_and_insert_launches_job')

            # Add and execute jobs
            scheduler.add_job(fetch_and_insert_news_job, 'interval', hours=6, id='fetch_and_insert_news_job')
            scheduler.add_job(fetch_and_insert_launches_job, 'interval', hours=6, id='fetch_and_insert_launches_job')

            # Register events and start the scheduler
            register_events(scheduler)
            scheduler.start()

            # Execute jobs immediately
            fetch_and_insert_news_job()
            fetch_and_insert_launches_job()

            # Print scheduled jobs
            jobs = scheduler.get_jobs()
            print("Scheduled jobs:")
            for job in jobs:
                print(f"Job ID: {job.id}, Next Run Time: {job.next_run_time}")