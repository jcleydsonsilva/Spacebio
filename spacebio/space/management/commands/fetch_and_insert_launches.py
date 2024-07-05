import logging
import requests
from django.core.management.base import BaseCommand
from space.models import *
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, is_naive, now
from requests.exceptions import RequestException
from json.decoder import JSONDecodeError
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def normalize_datetime(dt_str):
    if dt_str:
        dt = parse_datetime(dt_str)
        if is_naive(dt):
            dt = make_aware(dt)
        return dt
    return None

def update_if_different(instance, field, value):
    current_value = getattr(instance, field)

    if isinstance(value, str) and 'T' in value and 'Z' in value:
        value = normalize_datetime(value)

    if current_value != value:
        
        logger.debug(f"{Fore.YELLOW}Updating field '{field}' from '{current_value}' to '{value}{Style.RESET_ALL}'")
        setattr(instance, field, value)
        return True
    return False

class Command(BaseCommand):
    help = 'Fetch and insert launch data from API'

    def handle(self, *args, **kwargs):
        urls = [
            "https://lldev.thespacedevs.com/2.2.0/launch/previous/",
            "https://lldev.thespacedevs.com/2.2.0/launch/upcoming/",
            "https://lldev.thespacedevs.com/2.2.0/launch/"
        ]

        total_inserted = 0
        total_updated = 0
        script_name = 'fetch_and_insert_launches'

        for url in urls:
            execution_log, created = ExecutionLog.objects.get_or_create(script_name=script_name, url=url)
            last_executed = execution_log.last_executed

            params = {}
            if last_executed:
                params['updated_after'] = last_executed.isoformat()

            try:
                response = requests.get(url, params=params)
                response.raise_for_status()  # Raise an exception for bad status codes
                logger.debug(f'{Fore.BLUE}Fetched data from API successfully for {url}{Style.RESET_ALL}')

                data = response.json()

                for launch_data in data['results']:
                    try:
                        # Status
                        status_data = launch_data['status']
                        status, _ = Status.objects.get_or_create(
                            name=status_data['name'],
                            defaults={'abbrev': status_data['abbrev'], 'description': status_data['description']}
                        )

                        # NetPrecision
                        net_precision_data = launch_data.get('net_precision', {})
                        net_precision, _ = NetPrecision.objects.get_or_create(
                            name=net_precision_data.get('name', 'Unknown'),
                            defaults={'abbrev': net_precision_data.get('abbrev', ''), 'description': net_precision_data.get('description', '')}
                        )

                        # LaunchServiceProvider
                        lsp_data = launch_data['launch_service_provider']
                        launch_service_provider, _ = LaunchServiceProvider.objects.get_or_create(
                            name=lsp_data['name'],
                            defaults={'type': lsp_data['type'], 'url': lsp_data['url'], 'description': ''}
                        )

                        # RocketConfiguration
                        rocket_config_data = launch_data['rocket']['configuration']
                        rocket_configuration, _ = RocketConfiguration.objects.get_or_create(
                            name=rocket_config_data['name'],
                            defaults={'family': rocket_config_data.get('family', ''),
                                      'full_name': rocket_config_data.get('full_name', ''),
                                      'variant': rocket_config_data.get('variant', ''),
                                      'url': rocket_config_data['url'],
                                      'description': ''}
                        )

                        # Rocket
                        rocket, _ = Rocket.objects.get_or_create(
                            configuration_id=rocket_configuration.id,
                            defaults={'description': ''}
                        )

                        # Orbit
                        orbit_data = launch_data['mission']['orbit']
                        orbit, _ = Orbit.objects.get_or_create(
                            name=orbit_data['name'],
                            defaults={'abbrev': orbit_data['abbrev'], 'description': ''}
                        )

                        # Mission (using mission ID as unique field)
                        mission_data = launch_data['mission']
                        mission, _ = Mission.objects.get_or_create(
                            id=mission_data['id'], 
                            defaults={'name': mission_data['name'],
                                      'description': mission_data['description'],
                                      'type': mission_data['type'],
                                      'orbit': orbit}
                        )

                        # Agencies
                        for agency_data in mission_data.get('agencies', []):
                            agency, _ = Agency.objects.get_or_create(
                                name=agency_data['name'],
                                defaults={'type': agency_data['type'], 'country_code': agency_data['country_code'], 'abbrev': agency_data['abbrev'], 'description': agency_data['description'], 'administrator': agency_data.get('administrator', ''), 'founding_year': agency_data.get('founding_year', ''), 'info_url': agency_data.get('info_url', ''), 'wiki_url': agency_data.get('wiki_url', ''), 'logo_url': agency_data.get('logo_url', ''), 'image_url': agency_data.get('image_url', '')}
                            )
                            mission.agencies.add(agency)

                        # Location
                        location_data = launch_data['pad']['location']
                        location, _ = Location.objects.get_or_create(
                            name=location_data['name'],
                            defaults={'country_code': location_data['country_code'], 'map_image': location_data['map_image'], 'timezone_name': location_data['timezone_name'], 'total_launch_count': location_data['total_launch_count'], 'total_landing_count': location_data['total_landing_count'], 'description': location_data.get('description', '')}
                        )

                        # Pad (handling nullable map_url)
                        pad_data = launch_data['pad']
                        pad, _ = Pad.objects.get_or_create(
                            name=pad_data['name'],
                            defaults={'location': location,
                                      'map_url': pad_data.get('map_url', '') or '',  # Handling nullable map_url
                                      'latitude': pad_data.get('latitude', None),
                                      'longitude': pad_data.get('longitude', None),
                                      'total_launch_count': pad_data['total_launch_count'],
                                      'description': pad_data.get('description', '') if pad_data.get('description', '') is not None else ''}
                        )


                        # Launch (handling duplicate slug)
                        launch, created = Launch.objects.get_or_create(
                            launch_id=launch_data['id'],
                            defaults={
                                'name': launch_data['name'],
                                'url': launch_data['url'],
                                'slug': launch_data['slug'],
                                'status': status,
                                'last_updated': normalize_datetime(launch_data['last_updated']),
                                'net': normalize_datetime(launch_data['net']),
                                'window_end': normalize_datetime(launch_data['window_end']),
                                'window_start': normalize_datetime(launch_data['window_start']),
                                'net_precision': net_precision,
                                'launch_service_provider': launch_service_provider,
                                'rocket': rocket,
                                'mission': mission,
                                'pad': pad,
                                'webcast_live': launch_data['webcast_live'],
                                'image': launch_data.get('image', ''),
                                'infographic': launch_data.get('infographic', '')
                            }
                        )

                        if created:
                            total_inserted += 1
                            self.stdout.write(self.style.SUCCESS(f'{Fore.GREEN}Inserted new launch: {launch_data["name"]}{Style.RESET_ALL}'))
                        else:
                            updated = False
                            fields_to_update = {
                                'name', 'url', 'status', 'last_updated', 'net', 'window_end',
                                'window_start', 'net_precision', 'launch_service_provider', 'rocket',
                                'mission', 'pad', 'webcast_live', 'image', 'infographic'
                            }

                            for field in fields_to_update:
                                if field in ['status', 'net_precision', 'launch_service_provider', 'rocket', 'mission', 'pad']:
                                    related_instance = locals()[field]
                                    updated |= update_if_different(launch, field, related_instance)
                                else:
                                    updated |= update_if_different(launch, field, launch_data.get(field))

                            if updated:
                                logger.debug(f"{Fore.YELLOW}Updated fields for launch {launch.name}{Style.RESET_ALL}")
                                launch.save()
                                total_updated += 1
                                self.stdout.write(self.style.SUCCESS(f'Updated existing launch: {launch_data["name"]}'))

                    except (RequestException, JSONDecodeError, Exception) as e:
                        logger.error(f'Error processing launch {launch_data["name"]}: {str(e)}', exc_info=True)

                # Update the last executed timestamp for the URL
                execution_log.last_executed = now()
                execution_log.save()

            except RequestException as e:
                logger.error(f'{Fore.RED}Error making API request: {str(e)}{Style.RESET_ALL}')

        logger.debug(f'{Fore.GREEN}Total inserted: {total_inserted}{Style.RESET_ALL}')
        logger.debug(f'{Fore.YELLOW}Total updated: {total_updated}{Style.RESET_ALL}')
