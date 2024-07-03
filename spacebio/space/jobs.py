from django.core.management import call_command
import logging

    
def fetch_and_insert_news_job():
    call_command('fetch_and_insert_news')
