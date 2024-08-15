import requests
from django.utils.dateparse import parse_datetime
from space.models import *


# esse é um dos scripts que estou testando, este é mais completo e utiliza funções nativas do django



def fetch_and_insert_launches():
    url = 'URL_DA_API' # https://lldev.thespacedevs.com/2.2.0/launch/?mode=detailed
    try:
        response = requests.get(url)
        response.raise_for_status()
        launches = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer requisição à API: {e}")
        return

    for launch_data in launches:
        try:
            # Busca ou cria objetos relacionados
            status = get_or_create_object(LaunchStatus, name=launch_data.get('status'))
            net_precision = get_or_create_object(NetPrecision, name=launch_data.get('net_precision'))
            agency = get_or_create_object(Agency, name=launch_data.get('launch_service_provider'))
            rocket = get_or_create_object(Rocket, name=launch_data.get('rocket'))
            mission = get_or_create_object(Mission, name=launch_data.get('mission'))
            pad = get_or_create_object(Pad, name=launch_data.get('pad'))

            # Criação ou atualização do lançamento
            launch = create_or_update_launch(launch_data, status, net_precision, agency, rocket, mission, pad)
            
            # Atualização dos ManyToMany fields
            update_many_to_many_fields(launch, launch_data)

        except Exception as e:
            print(f"Erro ao processar lançamento {launch_data.get('id')}: {e}")

    print("Lançamentos inseridos/atualizados com sucesso.")

def get_or_create_object(model, **kwargs):
    obj, created = model.objects.get_or_create(**kwargs)
    return obj

def create_or_update_launch(data, status, net_precision, agency, rocket, mission, pad):
    launch_id = data.get('id')
    launch, created = Launch.objects.update_or_create(
        launch_id=launch_id,
        defaults={
            'slug': data.get('slug'),
            'flightclub_url': data.get('flightclub_url'),
            'r_spacex_api_id': data.get('r_spacex_api_id'),
            'name': data.get('name'),
            'status': status,
            'last_updated': parse_datetime(data.get('last_updated')),
            'net': parse_datetime(data.get('net')),
            'net_precision': net_precision,
            'window_end': parse_datetime(data.get('window_end')),
            'window_start': parse_datetime(data.get('window_start')),
            'probability': data.get('probability'),
            'weather_concerns': data.get('weather_concerns'),
            'holdreason': data.get('holdreason'),
            'failreason': data.get('failreason'),
            'hashtag': data.get('hashtag'),
            'launch_service_provider': agency,
            'rocket': rocket,
            'mission': mission,
            'pad': pad,
            'webcast_live': data.get('webcast_live'),
            'image': data.get('image'),
            'infographic': data.get('infographic'),
            'orbital_launch_attempt_count': data.get('orbital_launch_attempt_count'),
            'location_launch_attempt_count': data.get('location_launch_attempt_count'),
            'pad_launch_attempt_count': data.get('pad_launch_attempt_count'),
            'agency_launch_attempt_count': data.get('agency_launch_attempt_count'),
            'orbital_launch_attempt_count_year': data.get('orbital_launch_attempt_count_year'),
            'location_launch_attempt_count_year': data.get('location_launch_attempt_count_year'),
            'pad_launch_attempt_count_year': data.get('pad_launch_attempt_count_year'),
            'agency_launch_attempt_count_year': data.get('agency_launch_attempt_count_year'),
            'pad_turnaround': data.get('pad_turnaround')
        }
    )
    return launch

def update_many_to_many_fields(launch, data):
    # Limpa campos ManyToMany antes de atualizar
    launch.updates.clear()
    launch.InfoURLs.clear()
    launch.VidURLs.clear()
    launch.program.clear()
    launch.timeline.clear()
    launch.mission_patches.clear()

    # Atualiza campos ManyToMany
    for update_data in data.get('updates', []):
        update = get_or_create_object(Updates, name=update_data)
        launch.updates.add(update)

    for infourl_data in data.get('InfoURLs', []):
        infourl = get_or_create_object(InfoURLs, url=infourl_data)
        launch.InfoURLs.add(infourl)

    for vidurl_data in data.get('VidURLs', []):
        vidurl = get_or_create_object(VidURLs, url=vidurl_data)
        launch.VidURLs.add(vidurl)

    for program_data in data.get('program', []):
        program = get_or_create_object(Program, name=program_data)
        launch.program.add(program)


    for patch_data in data.get('mission_patches', []):
        patch = get_or_create_object(MissionPatches, image_url=patch_data)
        launch.mission_patches.add(patch)

    launch.save()
