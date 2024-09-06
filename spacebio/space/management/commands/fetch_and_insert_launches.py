from django.core.management.base import BaseCommand
import requests
from django.db import transaction
import logging
from colorama import Fore, Style
from datetime import datetime, timezone, timedelta
from space.models import *

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class Command(BaseCommand):
    help = 'Fetch and save news data from API'

    def handle(self, *args, **kwargs):
        script_name = 'fetch_and_insert_launches'
        base_url = 'https://lldev.thespacedevs.com/2.2.0/launch/?limit=100&mode=detailed'


        # Fetch the last execution log
        last_execution_log = ExecutionLog.objects.filter(script_name=script_name, url=base_url).first()
        if last_execution_log:
            last_executed = last_execution_log.last_executed - timedelta(days=20) # fetch from the last 20 days to avoid losing data
        else:
            last_executed = None
            
        print(f"Last execution: {last_executed}")
        
        #If there was a previous execution, add the timestamp to the URL
        if last_executed:
            last_executed_str = last_executed.isoformat().replace("+00:00", "Z")
            url = f'{base_url}&last_updated__gte={last_executed_str}'
        else:
            url = base_url
        

        def insert_or_update_launch_status(data):
            try:
                launch_status, created = LaunchStatus.objects.update_or_create(
                    id=data['id'],
                    defaults={
                        'name': data['name'],
                        'abbrev': data['abbrev'],
                        'description': data['description']
                    }
                )

                return launch_status
            except Exception as e:
                logger.error(f"Failed to insert or update launch status: {e}")
                raise


        def insert_or_update_net_precision(data):
            try:
                net_precision, created = NetPrecision.objects.update_or_create(
                    id=data['id'],
                    defaults={
                        'name': data['name'],
                        'abbrev': data['abbrev'],
                        'description': data['description']
                    }
                )
                    
                return net_precision
            except Exception as e:
                logger.error(f"Failed to insert or update net precision: {e}")
                raise


        def insert_or_update_expedition(data):
            try:
                pass
                # expedition, created = Expedition.objects.update_or_create(
                #     id=data['id'],
                #     defaults={
                #         'name': data['name'],
                #         'start': data['start'],
                #         'end': data['end'],
                #         'spacestation': data['spacestation'],
                #         'crew': data['crew'],
                #         'mission_patches': data['mission_patches'],
                #         'spacewalks': data['spacewalks'],
                #     }
                # )
                # if created:
                #     logger.info(f"Expedition {expedition.id} created.")
                # else:
                #     logger.info(f"Expedition {expedition.id} updated.")
                # return expedition
            except Exception as e:
                logger.error(f"Failed to insert or update expedition: {e}")
                raise


        def insert_or_update_agency(data):
            agency = None 
            try:
                if isinstance(data, dict):
                    agency, created = Agency.objects.update_or_create(
                        id=data['id'],
                        defaults={
                            'name': data['name'],
                            'featured': data.get('featured', False),
                            'type': data.get('type', None),
                            'country_code': data.get('country_code', None),
                            'abbrev': data.get('abbrev', None),
                            'description': data.get('description', None),
                            'administrator': data.get('administrator', None),
                            'founding_year': data.get('founding_year', None),
                            'launchers': data.get('launchers', None),
                            'spacecraft': data.get('spacecraft', None),
                            'launch_library_url': data.get('launch_library_url', None),
                            'total_launch_count': data.get('total_launch_count', 0),
                            'successful_launches': data.get('successful_launches', 0),
                            'consecutive_successful_launches': data.get('consecutive_successful_launches', 0),
                            'failed_launches': data.get('failed_launches', 0),
                            'pending_launches': data.get('pending_launches', 0),
                            'successful_landings': data.get('successful_landings', 0),
                            'failed_landings': data.get('failed_landings', 0),
                            'attempted_landings': data.get('attempted_landings', 0),
                            'consecutive_successful_landings': data.get('consecutive_successful_landings', 0),
                            'info_url': data.get('info_url', None),
                            'wiki_url': data.get('wiki_url', None),
                            'logo_url': data.get('logo_url', None),
                            'image_url': data.get('image_url', None),
                            'nation_url': data.get('nation_url', None)
                        }
                    )
                elif isinstance(data, int):
                    # Caso a função receba apenas um ID
                    agency, created = Agency.objects.get_or_create(id=data)
                else:
                    raise ValueError("Data should be either a dictionary or an integer ID.")
                
                return agency
            
            except KeyError as e:
                logger.error(f"Missing key in agency data: {e}")
                return None
            except Exception as e:
                logger.error(f"Failed to insert or update agency: {e}")
                return None

        def insert_or_update_mission_patches(data):
            try:
                agency = insert_or_update_agency(data['agency']) if data['agency'] else None

                mission_patch, created = MissionPatches.objects.update_or_create(
                    id=data['id'],
                    defaults={
                        'name': data['name'],
                        'priority': data['priority'],
                        'image_url': data['image_url'],
                        'agency': agency,
                    }
                )
                if created:
                    logger.info(f"Mission patch {mission_patch.id} created.")

                return mission_patch

            except Exception as e:
                logger.error(f"Failed to insert or update mission patch: {e}")
                raise
            

        def insert_or_update_program(data):
            try:
                
                program_type, created = ProgramType.objects.update_or_create(
                    id=data['type']['id'],
                    defaults={
                        'name': data['type']['name']
                    }
                )
                
                program, created = Program.objects.update_or_create(
                    id=data['id'],
                    defaults={
                        'name': data['name'],
                        'description': data['description'],
                        'image_url': data['image_url'],
                        'start_date': data['start_date'],
                        'end_date': data['end_date'],
                        'info_url': data['info_url'],
                        'wiki_url': data['wiki_url'],
                        'type': program_type
                    }
                )
                
                # agencies
                agencies = []
                for agency in data.get('agencies', []):
                    agency_data = insert_or_update_agency(agency)
                    if agency_data:
                        agencies.append(agency_data)
                program.agencies.set(agencies)
                
                
                # mission_patches
                missionPatches = []
                for mission_patch in data.get('mission_patches', []):
                    mission_patch_data = insert_or_update_mission_patches(mission_patch)
                    missionPatches.append(mission_patch_data)
                program.mission_patches.set(missionPatches)

                return program
            except Exception as e:
                logger.error(f"Failed to insert or update program: {e}")
                raise


        def insert_or_update_rocket(data):
            try:
                manufacturer = insert_or_update_agency(data['configuration']['manufacturer'])
                
                configuration, created = LauncherConfig.objects.update_or_create(
                    id = data['configuration']['id'],
                    defaults={
                        'name': data['configuration']['name'],
                        'active': data['configuration']['active'],
                        'reusable': data['configuration']['reusable'],
                        'description': data['configuration']['description'],
                        'family': data['configuration']['family'],
                        'full_name': data['configuration']['full_name'],
                        'manufacturer': manufacturer,
                        'variant': data['configuration']['variant'],
                        'alias': data['configuration']['alias'],
                        'min_stage': data['configuration']['min_stage'],
                        'max_stage': data['configuration']['max_stage'],
                        'length': data['configuration']['length'],
                        'diameter': data['configuration']['diameter'],
                        'maiden_flight': data['configuration']['maiden_flight'],
                        'launch_cost': data['configuration']['launch_cost'],
                        'launch_mass': data['configuration']['launch_mass'],
                        'leo_capacity': data['configuration']['leo_capacity'],
                        'gto_capacity': data['configuration']['gto_capacity'],
                        'to_thrust': data['configuration']['to_thrust'],
                        'apogee': data['configuration']['apogee'],
                        'vehicle_range': data['configuration']['vehicle_range'],
                        'image_url': data['configuration']['image_url'],
                        'info_url': data['configuration']['info_url'],
                        'wiki_url': data['configuration']['wiki_url'],
                        'total_launch_count': data['configuration']['total_launch_count'],
                        'consecutive_successful_launches': data['configuration']['consecutive_successful_launches'],
                        'successful_launches': data['configuration']['successful_launches'],
                        'failed_launches': data['configuration']['failed_launches'],
                        'pending_launches': data['configuration']['pending_launches'],
                        'attempted_landings': data['configuration']['attempted_landings'],
                        'successful_landings': data['configuration']['successful_landings'],
                        'failed_landings': data['configuration']['failed_landings'],
                        'consecutive_successful_landings': data['configuration']['consecutive_successful_landings'],
                    }
                )
                
                programs = []
                for program_data in data['configuration']['program']:
                    program_instance = insert_or_update_program(program_data)
                    programs.append(program_instance)
                configuration.program.set(programs)
                
                rocket, created = Rocket.objects.update_or_create(
                    id=data['id'],
                    defaults={
                        'configuration': configuration,
                        # 'launcher_stage': None, TODO implement
                        'spacecraft_stage': None # TODO implement
                    }
                )
                #===========================================
                # Rocket launcher_stage and spacecraft_stage ARE NOT IMPLEMENTED YET
                # the code below for launcher_stage just skips the creation of the objects
                #===========================================
                launcher_stages = []
                # for launcher_stage in data['launcher_stage']:
                #     launcher_stage = None
                #     launcher_stages.append(launcher_stage)
                
                rocket.launcher_stage.set(launcher_stages)
                #===========================================

                return rocket
            except Exception as e:
                logger.error(f"Failed to insert or update rocket: {e}")
                raise


        def insert_or_update_mission(data):
            try:
                if data['orbit']:
                    orbit, created = Orbit.objects.update_or_create(
                        id=data['orbit']['id'],
                        defaults={
                            'name': data['orbit']['name'],
                            'abbrev': data['orbit']['abbrev'],
                        }
                    )
                
                mission, created = Mission.objects.update_or_create(
                    id=data['id'],
                    defaults={
                        'name': data['name'],
                        'description': data['description'],
                        'launch_designator': data['launch_designator'],
                        'type': data['type'],
                        'orbit': orbit if data['orbit'] else None,
                    }
                )
                #===========================================
                # Mission agencies, info_urls and vid_urls ARE NOT IMPLEMENTED YET
                # the code below for these fields just skips the creation of the objects
                #===========================================
                agencies = []
                info_urls = []
                vid_urls = []
                mission.agencies.set(agencies)
                mission.info_urls.set(info_urls)
                mission.vid_urls.set(vid_urls)
                #===========================================
                

                return mission
            except Exception as e:
                logger.error(f"Failed to insert or update mission: {e}")
                raise


        def insert_or_update_location(data):
            try:
                location, created = Location.objects.update_or_create(
                    id=data['id'],
                    defaults={
                        'name': data['name'],
                        'country_code': data['country_code'],
                        'description': data['description'],
                        'map_image': data['map_image'],
                        'timezone_name': data['timezone_name'],
                        'total_launch_count': data['total_launch_count'],
                        'total_landing_count': data['total_landing_count'],
                    }
                )

                return location
            except Exception as e:
                logger.error(f"Failed to insert or update location: {e}")
                raise    
                        

        def insert_or_update_pad(data):
            try:
                
                agency = insert_or_update_agency(data['agency_id']) if data['agency_id'] else None    
                location = insert_or_update_location(data['location']) if data['location'] else None
                
                pad, created = Pad.objects.update_or_create(
                    id=data['id'],
                    defaults={
                        'agency_id': agency,
                        'name': data['name'],
                        'description': data['description'],
                        'info_url': data['info_url'],
                        'wiki_url': data['wiki_url'],
                        'map_url': data['map_url'],
                        'latitude': data['latitude'],
                        'longitude': data['longitude'],
                        'location': location,
                        'country_code': data['country_code'],
                        'map_image': data['map_image'],
                        'total_launch_count': data['total_launch_count'],
                        'orbital_launch_attempt_count': data['orbital_launch_attempt_count'],
                    }
                )

                return pad
            except Exception as e:
                logger.error(f"Failed to insert or update pad: {e}")
                raise


        def insert_or_update_vid_urls(data, launch):
            
            # this function utilizes two parameters because we need the launch id from the launch_info
            # to use as the foreign key in the VidURLs model
            
            try:
                
                if data['language']:
                    # vid url language
                    language, created = Language.objects.update_or_create(
                        id=data['language']['id'],
                        defaults={
                            'name': data['language']['name'],
                            'code': data['language']['code'],
                        }
                    )
                    
                if data['type']:    
                    # vid url type
                    vid_url_type, created = VidURLType.objects.update_or_create(
                        id=data['type']['id'],
                        defaults={
                            'name': data['type']['name'],
                        }
                    )

                vid_urls, created = VidURLs.objects.update_or_create(
                    url=data['url'],
                    defaults={
                        'launch': launch,
                        'priority': data['priority'],
                        'source': data['source'],
                        'publisher': data['publisher'],
                        'title': data['title'],
                        'description': data['description'],
                        'feature_image': data['feature_image'],
                        'type': vid_url_type if data['type'] else None,
                        'language': language if data['language'] else None,
                        'start_time': data['start_time'],
                        'end_time': data['end_time'],
                    }
                )
                if created:
                    logger.info(f"vid_urls {vid_urls.id} created.")

                return vid_urls
            except Exception as e:
                logger.error(f"Failed to insert or update vid_urls: {e}")
                raise


        def insert_or_update_info_urls(data):
            try:    
                if data['type']:
                    info_url_type, created = InfoURLType.objects.update_or_create(
                        id=data['type']['id'],
                        defaults={
                            'name': data['type']['name'],
                        }
                    )

                info_urls, created = InfoURLs.objects.update_or_create(
                    url=data['url'],
                    defaults={
                        'priority': data['priority'],
                        'source': data['source'],
                        'title': data['title'],
                        'description': data['description'],
                        'feature_image': data['feature_image'],
                        'type': info_url_type if data['type'] else None,
                    }
                )

                return info_urls
            except Exception as e:
                logger.error(f"Failed to insert or update info_urls: {e}")
                raise


        
        def insert_or_update_launch(data):
            nonlocal total_inserted
            nonlocal total_updated
            try:
                # Fetch existing launch from the database if it exists
                existing_launch = Launch.objects.filter(id=data['id']).first()

                # Prepare foreign key fields
                status = insert_or_update_launch_status(data['status']) if data['status'] else None
                net_precision = insert_or_update_net_precision(data['net_precision']) if data['net_precision'] else None
                launch_service_provider = insert_or_update_agency(data['launch_service_provider']) if data['launch_service_provider'] else None
                rocket = insert_or_update_rocket(data['rocket']) if data['rocket'] else None
                mission = insert_or_update_mission(data['mission']) if data['mission'] else None
                pad = insert_or_update_pad(data['pad']) if data['pad'] else None

                # Create or update launch
                launch, created = Launch.objects.update_or_create(
                    id=data['id'],
                    defaults={
                        'slug': data['slug'],
                        'flightclub_url': data['flightclub_url'],
                        'r_spacex_api_id': data['r_spacex_api_id'],
                        'name': data['name'],
                        'status': status,
                        'last_updated': data['last_updated'],
                        'net': data['net'],
                        'net_precision': net_precision,
                        'window_end': data['window_end'],
                        'window_start': data['window_start'],
                        'probability': data['probability'],
                        'weather_concerns': data['weather_concerns'],
                        'holdreason': data['holdreason'],
                        'failreason': data['failreason'],
                        'hashtag': data['hashtag'],
                        'launch_service_provider': launch_service_provider,
                        'rocket': rocket,
                        'mission': mission,
                        'pad': pad,
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

                # Check if the launch was created or updated
                if created:
                    total_inserted += 1
                    logger.info(f'{Fore.GREEN}Inserted new Launch: {launch.name}{Style.RESET_ALL}')
                else:
                    changes = []
                    for field, new_value in data.items():
                        if field in launch._meta.fields:  # Skip fields that aren't in the model
                            old_value = getattr(existing_launch, field, None)
                            if old_value != new_value:
                                changes.append(f"{field}: '{old_value}' -> '{new_value}'")
                    
                    if changes:
                        total_updated += 1
                        logger.info(f"{Fore.BLUE}Updated Launch: {launch.name}{Style.RESET_ALL}")
                        logger.info(f"Changes: {', '.join(changes)}")

                    
                
                # GETS THE MANY-TO-MANY FIELDS
                # info_urls
                infoURLs = []	
                for info_url in data.get('infoURLs', []):
                    info_url_data = insert_or_update_info_urls(info_url)
                    infoURLs.append(info_url_data)
                launch.InfoURLs.set(infoURLs)
                
                # vid_urls
                vidURLs = []
                for vid_url in data.get('vidURLs', []):
                    vid_url_data = insert_or_update_vid_urls(vid_url, launch) # two parameters explained in the function
                    vidURLs.append(vid_url_data)
                launch.VidURLs.set(vidURLs)

                # programs
                programs = []
                for program in data.get('programs', []):
                    program_data = insert_or_update_program(program)
                    programs.append(program_data)
                launch.program.set(programs)
                
                # mission_patches
                missionPatches = []
                for mission_patch in data.get('mission_patches', []):
                    mission_patch_data = insert_or_update_mission_patches(mission_patch)
                    missionPatches.append(mission_patch_data)
                launch.mission_patches.set(missionPatches)
                
                return launch, total_inserted, total_updated
            
            except Exception as e:
                logger.error(f'{Fore.RED}Error updating/inserting launch: {e}{Style.RESET_ALL}')
                raise

        total_inserted = 0
        total_updated = 0

        @transaction.atomic
        def insert_data(data):

            try:
                # this main function bellow calls all the other necessaries functions to get and insert data
                insert_or_update_launch(data)

            except Exception as e:
                logger.error(f'{Fore.RED}Transaction failed: {e}{Style.RESET_ALL}')
                raise


        def fetch_and_insert_all_launches():
            next_url = url
            page = 1

            logger.info(f'{Fore.MAGENTA}Fetching data updated after {last_executed}')
            while next_url:
                try:
                    logger.info(f'{Fore.MAGENTA}Fetching data from page {page}: {next_url}{Style.RESET_ALL}')
                    response = requests.get(next_url)
                    response.raise_for_status()
                    data = response.json()

                    for launch_data in data['results']:
                        insert_data(launch_data)
                        

                    next_url = data.get('next', None)
                    page += 1

                except requests.exceptions.RequestException as e:
                    logger.error(f'{Fore.RED}Error fetching page {page}: {e}{Style.RESET_ALL}')
                

            # Update or create the execution log
            ExecutionLog.objects.update_or_create(
                script_name=script_name,
                url=base_url,
                defaults={'last_executed': datetime.now(timezone.utc)}
            )
            

        fetch_and_insert_all_launches()

        logger.info(f'{Fore.GREEN}Total of {total_inserted} launches inserted.{Style.RESET_ALL}')
        logger.info(f'{Fore.BLUE}Total of {total_updated} launches updated.{Style.RESET_ALL}')
