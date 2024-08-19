from django.core.management.base import BaseCommand
import requests
from django.db import transaction
import logging
from space.models import *

# Set up logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fetch and save news data from API'

    def handle(self, *args, **kwargs):

        def insert_or_update_launch(data, dry_run=True):
            try:
                # Obter instâncias relacionadas ou None se não houver
                status_instance = LaunchStatus.objects.get(id=data['status']['id']) if data['status'] else None
                net_precision_instance = NetPrecision.objects.get(id=data['net_precision']['id']) if data['net_precision'] else None
                launch_service_provider_instance = Agency.objects.get(id=data['launch_service_provider']['id']) if data['launch_service_provider'] else None
                rocket_instance = Rocket.objects.get(id=data['rocket']['id']) if data['rocket'] else None
                mission_instance = Mission.objects.get(id=data['mission']['id']) if data['mission'] else None
                pad_instance = Pad.objects.get(id=data['pad']['id']) if data['pad'] else None
                
                launch, created = Launch.objects.update_or_create(
                    id=data['id'],
                    defaults={
                        'slug': data['slug'],
                        'flightclub_url': data['flightclub_url'],
                        'r_spacex_api_id': data['r_spacex_api_id'],
                        'name': data['name'],
                        'status': status_instance,  # instância de LaunchStatus
                        'last_updated': data['last_updated'],
                        'net': data['net'],
                        'net_precision': net_precision_instance,  # instância de NetPrecision
                        'window_end': data['window_end'],
                        'window_start': data['window_start'],
                        'probability': data['probability'],
                        'weather_concerns': data['weather_concerns'],
                        'holdreason': data['holdreason'],
                        'failreason': data['failreason'],
                        'hashtag': data['hashtag'],
                        'launch_service_provider': launch_service_provider_instance,  # instância de LaunchServiceProvider
                        'rocket': rocket_instance,  # instância de Rocket
                        'mission': mission_instance,  # instância de Mission
                        'pad': pad_instance,  # instância de Pad
                        'webcast_live': data['webcast_live'],
                        'image': data['image'],
                        'infographic': data['infographic'],
                        'orbital_launch_attempt_count': data['orbital_launch_attempt_count'],
                        'location_launch_attempt_count': data['location_launch_attempt_count'],
                        'pad_launch_attempt_count': data['pad_launch_attempt_count'],
                        'agency_launch_attempt_count': data['agency_launch_attempt_count'],
                        'orbital_launch_attempt_count_year': data['orbital_launch_attempt_count_year'],
                        'location_launch_attempt_count_year': data['location_launch_attempt_count_year'],
                        'pad_launch_attempt_count_year': data['pad_launch_attempt_count_year'],
                        'agency_launch_attempt_count_year': data['agency_launch_attempt_count_year'],
                        'pad_turnaround': data['pad_turnaround'],
                    }
                )
                if created:
                    logger.info(f"Launch {launch.id} created.")
                else:
                    logger.info(f"Launch {launch.id} updated.")
                return launch
            except Exception as e:
                logger.error(f"Error inserting/updating launch: {e}")
                raise

        # def insert_or_update_rocket(data):
        #     try:
        #         rocket, created = Rocket.objects.update_or_create(
        #             id=data['id'],
        #             defaults={
        #                 'configuration': LauncherConfig.objects.get(id=data['configuration_id']),
        #                 'spacecraft_stage': data.get('spacecraft_stage'),
        #             }
        #         )
        #         if created:
        #             logger.info(f"Rocket {rocket.id} created.")
        #         else:
        #             logger.info(f"Rocket {rocket.id} updated.")
        #         return rocket
        #     except Exception as e:
        #         logger.error(f"Error inserting/updating rocket: {e}")
        #         raise

        # def insert_or_update_orbit(data):
            # try:
            #     orbit, created = Orbit.objects.update_or_create(
            #         id=data['id'],
            #         defaults={
            #             'name': data['name'],
            #             'abbrev': data['abbrev'],
            #         }
            #     )
            #     if created:
            #         logger.info(f"Orbit {orbit.id} created.")
            #     else:
            #         logger.info(f"Orbit {orbit.id} updated.")
            #     return orbit
            # except Exception as e:
            #     logger.error(f"Error inserting/updating orbit: {e}")
            #     raise

        @transaction.atomic
        def insert_data(data):
            try:
                
                insert_or_update_launch(data, dry_run=True)
                
                # Insert or update rocket
                # rocket_data = data['rocket']
                # rocket = insert_or_update_rocket(rocket_data)

                # Insert or update orbit
                # orbit_data = data['orbit']
                # orbit = insert_or_update_orbit(orbit_data)

            except Exception as e:
                logger.error(f"Transaction failed: {e}")
                raise

        # Example usage
        data = requests.get('https://lldev.thespacedevs.com/2.2.0/launch/?limit=1&mode=detailed').json()
        data = data['results'][0]

        insert_data(data)
