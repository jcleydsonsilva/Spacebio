from django.core.management import call_command

def fetch_and_insert_launches_job():
    call_command('fetch_and_insert_launches')
    
def fetch_and_insert_news_job():
    call_command('fetch_and_insert_news')
