import django_filters

from space.models import *

class LaunchFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    # dadndo erro porque a query coloca a hora no where, precisa comparar apenas a data e tirar a hora da condição
    start_date = django_filters.DateFilter(field_name='window_start', method='filter_by_date')
    def filter_by_date(self, queryset, name, value):
        return queryset.filter(window_start__date=value)



    # dando erro porque precisa comparar o campo status_id da tabela launches para pegar o dado da tabela status
    status = django_filters.ChoiceFilter(
        field_name='status_id__id',
        choices=[
            ('1', 'Go for Launch'),
            ('2', 'To be Confirmed'),
            ('3', 'To be Determined'),
            ('4', 'Launch Successful'),
            ('5', 'Launch Failure'),
        ],
        empty_label='Any'
    )
    def get_status_choices():
        return [(status.name, status.name) for status in Status.objects.all()]
    
    
    class Meta:
        model = Launch
        fields = ['name', 'window_start', 'status']
