from django.core.management.base import BaseCommand
import requests
from random import choice
from django.utils.dateparse import parse_datetime
from space.models import *

class Command(BaseCommand):
    help = 'Fetch and save launch data from API'

    def create_default_mission(self):
        # Cria uma missão padrão e orbita
        default_orbit, _ = Orbit.objects.get_or_create(
            name='Not Informed',
            defaults={'abbrev': 'NI'}
        )

        default_mission, _ = Mission.objects.get_or_create(
            name='Not Informed',
            defaults={
                'description': 'Mission not informed',
                'type': 'Not Informed',
                'orbit': default_orbit
            }
        )
        return default_mission, default_orbit

    def handle(self, *args, **kwargs):
        url = 'https://lldev.thespacedevs.com/2.2.0/launch/upcoming/'
        total_inserted = 0
        total_updated = 0
        errors = []

        while url:
            try:
                self.stdout.write(self.style.NOTICE(f'Fetching data from {url}'))
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f'Error fetching data from API: {e}'))
                break

            for item in data['results']:
                try:
                    self.stdout.write(self.style.NOTICE(f'Processing launch: {item["name"]}'))
                    launch, created = Launch.objects.update_or_create(
                        slug=item['slug'],
                        defaults={
                            'launch_id': item['id'],
                            'name': item['name'],
                            'url': item['url'],
                            'status': Status.objects.get_or_create(
                                name=item['status']['name'],
                                defaults={'abbrev': item['status']['abbrev'], 'description': item['status']['description']}
                            )[0],
                            'last_updated': parse_datetime(item['last_updated']),
                            'net': parse_datetime(item['net']),
                            'window_end': parse_datetime(item['window_end']),
                            'window_start': parse_datetime(item['window_start']),
                            'net_precision': NetPrecision.objects.get_or_create(
                                name=item.get('net_precision', {}).get('name', 'Default Net Precision Name'),
                                defaults={
                                    'abbrev': item.get('net_precision', {}).get('abbrev', ''), 
                                    'description': item.get('net_precision', {}).get('description', '')
                                }
                            )[0],
                            'launch_service_provider': LaunchServiceProvider.objects.get_or_create(
                                name=item['launch_service_provider']['name'],
                                defaults={'type': item['launch_service_provider']['type'], 'url': item['launch_service_provider']['url']}
                            )[0],
                            'rocket': Rocket.objects.get_or_create(
                                configuration=RocketConfiguration.objects.get_or_create(
                                    name=item['rocket']['configuration']['name'],
                                    defaults={
                                        'family': item['rocket']['configuration']['family'],
                                        'full_name': item['rocket']['configuration']['full_name'],
                                        'variant': item['rocket']['configuration']['variant'],
                                        'url': item['rocket']['configuration']['url']
                                    }
                                )[0]
                            )[0],
                            'mission': Mission.objects.get_or_create(
                                name=item.get('mission', {}).get('name', 'Not Informed'),
                                defaults={
                                    'description': item.get('mission', {}).get('description', 'Mission not informed'),
                                    'type': item.get('mission', {}).get('type', 'Not Informed'),
                                    'orbit': Orbit.objects.get_or_create(
                                        name=item.get('mission', {}).get('orbit', {}).get('name', 'Not Informed'),
                                        defaults={'abbrev': item.get('mission', {}).get('orbit', {}).get('abbrev', 'NI')}
                                    )[0]
                                }
                            )[0],
                            'pad': Pad.objects.get_or_create(
                                name=item['pad']['name'],
                                defaults={
                                    'location': Location.objects.get_or_create(
                                        name=item['pad']['location']['name'],
                                        defaults={
                                            'country_code': item['pad']['location']['country_code'],
                                            'map_image': item['pad']['location']['map_image'],
                                            'timezone_name': item['pad']['location']['timezone_name'],
                                            'total_launch_count': item['pad']['location']['total_launch_count'],
                                            'total_landing_count': item['pad']['location']['total_landing_count']
                                        }
                                    )[0],
                                    'map_url': item['pad']['map_url'],
                                    'latitude': item['pad']['latitude'],
                                    'longitude': item['pad']['longitude'],
                                    'total_launch_count': item['pad']['total_launch_count']
                                }
                            )[0],
                            'webcast_live': item['webcast_live'],
                            'image': item.get('image', ''),
                            'infographic': item.get('infographic', '')
                        }
                    )
                    if created:
                        total_inserted += 1
                        self.stdout.write(self.style.SUCCESS(f'Inserted new launch: {item["name"]}'))
                    else:
                        total_updated += 1
                        self.stdout.write(self.style.SUCCESS(f'Updated existing launch: {item["name"]}'))

                    for program_data in item.get('program', []):
                        program, _ = Program.objects.get_or_create(
                            name=program_data['name'],
                            defaults={
                                'description': program_data.get('description', ''),
                                'image_url': program_data.get('image_url', ''),
                                'start_date': parse_datetime(program_data.get('start_date', '')),
                                'end_date': parse_datetime(program_data.get('end_date', '')) if program_data.get('end_date') else None,
                                'info_url': program_data.get('info_url', ''),
                                'wiki_url': program_data.get('wiki_url', ''),
                            }
                        )
                        for agency_data in program_data.get('agencies', []):
                            agency, _ = Agency.objects.get_or_create(
                                name=agency_data['name'],
                                defaults={'type': agency_data.get('type', '')}
                            )
                            program.agencies.add(agency)
                        launch.programs.add(program)
                        self.stdout.write(self.style.NOTICE(f'Added program {program_data["name"]} to launch {item["name"]}'))

                except Exception as e:
                    errors.append((item, e))
                    self.stdout.write(self.style.ERROR(f'Error processing launch {item["name"]}: {e}'))

            url = data.get('next')
        self.stdout.write(self.style.SUCCESS(f'Concluído! {total_inserted} lançamentos inseridos e {total_updated} lançamentos atualizados.'))

        if errors:
            self.stdout.write(self.style.ERROR('Erros encontrados durante o processamento:'))
            for item, error in errors:
                self.stdout.write(self.style.ERROR(f'Item com erro: {item}'))
                self.stdout.write(self.style.ERROR(f'Mensagem de erro: {error}'))