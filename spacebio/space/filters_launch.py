import django_filters
from django.db.models import Q
from django.utils.timezone import now

from space.models import *

class LaunchFilter(django_filters.FilterSet):
    # Filtro para palavras-chave em vários campos
    keywords = django_filters.CharFilter(method='filter_by_keywords', label='Filter by name')

    def filter_by_keywords(self, queryset, name, value):
        return queryset.filter(
            Q(slug__icontains=value) |
            Q(name__icontains=value)
        )

    start_date = django_filters.DateFromToRangeFilter(field_name='window_start', label='Date Range')
    def filter_queryset(self, queryset):
        data = self.form.cleaned_data
        start_date_after = data.get('start_date_after')
        start_date_before = data.get('start_date_before')
        current_time = now()

        # Caso o usuário informe apenas uma data (após)
        if start_date_after and not start_date_before:
            return queryset.filter(window_start__gte=start_date_after)

        # Caso o usuário informe apenas uma data (antes)
        if start_date_before and not start_date_after:
            return queryset.filter(window_start__lte=start_date_before)

        # Caso o usuário informe ambas as datas
        if start_date_after and start_date_before:
            return queryset.filter(window_start__range=(start_date_after, start_date_before))

        # Se nenhum filtro de data for aplicado, retorne o queryset original
        return super().filter_queryset(queryset)

    # Filtro de Status
    status = django_filters.ChoiceFilter(
        field_name='status__id',
        choices=[
            (1, 'Go for Launch'),
            (8, 'To Be Confirmed'),
            (2, 'To be Determined'),
            (3, 'Launch Successful'),
            (4, 'Launch Failure'),
            (7, 'Launch was a Partial Failure'),
        ],
        empty_label='Any'
    )

    # Filtro de Provedor de Serviços de Lançamento
    launch_service_provider = django_filters.ModelChoiceFilter(
        field_name='launch_service_provider',
        queryset=Agency.objects.all(),
        label='Launch Service Provider',
        empty_label='Any'
    )

    # Filtro de Localização de Lançamento
    location = django_filters.ModelChoiceFilter(
        field_name='pad__location',
        queryset=Location.objects.all(),
        label='Launch Location',
        empty_label='Any'
    )

    class Meta:
        model = Launch
        fields = ['name', 'window_start', 'status', 'launch_service_provider', 'pad']