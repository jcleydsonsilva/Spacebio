from django.core.management.base import BaseCommand
import requests
from django.utils.dateparse import parse_datetime
from space.models import ExecutionLog, News, Launch
import logging
from colorama import Fore, Style
from datetime import datetime, timezone

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class Command(BaseCommand):
    help = 'Fetch and save news data from API'

    def handle(self, *args, **kwargs):
        script_name = 'fetch_and_insert_news'
        base_url = 'https://api.spaceflightnewsapi.net/v4/articles/'

        # Fetch the last execution log
        last_execution_log = ExecutionLog.objects.filter(script_name=script_name, url=base_url).first()
        if last_execution_log:
            last_executed = last_execution_log.last_executed
        else:
            last_executed = None

        # If there was a previous execution, add the timestamp to the URL
        if last_executed:
            last_executed_str = last_executed.isoformat().replace("+00:00", "Z")
            url = f'{base_url}?updated_at_gte={last_executed_str}'
        else:
            url = base_url

        logger.info(f'{Fore.MAGENTA}Fetching data updated after {last_executed}')
        logger.info(f'{Fore.MAGENTA}Fetching data from {url}')

        total_inserted = 0
        total_updated = 0
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
                            launch_info = launch_data[0]  # Ensure there's at least one element
                            launch_id = launch_info.get('id')
                            if launch_id:
                                launch = Launch.objects.filter(launch_id=launch_id).first()
                                
                        news, created = News.objects.update_or_create(
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

                        if created:
                            total_inserted += 1
                            logger.info(f'{Fore.GREEN}Inserted new news: {item["title"]}{Style.RESET_ALL}')
                        else:
                            total_updated += 1
                            logger.info(f'{Fore.BLUE}Updated existing news: {item["title"]}{Style.RESET_ALL}')

                    except Exception as e:
                        errors.append((item, e))
                        logger.error(f'{Fore.RED}Error processing news {item["title"]}: {e}{Style.RESET_ALL}')

                url = data.get('next', None)

            except requests.exceptions.RequestException as e:
                logger.error(f'{Fore.RED}Error making the request: {e}{Style.RESET_ALL}')
                break  # Exit loop if there is a request error

        logger.info(f'{Fore.GREEN}Finished! {total_inserted} news inserted and {total_updated} news updated.{Style.RESET_ALL}')

        if errors:
            logger.error(f'{Fore.RED}Errors encountered during processing:{Style.RESET_ALL}')
            for item, error in errors:
                logger.error(f'{Fore.RED}Item with error: {item}{Style.RESET_ALL}')
                logger.error(f'{Fore.RED}Error message: {error}{Style.RESET_ALL}')

        # Update or create the execution log
        ExecutionLog.objects.update_or_create(
            script_name=script_name,
            url=base_url,
            defaults={'last_executed': datetime.now(timezone.utc)}
        )
