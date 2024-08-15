import django_filters

from space.models import *

class LaunchFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    # Filtros de Data
    start_date = django_filters.DateFromToRangeFilter(field_name='window_start', label='Date Range')

    # Filtro de Status
    status = django_filters.ChoiceFilter(
        field_name='status__id',
        choices=[
            (1, 'Go for Launch'),
            (2, 'To be Confirmed'),
            (3, 'To be Determined'),
            (4, 'Launch Successful'),
            (5, 'Launch Failure'),
        ],
        empty_label='Any'
    )

    # # Filtro de Provedor de Serviços de Lançamento
    # launch_service_provider = django_filters.ModelChoiceFilter(
    #     field_name='launch_service_provider',
    #     queryset=LaunchServiceProvider.objects.all(),
    #     label='Launch Service Provider',
    #     empty_label='Any'
    # )

    # # Filtro de Localização de Lançamento
    # location = django_filters.ModelChoiceFilter(
    #     field_name='pad__location',
    #     queryset=Location.objects.all(),
    #     label='Launch Location',
    #     empty_label='Any'
    # )

    # class Meta:
    #     model = Launch
    #     fields = ['name', 'start_date', 'status', 'launch_service_provider', 'location']