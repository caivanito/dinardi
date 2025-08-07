from django.contrib import admin

# Register your models here.

from voting.models import (
    Voter,
    PoliticalParty,
    Province,
    Locality,
    Zone,
    Vote,
    VotingStatus
    )

admin.site.register(Voter)
admin.site.register(PoliticalParty)
admin.site.register(Province)
admin.site.register(Locality)
admin.site.register(Zone)
admin.site.register(Vote)
admin.site.register(VotingStatus)