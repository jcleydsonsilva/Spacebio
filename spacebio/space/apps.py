from django.apps import AppConfig


class SpaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'space'
    
    # def ready(self):        
    #     from apscheduler.schedulers.background import BackgroundScheduler
    #     from django_apscheduler.jobstores import DjangoJobStore, register_events
    #     from django_apscheduler.jobstores import DjangoJob
    #     import logging

    #     from .jobs import fetch_and_insert_news_job
        
    #     # Configurar o logger
    #     logging.basicConfig()
    #     logging.getLogger('apscheduler').setLevel(logging.DEBUG)

    #     # Inicializar o scheduler
    #     scheduler = BackgroundScheduler()
    #     scheduler.add_jobstore(DjangoJobStore(), "default")

    #     # Remover o job existente, se houver
    #     try:
    #         existing_job = DjangoJob.objects.get(id='fetch_and_insert_news_job')
    #         existing_job.delete()
    #         print(f"Removed existing job with ID 'fetch_and_insert_news_job'.")
    #     except DjangoJob.DoesNotExist:
    #         pass
        
    #     # Adicionar o job ao scheduler
    #     scheduler.add_job(fetch_and_insert_news_job, 'interval', hours=6, id='fetch_and_insert_news_job')

    #     # Registrar eventos e iniciar o scheduler
    #     register_events(scheduler)
    #     scheduler.start()
