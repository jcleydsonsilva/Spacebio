import json
from datetime import datetime
from space.models import *


# este e o script de fetch_launches mas apenas com esse codigo, ainda não testei se funciona



def update_or_create_launch(launch_data):
    # Tenta buscar um lançamento existente pelo ID ou cria um novo
    launch, created = Launch.objects.get_or_create(id=launch_data['id'])

    for field, value in launch_data.items():
        if hasattr(launch, field):
            field_obj = getattr(Launch, field).field

            if isinstance(field_obj, models.ForeignKey):
                related_model = field_obj.related_model
                related_obj = get_or_create_object(related_model, **value)
                setattr(launch, field, related_obj)
            
            elif isinstance(field_obj, models.ManyToManyField):
                related_model = field_obj.related_model
                related_objects = [
                    get_or_create_object(related_model, **item) for item in value
                ]
                getattr(launch, field).set(related_objects)
            
            else:
                setattr(launch, field, value)

    launch.save()

def get_or_create_object(model, **data):
    # Tenta buscar ou criar uma instância do modelo relacionado
    obj, created = model.objects.update_or_create(
        id=data['id'], defaults=data
    )
    return obj
