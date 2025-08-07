from django.urls import path
from voting.views import (
    load_localities,
    load_zones,
    load_party_details,
    VoterPreloadView,
    dni_validate,
    IndexView,
    VoteView,
    ElectionResultsView,
    close_voting,
)

urlpatterns = [
    path('index', IndexView.as_view(), name='index'),
    path('validar-dni/', dni_validate, name='dni_validate'),
    path('ajax/load-localities/', load_localities, name='load_localities'),
    path('ajax/load-zones/', load_zones, name='load_zones'),
    path('ajax/load-party-details/', load_party_details, name='load_party_details'),
    path('preload/', VoterPreloadView.as_view(), name='preload'),
    path('vote/', VoteView.as_view(), name='vote'),
    path('results/', ElectionResultsView.as_view(), name='results'),
    path('close_voting/', close_voting, name='close_voting'),
]