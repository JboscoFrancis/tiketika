import django_filters
from django_filters import CharFilter
from django.forms.widgets import TextInput, DateInput
from .models import Route

class RouteFilter(django_filters.FilterSet):
    source = django_filters.CharFilter(label = 'From', lookup_expr='icontains', widget=TextInput(attrs={'class': 'form-control','placeholder': 'from'}))
    destination = django_filters.CharFilter(label = 'To', lookup_expr='icontains', widget=TextInput(attrs={'class': 'form-control','placeholder': 'to'}))
    journey_date = django_filters.DateFilter(label = 'journey_date', widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Route
        fields = ['source','destination','bus','journey_date']