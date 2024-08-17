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
            "https://lldev.thespacedevs.com/2.2.0/launch/previous/?mode=detailed",
            "https://lldev.thespacedevs.com/2.2.0/launch/upcoming/?mode=detailed",
            "https://lldev.thespacedevs.com/2.2.0/launch/?mode=detailed"
        ]

        total_inserted = 0
        total_updated = 0
        script_name = 'fetch_and_insert_launches'



        for url in urls:
            
            while url: 
                
                try:
                    response = requests.get(url)
                    response.raise_for_status()  # Raise an exception for bad status codes
                    logger.debug(f'{Fore.MAGENTA}Fetched data from API successfully for {url}{Style.RESET_ALL}')

                    data = response.json()

                    for launch_data in data['results']:
                        try:
                            # Status
                            status_data = launch_data['status']
                            status, _ = LaunchStatus.objects.get_or_create(
                                id = status_data['id'],
                                name=status_data['name'],
                                defaults={'abbrev': status_data['abbrev'], 'description': status_data['description']}
                            )

                            # NetPrecision
                            net_precision_data = launch_data.get('net_precision', {})
                            net_precision, _ = NetPrecision.objects.get_or_create(
                                id=net_precision_data.get('id', 'Unknown'),
                                name=net_precision_data.get('name', 'Unknown'),
                                defaults={'abbrev': net_precision_data.get('abbrev', ''), 'description': net_precision_data.get('description', '')}
                            )
                            '''
                            # LaunchServiceProvider
                            lsp_data = launch_data['launch_service_provider']
                            print ('---------------------------')
                            print (lsp_data)
                            print ('_--------------------------')
                            launch_service_provider, _ = LaunchServiceProvider.objects.get_or_create(
                                id=lsp_data['id'],
                                name=lsp_data['name'],
                                defaults={'type': lsp_data['type'], 'description': '', 'url': lsp_data['url']}
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
                            '''
                            # Orbit
                            orbit_data = launch_data['mission']['orbit']
                            orbit, _ = Orbit.objects.get_or_create(
                                id=orbit_data['id'],
                                name=orbit_data['name'],
                                defaults={'abbrev': orbit_data['abbrev']}
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
                                id=location_data['id'],
                                name=location_data['name'],
                                defaults={'country_code': location_data['country_code'], 'map_image': location_data['map_image'], 'timezone_name': location_data['timezone_name'], 'total_launch_count': location_data['total_launch_count'], 'total_landing_count': location_data['total_landing_count'], 'description': location_data.get('description', '')}
                            )

                            # Pad (handling nullable map_url)
                            pad_data = launch_data['pad']
                            pad, _ = Pad.objects.get_or_create(
                                id=pad_data['id'],
                                name=pad_data['name'],
                                defaults={'description': pad_data.get('description', ''),
                                        'info_url': pad_data.get('info_url', None),
                                        'wiki_url': pad_data.get('wiki_url', None),
                                        'map_url': pad_data.get('map_url', '') or '',  # Handling nullable map_url
                                        'latitude': pad_data.get('latitude', None),
                                        'longitude': pad_data.get('longitude', None),
                                        'country_code':pad_data.get('country_code', None),
                                        'map_image': pad_data.get('map_image', None),
                                        'total_launch_count': pad_data['total_launch_count'],
                                        'orbital_launch_attempt_count':pad_data['orbital_launch_attempt_count'],
                                        'agency_id_id':pad_data.get('agency_id', None),
                                        'location_id':location_data['id']
                                        }
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

                            # # VidURL
                            # try:
                            #     vidurl_data = launch_data['vidURLs'][0]
                            # except:
                            #     vidurl_data = launch_data['vidURLs']
                                
                            # vid, _ = VidURL.objects.get_or_create(
                            #     launch=launch,
                            #     defaults={
                            #         'priority': vidurl_data['priority'] or 0,
                            #         'source': vidurl_data['source'],
                            #         'publisher': vidurl_data['publisher'],
                            #         'title': vidurl_data['title'],
                            #         'description': vidurl_data['description'],
                            #         'feature_image': vidurl_data['feature_image'],
                            #         'url': vidurl_data['url'],
                            #         'type': vidurl_data['type'],
                            #         'language': vidurl_data['language'],
                            #         'start_time': normalize_datetime(vidurl_data['start_time']),
                            #         'end_time': normalize_datetime(vidurl_data['end_time']),
                            #     }
                            # )
                            
                            
                            # Inside your loop processing each launch_data
                            for vidurl_data in launch_data.get('vidURLs', []):  # Iterate over each vidURL item
                                try:
                                    # Extract data with default values where necessary
                                    priority = int(vidurl_data.get('priority', 0))
                                    source = vidurl_data.get('source', '')
                                    publisher = vidurl_data.get('publisher', '')
                                    title = vidurl_data.get('title', '')
                                    description = vidurl_data.get('description', '')
                                    feature_image = vidurl_data.get('feature_image', '')
                                    url = vidurl_data.get('url', '')
                                    vid_type = vidurl_data.get('type', '')
                                    language_data = vidurl_data.get('language', {})
                                    language = language_data.get('code', '') if language_data else ''
                                    start_time = normalize_datetime(vidurl_data.get('start_time'))
                                    end_time = normalize_datetime(vidurl_data.get('end_time'))
                                    
                                    # Create or get the VidURL object
                                    vid, _ = VidURL.objects.get_or_create(
                                        launch=launch,
                                        defaults={
                                            'priority': priority,
                                            'source': source,
                                            'publisher': publisher,
                                            'title': title,
                                            'description': description,
                                            'feature_image': feature_image,
                                            'url': url,
                                            'type': vid_type,
                                            'language': language,
                                            'start_time': start_time,
                                            'end_time': end_time,
                                        }
                                    )
                                    logger.debug(f"Inserted or updated VidURL: {url}")

                                except Exception as e:
                                    logger.error(f"Error processing VidURL: {vidurl_data}. Error: {e}")
                            
                                                    
                            
                            # InfoURL
                            # try:
                            #     infourl_data = launch_data['infoURLs'][0]
                            # except:
                            #     infourl_data = launch_data['infoURLs']
                                
                            # info, _ = InfoURL.objects.get_or_create(
                            #     launch=launch,
                            #     defaults={
                            #         'priority': infourl_data['priority'] or 0,
                            #         'source': infourl_data['source'],
                            #         'title': infourl_data['title'],
                            #         'description': infourl_data['description'],
                            #         'feature_image': infourl_data['feature_image'],
                            #         'url': infourl_data['url'],
                            #         'type': infourl_data['type'],
                            #         'language': infourl_data['language'],
                            #     }
                            # )

                            # Inside your loop processing each launch_data
                            for infourl_data in launch_data.get('infoURLs', []):  # Iterate over each infoURL item
                                try:
                                    # Extract data with default values where necessary
                                    priority = int(infourl_data.get('priority', 0))
                                    source = infourl_data.get('source', '')
                                    title = infourl_data.get('title', '')
                                    description = infourl_data.get('description', '')
                                    feature_image = infourl_data.get('feature_image', '')
                                    url = infourl_data.get('url', '')
                                    infotype = infourl_data.get('type', '')
                                    language_data = infourl_data.get('language', {})
                                    language = language_data.get('code', '') if language_data else ''
                                    
                                    # Create or get the InfoURL object
                                    info, _ = InfoURL.objects.get_or_create(
                                        launch=launch,
                                        defaults={
                                            'priority': priority,
                                            'source': source,
                                            'title': title,
                                            'description': description,
                                            'feature_image': feature_image,
                                            'url': url,
                                            'type': infotype,
                                            'language': language,
                                        }
                                    )
                                    logger.debug(f"Inserted or updated InfoURL: {url}")

                                except Exception as e:
                                    logger.error(f"Error processing InfoURL: {infourl_data}. Error: {e}")



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
                                    logger.debug(f"{Fore.BLUE}Updated fields for launch {launch.name}{Style.RESET_ALL}")
                                    launch.save()
                                    total_updated += 1
                                    self.stdout.write(self.style.SUCCESS(f'Updated existing launch: {launch_data["name"]}'))

                        except (RequestException, JSONDecodeError, Exception) as e:
                            logger.error(f'{Fore.RED}Error processing launch {launch_data["name"]}: {str(e)}', exc_info=True)

                except RequestException as e:
                    logger.error(f'{Fore.RED}Error making API request: {str(e)}{Style.RESET_ALL}')

            logger.debug(f'{Fore.BLUE}Total launches updated: {total_updated}{Style.RESET_ALL}')
            logger.debug(f'{Fore.GREEN}Total launches inserted: {total_inserted}{Style.RESET_ALL}')
