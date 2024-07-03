from django.core.management.base import BaseCommand
import requests
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from space.models import *
from urllib.parse import urlencode

class Command(BaseCommand):
    help = 'Fetch and save news data from API'

    def handle(self, *args, **kwargs):
        script_name = 'fetch_and_insert_news'
        execution_log = ExecutionLog.objects.filter(script_name=script_name).first()
        last_executed = execution_log.last_executed if execution_log else None

        base_url = 'https://api.spaceflightnewsapi.net/v4/articles'
        params = {}
        if last_executed:
            params['last_updated__gt'] = last_executed.isoformat()

        url = base_url + '?' + urlencode(params)

        total_inserted = 0
        errors = []
        
        while url:
            try:
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                
                for item in data['results']:
                    try:
                        launch = None
                        launch_data = item.get('launches')
                        if launch_data and isinstance(launch_data, list):
                            launch_info = launch_data[0]  # Verificar se há pelo menos um elemento na lista
                            launch_id = launch_info.get('launch_id')
                            if launch_id:
                                launch = Launch.objects.filter(launch_id=launch_id).first()

                        News.objects.update_or_create(
                            title=item['title'],
                            defaults={
                                'url': item['url'],
                                'image_url': item.get('image_url', ''),
                                'news_site': item.get('news_site', ''),
                                'summary': item.get('summary', ''),
                                'published_at': parse_datetime(item['published_at']),
                                'updated_at': parse_datetime(item['updated_at']),
                                'featured': item.get('featured', False),
                                'launch': launch,
                            }
                        )
                        total_inserted += 1
                   
                    except Exception as e:
                        errors.append((item, e))
                
                url = data.get('next')
            
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f'Error making the request: {e}'))
        
        # Atualizar o timestamp da última execução
        if execution_log:
            execution_log.last_executed = timezone.now()
            execution_log.save()
        else:
            ExecutionLog.objects.create(script_name=script_name)

        self.stdout.write(self.style.SUCCESS(f'Finished! {total_inserted} news inserted.'))
        
        if errors:
            self.stdout.write(self.style.ERROR('Errors encountered during processing:'))
            for item, error in errors:
                self.stdout.write(self.style.ERROR(f'Item with error: {item}'))
                self.stdout.write(self.style.ERROR(f'Error message: {error}'))
