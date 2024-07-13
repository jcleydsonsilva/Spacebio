import django_filters
from space.models import Launch

class LaunchFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    # dadndo erro porque a query coloca a hora no where, precisa comparar apenas a data e tirar a hora da condição
    start_date = django_filters.DateFilter(field_name='window_start', lookup_expr='date')


    # dando erro porque precisa comparar o campo status_id da tabela launches para pegar o dado da tabela status
    status = django_filters.ChoiceFilter(
        field_name='status',
        choices=[('upcoming', 'Upcoming'), ('completed', 'Completed')],
        empty_label='Any'
    )

    class Meta:
        model = Launch
        fields = ['name', 'window_start', 'status']
