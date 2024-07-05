from django.apps import AppConfig

class SpaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'space'
    
    def ready(self):
        from apscheduler.schedulers.background import BackgroundScheduler
        from django_apscheduler.jobstores import DjangoJob, DjangoJobStore, register_events
        from .jobs import fetch_and_insert_news_job, fetch_and_insert_launches_job
        import logging
        # Configurar o logger
        logging.basicConfig()
        logging.getLogger('apscheduler').setLevel(logging.DEBUG)

        # Inicializar o scheduler
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Função auxiliar para remover jobs existentes
        def remove_job_if_exists(job_id):
            try:
                existing_job = DjangoJob.objects.get(id=job_id)
                existing_job.delete()
                print(f"Removed existing job with ID '{job_id}'.")
            except DjangoJob.DoesNotExist:
                pass

        # Remover jobs existentes
        remove_job_if_exists('fetch_and_insert_news_job')
        remove_job_if_exists('fetch_and_insert_launches_job')

        # Adicionar e executar jobs
        scheduler.add_job(fetch_and_insert_news_job, 'interval', hours=6, id='fetch_and_insert_news_job')
        scheduler.add_job(fetch_and_insert_launches_job, 'interval', hours=6, id='fetch_and_insert_launches_job')

        # Registrar eventos e iniciar o scheduler
        register_events(scheduler)
        scheduler.start()

        # Executar jobs imediatamente
        fetch_and_insert_news_job()
        fetch_and_insert_launches_job()
